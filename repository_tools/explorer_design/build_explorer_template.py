"""Build the canonical Explorer template from the retained design sources.

The designed views (``sources/*.dc.html``) are the export of the design
session, retained verbatim so a later design round is reviewable as a diff.
This tool applies an explicit, count-asserted patch list that binds the views
to the generated bundle contract, inlines the component runtime, the vendored
React UMD builds (verified against the subresource-integrity digests the
runtime itself declares), and the design-system stylesheet, and writes one
self-contained ``index.template.html``.

    python -m repository_tools.explorer_design.build_explorer_template          # write
    python -m repository_tools.explorer_design.build_explorer_template --check  # verify

The build is deterministic: identical sources produce identical bytes.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
REPOSITORY_ROOT = HERE.parents[1]
SOURCES = HERE / "sources"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "templates" / "repository" / "standard" / "scripts" / "harness_explorer" / "index.template.html"
BOOTSTRAP_MARKER = "__HARNESS_BOOTSTRAP_JSON__"
MAX_TEMPLATE_BYTES = 524_288

#: Designed views embedded as component sources, in the order they are keyed.
VIEWS = ("Overview", "Lineage View", "Graph", "Record")
VENDORED = (
    ("vendor/react.production.min.js", "REACT_SRI"),
    ("vendor/react-dom.production.min.js", "REACT_DOM_SRI"),
)


#: URL-shaped string literals the vendored code legitimately contains: XML
#: namespace identifiers used with createElementNS and React's minified
#: error-message pointer. None is ever requested.
ALLOWED_URL_LITERALS = frozenset(
    {
        "http://www.w3.org/1998/Math/MathML",
        "http://www.w3.org/1999/xhtml",
        "http://www.w3.org/1999/xlink",
        "http://www.w3.org/2000/svg",
        "http://www.w3.org/XML/1998/namespace",
        "https://reactjs.org/docs/error-decoder.html?invariant=",
    }
)


class BuildError(RuntimeError):
    """The sources do not match the patch list or a build constraint."""


@dataclass(frozen=True)
class Patch:
    """One exact replacement with the number of occurrences it must hit."""

    old: str
    new: str
    count: int
    files: tuple[str, ...]
    regex: bool = False


NAV_ANCHOR_STYLE = (
    'style="display:block;padding:10px 16px;border-left:3px solid transparent;'
    "font:600 13px var(--font-body);color:var(--l-fg);text-decoration:none;"
    'white-space:nowrap;overflow:hidden" style-hover="background:var(--l-soft);color:var(--l-accent-deep)"'
)

BASE_PATCHES: tuple[Patch, ...] = (
    # Self-containment: the design-system assets are inlined by the shell.
    Patch('<link rel="stylesheet" href="_ds/modernist-fa553ae2-9bac-470c-a217-b75ed1439a60/styles.css">\n', "", 4, VIEWS),
    Patch('<script src="_ds/modernist-fa553ae2-9bac-470c-a217-b75ed1439a60/_ds_bundle.js"></script>\n', "", 4, VIEWS),
    # Navigation between views is query-string routing inside one document.
    Patch('href="Overview.dc.html"', 'href="?view=overview"', 3, ("Overview", "Lineage View", "Graph")),
    Patch('href="Lineage View.dc.html"', 'href="?view=lineage"', 3, ("Overview", "Lineage View", "Graph")),
    Patch('href="Graph.dc.html"', 'href="?view=graph"', 3, ("Overview", "Lineage View", "Graph")),
    Patch("href: 'Lineage View.dc.html'", "href: '?view=lineage'", 2, ("Overview",)),
    Patch("'Lineage View.dc.html?artifact=' + encodeURIComponent(", "'?view=lineage&artifact=' + encodeURIComponent(", 2, ("Overview", "Graph")),
    Patch(' <a href="Rationale.dc.html">Design rationale</a>', "", 1, ("Lineage View",)),
    # Same-view deep links keep the current view.
    Patch("window.location.pathname", "window.HarnessExplorer.viewHref()", 3, ("Lineage View", "Graph")),
    Patch("'?artifact=' + encodeURIComponent(", "window.HarnessExplorer.artifactHref(", 2, ("Lineage View", "Graph")),
    # Data access goes through the shell's manifest-verified loader.
    Patch("fetch('data/lineage-bundle.json').then(r => r.json())", "window.HarnessExplorer.bundle()", 3, ("Overview", "Lineage View", "Graph")),
    Patch("fetch('uploads/artifacts/topology.json').then(r => r.json())", "window.HarnessExplorer.topology()", 1, ("Graph",)),
    Patch("fetch(this._root + 'artifacts/' + id + '.json')", "window.HarnessExplorer.artifactResponse(id)", 1, ("Lineage View",)),
    Patch("fetch((b.data_root || '') + 'artifacts/' + id + '.json')", "window.HarnessExplorer.artifactResponse(id)", 1, ("Overview",)),
    Patch("fetch((this.props.dataRoot || '') + 'artifacts/' + id + '.json')", "window.HarnessExplorer.artifactResponse(id)", 1, ("Record",)),
    Patch("fetch(this._root + d.raw_path)", "window.HarnessExplorer.evidenceResponse(d.raw_path)", 1, ("Lineage View",)),
    Patch("fetch((this.props.dataRoot || '') + doc.raw_path)", "window.HarnessExplorer.evidenceResponse(doc.raw_path)", 1, ("Record",)),
    # The text filter is a search field so the platform supplies a visible
    # clear control beside the existing Escape shortcut.
    Patch('<input value="{{query}}" onChange="{{onQuery}}" onKeyDown="{{onSearchKey}}" placeholder="Search id or title', '<input type="search" value="{{query}}" onChange="{{onQuery}}" onKeyDown="{{onSearchKey}}" placeholder="Search id or title', 1, ("Lineage View",)),
    # Reader preferences never persist beyond the page.
    Patch("localStorage.getItem('lin-nav-open')", "window.HarnessExplorer.prefs.getItem('lin-nav-open')", 3, ("Overview", "Lineage View", "Graph")),
    Patch("localStorage.setItem('lin-nav-open', v ? '1' : '0')", "window.HarnessExplorer.prefs.setItem('lin-nav-open', v ? '1' : '0')", 3, ("Overview", "Lineage View", "Graph")),
    # The Readiness view joins the navigation.
    Patch(
        ">{{graphLabel}}</a>",
        '>{{graphLabel}}</a>\n    <a href="?view=readiness" title="Readiness" ' + NAV_ANCHOR_STYLE + ">{{readinessLabel}}</a>",
        3,
        ("Overview", "Lineage View", "Graph"),
    ),
    Patch("graphLabel: open ? 'Virtual Twin' : 'V',", "graphLabel: open ? 'Virtual Twin' : 'V',\n      readinessLabel: open ? 'Readiness' : 'R',", 3, ("Overview", "Lineage View", "Graph")),
    # Overview indicators come from the generator's metrics block instead of
    # fetching every artifact detail; the fan-out remains as a fallback.
    Patch(
        "      return Promise.all((b.detail_ids || []).map(id =>\n        window.HarnessExplorer.artifactResponse(id).then(r => r.ok ? r.json() : null).catch(() => null).then(d => [id, d])\n      ));",
        "      if (b.metrics) return [];\n      return Promise.all((b.detail_ids || []).map(id =>\n        window.HarnessExplorer.artifactResponse(id).then(r => r.ok ? r.json() : null).catch(() => null).then(d => [id, d])\n      ));",
        1,
        ("Overview",),
    ),
    Patch(
        "    const details = [...this._details.values()].map(d => d.artifact);\n",
        "    const details = [...this._details.values()].map(d => d.artifact);\n    const m = b.metrics || null;\n",
        1,
        ("Overview",),
    ),
    Patch(
        "    const rlsDetail = details.filter(a => a.type === 'release_record' && a.status === 'released').sort((a, z) => String(z.released_at || '').localeCompare(String(a.released_at || '')))[0];",
        "    const rlsDetail = m ? (m.latest_release || null) : details.filter(a => a.type === 'release_record' && a.status === 'released').sort((a, z) => String(z.released_at || '').localeCompare(String(a.released_at || '')))[0];\n    const missingCoverage = (b.coverage || []).filter(row => row.active && (!row.specified || !row.verified)).map(row => row.requirement);",
        1,
        ("Overview",),
    ),
    Patch(
        "        href: this.lin('REQ-LRE-003'), linkLabel: 'Coverage per requirement →'",
        "        href: false, chips: missingCoverage.map(id => ({ label: id, href: this.lin(id) }))",
        1,
        ("Overview",),
    ),
    Patch(
        "    const events = details.flatMap(a => (a.lifecycle_events || []).map(e => ({ ...e, artifact: a.id })));\n    const unattributed = events.filter(e => !e.decided_by).length;\n    const roles = {};\n    events.forEach(e => { if (e.decided_by) roles[e.decided_by] = (roles[e.decided_by] || 0) + 1; });",
        "    const eventList = details.flatMap(a => (a.lifecycle_events || []).map(e => ({ ...e, artifact: a.id })));\n    const events = { length: m ? m.lifecycle_events : eventList.length };\n    const unattributed = m ? m.unattributed_events : eventList.filter(e => !e.decided_by).length;\n    const roles = m ? { ...(m.decided_by || {}) } : {};\n    if (!m) eventList.forEach(e => { if (e.decided_by) roles[e.decided_by] = (roles[e.decided_by] || 0) + 1; });",
        1,
        ("Overview",),
    ),
    Patch(
        "    const delegT = events.filter(e => String(e.decided_by || '').includes('delegated')).length;\n    const delegRec = details.filter(a => String(a.prepared_by || '').includes('delegated')).length;",
        "    const delegT = m ? m.delegated_transitions : eventList.filter(e => String(e.decided_by || '').includes('delegated')).length;\n    const delegRec = m ? m.delegated_records : details.filter(a => String(a.prepared_by || '').includes('delegated')).length;\n    const delegIds = m ? (m.delegated_artifacts || []) : [...new Set([...eventList.filter(e => String(e.decided_by || '').includes('delegated')).map(e => e.artifact), ...details.filter(a => String(a.prepared_by || '').includes('delegated')).map(a => a.id)])];",
        1,
        ("Overview",),
    ),
    Patch(
        "        sub: 'across the ' + details.length + ' records sampled in this bundle',",
        "        sub: 'across all ' + (m ? (c.artifacts || 0) : details.length) + ' records in this bundle',",
        1,
        ("Overview",),
    ),
    Patch(
        "        chips: [{ label: 'WO-ECP-024', href: this.lin('WO-ECP-024') }, { label: 'VREC-ECP-028', href: this.lin('VREC-ECP-028') }]",
        "        chips: delegIds.map(id => ({ label: id, href: this.lin(id) }))",
        1,
        ("Overview",),
    ),
    Patch(
        "        chips: [{ label: 'VREC-SEH-021', href: this.lin('VREC-SEH-021') }]",
        "        chips: (m && m.latest_release && m.latest_release.verification_record ? [{ label: m.latest_release.verification_record, href: this.lin(m.latest_release.verification_record) }] : [])",
        1,
        ("Overview",),
    ),
    Patch(
        "    details.filter(a => a.type === 'work_order').forEach(a => {\n      const evs = a.lifecycle_events || [];\n      const ap = evs.find(e => e.to === 'approved'), im = evs.find(e => e.to === 'implemented');\n      if (ap && im) { const ms = Date.parse(im.decided_at) - Date.parse(ap.decided_at); if (ms > 0) leads.push({ id: a.id, ms }); }\n    });",
        "    if (m) (m.lead_times || []).forEach(l => leads.push({ id: l.id, ms: l.hours * 3600000 }));\n    else details.filter(a => a.type === 'work_order').forEach(a => {\n      const evs = a.lifecycle_events || [];\n      const ap = evs.find(e => e.to === 'approved'), im = evs.find(e => e.to === 'implemented');\n      if (ap && im) { const ms = Date.parse(im.decided_at) - Date.parse(ap.decided_at); if (ms > 0) leads.push({ id: a.id, ms }); }\n    });",
        1,
        ("Overview",),
    ),
    Patch(
        "        sub: leads.length ? 'p90 ' + this.humanH(p90) + ' · n=' + leads.length + ' work orders in this sample' : '',",
        "        sub: leads.length ? 'p90 ' + this.humanH(p90) + ' · n=' + leads.length + ' work orders' : '',",
        1,
        ("Overview",),
    ),
    Patch(
        "    const relContract = details.find(a => a.type === 'release_contract' && a.status === 'approved');",
        "    const relContract = m ? (m.release_arc ? { id: m.release_arc.contract_id, lifecycle_events: [{ decided_at: m.release_arc.contract_approved_at }] } : null) : details.find(a => a.type === 'release_contract' && a.status === 'approved');",
        1,
        ("Overview",),
    ),
    Patch(
        "        claim: 'The maintainer\\u2019s entry point. The three drafts sit outside this sample\\u2019s scope; the full bundle links each one.',\n        style: this.tileStyle('ok'), figColor: 'var(--l-fg)', rows: false",
        "        claim: 'The maintainer\\u2019s entry point: every draft and ready record is a pending human decision.',\n        style: this.tileStyle('ok'), figColor: 'var(--l-fg)', rows: false,\n        chips: b.artifacts.filter(a => a.status === 'draft' || a.status === 'ready').map(a => ({ label: a.id, href: this.lin(a.id) }))",
        1,
        ("Overview",),
    ),
)

#: WO-DCM-001 (SPEC-DCM-001 rule 13): the in-flight tile lists open and
#: deferred decisions with their age and deciding role; the record panel
#: shows a decision's fields, the decision trail of a concerned artifact and
#: the standing deviations a specification, work order or record inherits.
#: Kept apart so a root released before them can be compared to the build
#: without them.
DECISION_PATCHES: tuple[Patch, ...] = (
    Patch(
        "    const m = b.metrics || null;\n",
        "    const m = b.metrics || null;\n"
        "    const openDecs = b.artifacts.filter(a => a.type === 'decision' && (a.status === 'open' || a.status === 'deferred'));\n"
        "    const decAge = a => { const t0 = Date.parse(a.created || ''), t1 = Date.parse(b.generated_at || '') || Date.now(); return isNaN(t0) ? '' : ' · ' + this.humanH(t1 - t0) + ' old'; };\n",
        1,
        ("Overview",),
    ),
    Patch(
        "        fig: (q.draft ?? 0) + ' drafts · ' + (q.ready ?? 0) + ' ready',",
        "        fig: (q.draft ?? 0) + ' drafts · ' + (q.ready ?? 0) + ' ready' + (openDecs.length ? ' · ' + openDecs.length + ' open decision' + (openDecs.length === 1 ? '' : 's') : ''),",
        1,
        ("Overview",),
    ),
    Patch(
        "        chips: b.artifacts.filter(a => a.status === 'draft' || a.status === 'ready').map(a => ({ label: a.id, href: this.lin(a.id) }))",
        "        chips: [...openDecs.map(a => ({ label: a.id + ' (' + a.status + (a.deciding_roles && a.deciding_roles.length ? ' · ' + a.deciding_roles.join(', ') : '') + decAge(a) + ')', href: this.lin(a.id) })), ...b.artifacts.filter(a => a.status === 'draft' || a.status === 'ready').map(a => ({ label: a.id, href: this.lin(a.id) }))]",
        1,
        ("Overview",),
    ),
    Patch(
        "work_order: 'Work order (WO) — an authorized change', ",
        "work_order: 'Work order (WO) — an authorized change', decision: 'Decision (DEC) — a pending question or an implementation deviation', ",
        1,
        ("Record",),
    ),
    Patch(
        "    push('snapshot sha256', a.artifact_snapshot_sha256, true);\n",
        "    push('snapshot sha256', a.artifact_snapshot_sha256, true);\n"
        "    (a.standing_deviations || []).forEach(id => push('standing deviation', id + ' — accepted; stands until the rule is amended or superseded'));\n"
        "    (a.decisions || []).forEach(d => push('decision ' + d.id, (d.kind || 'decision') + ' · ' + d.status + (d.option ? ' · ' + d.option : '') + (d.decided_by ? ' by ' + d.decided_by : '') + (d.question ? ' — ' + d.question : '')));\n",
        1,
        ("Record",),
    ),
    Patch(
        "    pushMeta('source', a.path);\n",
        "    if (a.type === 'decision') {\n"
        "      pushMeta('kind', a.kind); pushMeta('question', a.question); pushMeta('raised by', a.raised_by);\n"
        "      (a.options || []).forEach(o => pushMeta('option ' + o.id, o.label));\n"
        "      pushMeta('recommendation', a.recommendation); pushMeta('against', a.against); pushMeta('observed', a.observed);\n"
        "      pushMeta('blocks', (a.blocks || []).join(', ')); pushMeta('deciding role', (a.deciding_roles || []).join(', '));\n"
        "      if (a.disposition) { const dp = a.disposition; pushMeta('disposition', (dp.option || '') + (dp.label ? ' — ' + dp.label : '') + (dp.decided_by ? ' · ' + dp.decided_by : '') + (dp.decided_at ? ' · ' + dp.decided_at : '')); pushMeta('disposition reason', dp.reason); pushMeta('revisit', dp.revisit); if (dp.scope && dp.scope.length) pushMeta('deferral scope', dp.scope.join(', ')); }\n"
        "    }\n"
        "    pushMeta('source', a.path);\n",
        1,
        ("Record",),
    ),
)

PATCHES: tuple[Patch, ...] = (*BASE_PATCHES, *DECISION_PATCHES)


def _read(relative: str) -> str:
    path = SOURCES / relative
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise BuildError(f"source {relative} is unavailable or not UTF-8") from exc
    # A checkout may convert line endings; the build is defined over LF bytes.
    return text.replace("\r\n", "\n")


def _apply(patch: Patch, sources: dict[str, str]) -> None:
    hits = 0
    for name in patch.files:
        text = sources[name]
        if patch.regex:
            text, n = re.subn(patch.old, patch.new, text)
        else:
            n = text.count(patch.old)
            text = text.replace(patch.old, patch.new)
        hits += n
        sources[name] = text
    if hits != patch.count:
        raise BuildError(f"patch {patch.old[:70]!r} matched {hits} times across {patch.files}; expected {patch.count}")


def _verify_vendored(runtime: str) -> list[str]:
    scripts: list[str] = []
    for relative, constant in VENDORED:
        declared = re.search(constant + r'\s*=\s*"(sha(\d+)-[A-Za-z0-9+/=]+)"', runtime)
        if not declared:
            raise BuildError(f"the component runtime declares no {constant}")
        algorithm = "sha" + declared.group(2)
        text = _read(relative)
        payload = text.encode("utf-8")
        computed = f"{algorithm}-{base64.b64encode(hashlib.new(algorithm, payload).digest()).decode('ascii')}"
        if computed != declared.group(1):
            raise BuildError(f"{relative} does not match the runtime's {constant} ({computed} != {declared.group(1)})")
        scripts.append(text)
    return scripts


def _embedded_string(value: str) -> str:
    """A JSON string literal safe inside an inline script element."""
    payload = json.dumps(value, ensure_ascii=False)
    for source, replacement in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"), ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        payload = payload.replace(source, replacement)
    return payload


def _component_registry(sources: dict[str, str]) -> str:
    entries = ",\n".join(
        f"  {_embedded_string('./' + _encode(name) + '.dc.html')}: new Blob([{_embedded_string(sources[name])}], {{ type: 'text/html' }})"
        for name in VIEWS
    )
    return "window.__resourceBlobs = Object.freeze({\n" + entries + "\n});\n"


def _encode(name: str) -> str:
    # encodeURIComponent for the characters that occur in view names.
    return name.replace(" ", "%20")


def _strip_remote_css(stylesheet: str) -> str:
    stripped, n = re.subn(r"@import\s+url\([^)]*\)\s*[^;]*;\s*", "", stylesheet)
    if n != 1:
        raise BuildError(f"expected exactly one remote @import in styles.css, found {n}")
    if "url(" in stripped or "@import" in stripped:
        raise BuildError("styles.css still references an external resource")
    return stripped.strip() + "\n"


def _token_style(overview: str) -> str:
    """The Overview's helmet token block, used as the document's base tokens."""
    match = re.search(r"<helmet>.*?<style>\s*(.*?)\s*</style>", overview, re.S)
    if not match or "--l-bg" not in match.group(1):
        raise BuildError("the Overview view declares no token style block")
    return match.group(1).strip() + "\n"


def build(patches: Sequence[Patch] = PATCHES) -> str:
    sources = {name: _read(f"{name}.dc.html") for name in VIEWS}
    runtime = _read("support.js")
    shell = _read("shell/shell.html")
    explorer = _read("shell/explorer.js")
    readiness_css = _read("shell/readiness.css")
    tokens = _token_style(sources["Overview"])
    stylesheet = _strip_remote_css(_read("styles.css"))
    for patch in patches:
        _apply(patch, sources)
    for name in VIEWS:
        text = sources[name]
        for forbidden in (".dc.html\"", ".dc.html'", "localStorage", "sessionStorage", "https://", "http://"):
            if forbidden in text:
                raise BuildError(f"{name} still contains {forbidden!r} after patching")
    if "https://" in explorer or "https://" in readiness_css or "http://" in explorer:
        raise BuildError("the shell must not reference a remote origin")
    vendored = _verify_vendored(runtime)
    # Two string literals in the vendored code spell "<script"; neutralize the
    # spelling so the document's script elements stay countable and a raw
    # "<script" never appears outside a real element.
    library = "\n;\n".join([*[item.rstrip() for item in vendored], runtime.rstrip()])
    if library.count("<script") != 2:
        raise BuildError(f"expected two '<script' string literals in the vendored runtime, found {library.count('<script')}")
    library = library.replace("<script", "\\x3cscript")
    # The runtime's CDN fallbacks (React, ReactDOM, Babel) are unreachable
    # because both React builds are inlined ahead of it; retire the origins so
    # the document names no remote location at all.
    if library.count('"https://unpkg.com/') != 3:
        raise BuildError(f"expected three unpkg fallback URLs in the runtime, found {library.count(chr(34) + 'https://unpkg.com/')}")
    library = library.replace('"https://unpkg.com/', '"about:blank#vendored/')
    runtime_block = "\n;\n".join([explorer.rstrip(), _component_registry(sources).rstrip(), library]) + "\n"
    for forbidden in ("localStorage", "sessionStorage", "unpkg.com", "googleapis.com"):
        if forbidden in runtime_block:
            raise BuildError(f"the runtime block still contains {forbidden!r}")
    literals = set(re.findall(r"https?://[^\"'` )]+", runtime_block))
    if not literals <= ALLOWED_URL_LITERALS:
        raise BuildError(f"the runtime block names an unexpected location: {sorted(literals - ALLOWED_URL_LITERALS)}")
    if shell.count(BOOTSTRAP_MARKER) != 1 or shell.count("__EXPLORER_RUNTIME__") != 1 or shell.count("__EXPLORER_STYLES__") != 1:
        raise BuildError("the shell must contain each marker exactly once")
    styles = stylesheet + tokens + readiness_css
    output = shell.replace("__EXPLORER_STYLES__", styles.rstrip()).replace("__EXPLORER_RUNTIME__", runtime_block.rstrip())
    if output.count(BOOTSTRAP_MARKER) != 1:
        raise BuildError("the built template must contain exactly one bootstrap marker")
    if output.count("<script") != 3:
        raise BuildError(f"the built template must contain exactly three script elements, found {output.count('<script')}")
    if "</script>" in runtime_block.replace("\\u003c/script", ""):
        raise BuildError("an embedded source would terminate the runtime script element")
    encoded = output.encode("utf-8")
    if len(encoded) > MAX_TEMPLATE_BYTES:
        raise BuildError(f"built template is {len(encoded)} bytes; the budget is {MAX_TEMPLATE_BYTES}")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail when the output differs from the current build")
    args = parser.parse_args(argv)
    try:
        built = build()
    except BuildError as exc:
        print(f"explorer template build failed: {exc}", file=sys.stderr)
        return 2
    if args.check:
        try:
            current = args.output.read_bytes()
        except OSError:
            print(f"{args.output} is missing", file=sys.stderr)
            return 1
        if current.replace(b"\r\n", b"\n") != built.encode("utf-8"):
            print(f"{args.output} differs from the build of its sources", file=sys.stderr)
            return 1
        print(f"{args.output} matches its sources ({len(current)} bytes)")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(built.encode("utf-8"))
    print(f"wrote {args.output} ({len(built.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

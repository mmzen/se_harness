/* Harness Explorer shell runtime.
 *
 * Owns everything the designed view components must not: reading the
 * embedded bootstrap, fetching and integrity-verifying manifest-declared
 * resources, flattening the verified summary and topology into the bundle
 * shape the views consume, query-string routing between views, in-memory
 * reader preferences, and the Readiness view. Repository text only ever
 * reaches the DOM through textContent or escaped interpolation here.
 */
(() => {
  "use strict";
  const BUNDLE_SCHEMA = "harness-dashboard-bundle-v2";
  const BOOTSTRAP_SCHEMA = "harness-dashboard-bootstrap-v2";
  const SUMMARY_SCHEMA = "harness-dashboard-summary-v2";
  const TOPOLOGY_SCHEMA = "harness-dashboard-topology-v2";
  const READINESS_SCHEMA = "harness-dashboard-readiness-v2";
  const ARTIFACT_SCHEMA = "harness-dashboard-artifact-v2";
  const EVIDENCE_SCHEMA = "utf8-markdown-v1";
  const VIEWS = Object.freeze(["overview", "lineage", "graph", "readiness"]);
  const CONTROLLED_PATH = /^(?:dashboard-manifest\.json|data\/(?:summary|topology|readiness|artifacts)\/[0-9a-f]{64}\.json|content\/[0-9a-f]{64}\.txt)$/;

  const array = value => (Array.isArray(value) ? value : []);
  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const label = value => String(value ?? "").replaceAll("_", " ").replace(/\b\w/g, c => c.toUpperCase());

  function readBootstrap() {
    const element = document.getElementById("harness-dashboard-bootstrap");
    if (!element) return null;
    try {
      const value = JSON.parse(element.textContent);
      if (value && typeof value === "object" && value.schema === BOOTSTRAP_SCHEMA && value.bundle_schema === BUNDLE_SCHEMA && value.manifest && typeof value.repository_revision === "string") return value;
    } catch (error) {
      return null;
    }
    return null;
  }
  const bootstrap = readBootstrap();

  // ---- verified resource access -------------------------------------------
  const verified = new Map();
  const inflight = new Map();
  async function digestHex(bytes) {
    const digest = await crypto.subtle.digest("SHA-256", bytes);
    return [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, "0")).join("");
  }
  function validDescriptor(descriptor) {
    return Boolean(descriptor) && typeof descriptor === "object" && CONTROLLED_PATH.test(String(descriptor.path)) && Number.isInteger(descriptor.bytes) && descriptor.bytes >= 0 && /^[0-9a-f]{64}$/.test(String(descriptor.sha256));
  }
  async function fetchBound(descriptor) {
    if (!validDescriptor(descriptor)) throw new Error("Resource descriptor is not controlled by the manifest.");
    const key = descriptor.path + "#" + descriptor.sha256;
    if (verified.has(key)) return verified.get(key);
    if (inflight.has(key)) return inflight.get(key);
    const request = (async () => {
      if (location.protocol === "file:") throw new Error("Serve this generated directory over HTTP; direct file opening cannot load progressive dashboard data.");
      if (!globalThis.crypto || !globalThis.crypto.subtle) throw new Error("Web Crypto is required to verify dashboard resources.");
      const response = await fetch(descriptor.path, { credentials: "same-origin", redirect: "error", cache: "no-cache" });
      if (!response.ok) throw new Error(`Resource request failed (${response.status}).`);
      if (new URL(response.url, location.href).origin !== location.origin) throw new Error("Resource origin differs from the page.");
      const bytes = new Uint8Array(await response.arrayBuffer());
      if (bytes.length !== descriptor.bytes) throw new Error("Resource size differs from its descriptor.");
      if ((await digestHex(bytes)) !== descriptor.sha256) throw new Error("Resource digest differs from its descriptor.");
      const text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
      let value;
      if (descriptor.schema === EVIDENCE_SCHEMA) {
        value = text;
      } else {
        value = JSON.parse(text);
        if (!value || typeof value !== "object" || (descriptor.schema && value.schema !== descriptor.schema)) throw new Error("Verified resource uses an unexpected schema.");
      }
      verified.set(key, value);
      return value;
    })();
    inflight.set(key, request);
    try {
      return await request;
    } finally {
      inflight.delete(key);
    }
  }

  let manifestPromise = null;
  function manifest() {
    if (manifestPromise) return manifestPromise;
    manifestPromise = (async () => {
      if (!bootstrap) throw new Error("Dashboard bootstrap is unsupported or incomplete.");
      const value = await fetchBound({ ...bootstrap.manifest, schema: BUNDLE_SCHEMA });
      if (!value.repository || value.repository.revision !== bootstrap.repository_revision) throw new Error("Manifest revision differs from the bootstrap.");
      for (const role of ["summary", "topology", "readiness"]) {
        const descriptor = value.entrypoints && value.entrypoints[role];
        if (!validDescriptor(descriptor) || descriptor.role !== role) throw new Error(`Manifest ${role} entrypoint is invalid.`);
      }
      return value;
    })().catch(error => {
      manifestPromise = null;
      throw error;
    });
    return manifestPromise;
  }
  async function entrypoint(role, schema) {
    const value = await manifest();
    const descriptor = value.entrypoints[role];
    if (descriptor.schema !== schema) throw new Error(`Manifest ${role} entrypoint schema differs.`);
    const resource = await fetchBound(descriptor);
    const revision = resource.repository_revision ?? (resource.repository && resource.repository.revision);
    if (revision !== bootstrap.repository_revision) throw new Error(`The ${role} resource revision differs from the manifest.`);
    return resource;
  }
  const summary = () => entrypoint("summary", SUMMARY_SCHEMA);
  const topology = () => entrypoint("topology", TOPOLOGY_SCHEMA);
  const readiness = () => entrypoint("readiness", READINESS_SCHEMA);

  // ---- the flattened bundle the designed views consume ---------------------
  let bundlePromise = null;
  let detailIndex = new Map();
  function bundle() {
    if (bundlePromise) return bundlePromise;
    bundlePromise = (async () => {
      const [summaryValue, topologyValue] = await Promise.all([summary(), topology()]);
      const artifacts = [];
      const distributions = {};
      const index = new Map();
      for (const row of array(topologyValue.artifacts)) {
        if (!row || typeof row !== "object" || typeof row.id !== "string" || !row.id) continue;
        if (validDescriptor(row.detail) && row.detail.schema === ARTIFACT_SCHEMA) index.set(row.id, row.detail);
        const flat = {
          id: row.id,
          type: typeof row.type === "string" ? row.type : null,
          status: typeof row.status === "string" ? row.status : null,
          title: typeof row.title === "string" ? row.title : null,
          owners: array(row.owners).filter(item => typeof item === "string"),
          authority: typeof row.authority === "string" ? row.authority : null,
          path: typeof row.path === "string" ? row.path : null,
        };
        if (typeof row.version === "string") flat.version = row.version;
        if (typeof row.released_at === "string") flat.released_at = row.released_at;
        if (row.distribution && typeof row.distribution === "object") distributions[row.id] = row.distribution;
        artifacts.push(flat);
      }
      const relations = array(topologyValue.relations).filter(item => item && typeof item === "object" && item.target_exists !== false);
      const repository = summaryValue.repository && typeof summaryValue.repository === "object" ? summaryValue.repository : {};
      detailIndex = index;
      return Object.freeze({
        schema: "harness-explorer-bundle-v1",
        data_root: "",
        source_url: typeof repository.source_url === "string" ? repository.source_url : "",
        repository_revision: bootstrap.repository_revision,
        repository,
        counts: summaryValue.counts || {},
        lifecycle_counts: summaryValue.lifecycle_counts || {},
        queue_counts: summaryValue.queue_counts || {},
        metrics: summaryValue.metrics && typeof summaryValue.metrics === "object" ? summaryValue.metrics : null,
        finding_rules_version: summaryValue.finding_rules_version ?? null,
        quality_gates_version: summaryValue.quality_gates_version ?? null,
        artifacts,
        relations,
        coverage: array(topologyValue.coverage),
        detail_ids: [...index.keys()].sort(),
        distributions,
      });
    })().catch(error => {
      bundlePromise = null;
      throw error;
    });
    return bundlePromise;
  }
  const unavailable = status => ({ ok: false, status, json: async () => null, text: async () => "" });
  function artifactResponse(id) {
    return bundle()
      .then(() => {
        const descriptor = detailIndex.get(String(id));
        if (!descriptor) return unavailable(404);
        return fetchBound(descriptor).then(value => {
          if (value.repository_revision !== bootstrap.repository_revision || !value.artifact || value.artifact.id !== id) throw new Error("Artifact detail identity differs from the topology.");
          return { ok: true, status: 200, json: async () => value, text: async () => JSON.stringify(value) };
        });
      })
      .catch(() => unavailable(0));
  }
  function evidenceResponse(rawPath) {
    return manifest()
      .then(value => {
        const descriptor = array(value.resources).find(item => item && item.path === rawPath && item.role === "evidence" && item.schema === EVIDENCE_SCHEMA);
        if (!descriptor) return unavailable(404);
        return fetchBound(descriptor).then(text => ({ ok: true, status: 200, text: async () => text, json: async () => null }));
      })
      .catch(() => unavailable(0));
  }

  // ---- routing and reader preferences ---------------------------------------
  function params() {
    return new URLSearchParams(location.search);
  }
  function view() {
    const query = params();
    const requested = query.get("view");
    if (VIEWS.includes(requested)) return requested;
    if (query.get("artifact")) return "lineage";
    return "overview";
  }
  const viewHref = () => location.pathname + "?view=" + view();
  const artifactHref = id => "?view=" + view() + "&artifact=" + encodeURIComponent(String(id));
  const prefs = (() => {
    const store = new Map();
    return Object.freeze({
      getItem: key => (store.has(key) ? store.get(key) : null),
      setItem: (key, value) => {
        store.set(key, String(value));
      },
      removeItem: key => {
        store.delete(key);
      },
    });
  })();

  // ---- Readiness view -------------------------------------------------------
  const NAV_LINKS = [
    ["overview", "Home"],
    ["lineage", "Lineage"],
    ["graph", "Virtual Twin"],
    ["readiness", "Readiness"],
  ];
  function navMarkup(current) {
    return `<nav aria-label="Views" class="hx-nav"><div class="hx-brand"><span class="hx-brand-mark"></span><span class="hx-brand-name">EXPLORER</span></div>${NAV_LINKS.map(([id, text]) => `<a href="?view=${id}"${id === current ? ' aria-current="page"' : ""} title="${esc(text)}">${esc(text)}</a>`).join("")}</nav>`;
  }
  function deriveSubjects(readinessValue, bundleValue) {
    const byId = new Map(bundleValue.artifacts.map(item => [item.id, item]));
    const findings = array(readinessValue.findings);
    return array(readinessValue.readiness).map(item => {
      const work = byId.get(item.work_order) || {};
      const gates = array(item.gates).map(gate => {
        const conditions = array(gate.conditions);
        const unsatisfied = conditions.filter(condition => condition.state === "unsatisfied").length;
        const unknown = conditions.filter(condition => condition.state === "not_assessable").length;
        return { ...gate, id: gate.gate, status: gate.state, detail: `${conditions.length} conditions · ${unsatisfied} unsatisfied · ${unknown} not assessable` };
      });
      const rows = gates.flatMap(gate => array(gate.conditions).map(condition => ({
        artifactId: array(condition.evidence)[0] || item.work_order,
        gate: gate.id,
        label: condition.label,
        reference: array(condition.evidence).join(", ") || "No retained evidence reference",
        status: condition.state,
        tone: condition.state === "satisfied" ? "clear" : condition.state === "unsatisfied" ? "blocked" : "review",
      })));
      const relatedFindings = findings.filter(finding => array(finding.artifacts).includes(item.work_order)).map(finding => ({ title: finding.rule, summary: finding.message, severity: finding.severity }));
      return {
        id: item.work_order,
        label: item.work_order,
        title: work.title || "",
        status: item.status,
        owner: array(work.owners).join(", ") || "Unassigned",
        gates,
        evidence: rows,
        findings: relatedFindings,
      };
    });
  }
  const gateState = gate => (gate.status === "unsatisfied" ? "unsatisfied" : gate.status === "not_assessable" ? "not_assessable" : "satisfied");
  function posture(subject) {
    let satisfied = 0, unsatisfied = 0, unknown = 0;
    array(subject.gates).forEach(gate => {
      if (gate.status === "unsatisfied") unsatisfied += 1;
      else if (gate.status === "not_assessable") unknown += 1;
      else satisfied += 1;
    });
    return { satisfied, unsatisfied, unknown, total: array(subject.gates).length };
  }
  function gateRollup(subjects) {
    const map = new Map();
    subjects.forEach(subject => array(subject.gates).forEach(gate => {
      if (!map.has(gate.id)) map.set(gate.id, { id: gate.id, label: gate.label, satisfied: 0, unsatisfied: 0, unknown: 0, total: 0 });
      const entry = map.get(gate.id);
      entry.total += 1;
      if (gate.status === "unsatisfied") entry.unsatisfied += 1;
      else if (gate.status === "not_assessable") entry.unknown += 1;
      else entry.satisfied += 1;
    }));
    return [...map.values()];
  }
  const segment = (count, name) => (count ? `<span class="${name}" style="flex:${count}"></span>` : "");
  const postureBar = (counts, text) => `<div class="hx-posture" role="img" aria-label="${esc(text)}">${segment(counts.satisfied, "is-satisfied")}${segment(counts.unsatisfied, "is-unsatisfied")}${segment(counts.unknown, "is-unknown")}</div>`;
  const artifactLink = id => `<a class="hx-ref" href="?view=lineage&amp;artifact=${encodeURIComponent(String(id))}">${esc(id)}</a>`;

  function renderReadiness(host) {
    if (!host || host.dataset.explorerReadiness === "mounted") return;
    host.dataset.explorerReadiness = "mounted";
    host.innerHTML = `<div class="hx-page">${navMarkup("readiness")}<main class="hx-main"><p class="hx-kicker">Assurance boundary</p><h1 class="hx-title">Readiness</h1><p class="hx-lead" id="hxReadinessLead">Loading readiness evidence…</p><div id="hxReadinessBody"></div></main></div>`;
    const lead = host.querySelector("#hxReadinessLead");
    const body = host.querySelector("#hxReadinessBody");
    const state = { subjects: [], provenance: [], experiments: [], findings: [], gate: null, gateState: "all", all: false, subject: null, filter: "all" };
    const query = params();
    if (query.get("subject")) state.subject = query.get("subject");
    if (query.get("gate")) {
      state.gate = query.get("gate");
      state.gateState = query.get("state") || "all";
    }
    if (query.get("all") === "1") state.all = true;

    function syncRoute() {
      const next = new URLSearchParams({ view: "readiness" });
      if (state.subject) next.set("subject", state.subject);
      else if (state.all) next.set("all", "1");
      else if (state.gate) {
        next.set("gate", state.gate);
        next.set("state", state.gateState);
      }
      try {
        history.replaceState(null, "", location.pathname + "?" + next.toString());
      } catch (error) {
        /* history is a convenience, never state */
      }
    }
    function matches(subject) {
      if (state.all) return true;
      if (!state.gate) return false;
      const gate = array(subject.gates).find(item => item.id === state.gate);
      return Boolean(gate) && (state.gateState === "all" || gateState(gate) === state.gateState);
    }
    function selectionText() {
      if (state.all) return `All ${state.subjects.length} readiness subjects`;
      if (!state.gate) return null;
      const gate = array(state.subjects[0] && state.subjects[0].gates).find(item => item.id === state.gate);
      return `${state.gate} ${gate ? gate.label : ""} · ${state.gateState === "all" ? "every recorded state" : label(state.gateState)}`;
    }
    function indexMarkup() {
      const subjects = state.subjects;
      const selection = selectionText();
      const rows = selection ? subjects.filter(matches) : [];
      const rollup = gateRollup(subjects);
      const active = (gate, gateStateName) => String(Boolean(state.gate === gate.id && state.gateState === gateStateName && !state.all));
      const figure = (gate, count, gateStateName, text) => (count ? `<button type="button" class="hx-gate-state" data-gate="${esc(gate.id)}" data-gate-state="${gateStateName}" aria-pressed="${active(gate, gateStateName)}">${count} ${esc(text)}</button>` : "");
      const gateFigures = rollup.map(gate => {
        const parts = [];
        if (gate.satisfied) parts.push(`${gate.satisfied} satisfied`);
        if (gate.unsatisfied) parts.push(`${gate.unsatisfied} unsatisfied`);
        if (gate.unknown) parts.push(`${gate.unknown} not assessable`);
        return `<div class="hx-gate-figure" data-gate-active="${active(gate, "all")}"><span class="hx-gate-code">${esc(gate.id)}</span><strong>${esc(gate.label)}</strong><button type="button" class="hx-gate-total" data-gate="${esc(gate.id)}" data-gate-state="all" aria-pressed="${active(gate, "all")}">${gate.satisfied} / ${gate.total}</button>${postureBar(gate, parts.join(" · "))}<div class="hx-gate-states">${figure(gate, gate.satisfied, "satisfied", "satisfied")}${figure(gate, gate.unsatisfied, "unsatisfied", "unsatisfied")}${figure(gate, gate.unknown, "not_assessable", "not assessable")}</div></div>`;
      }).join("") || '<div class="hx-gate-figure"><small>No gate is recorded for the listed subjects.</small></div>';
      const table = rows.map(subject => {
        const counts = posture(subject);
        const detail = [`${counts.satisfied} of ${counts.total} gates satisfied`];
        if (counts.unsatisfied) detail.push(`${counts.unsatisfied} unsatisfied`);
        if (counts.unknown) detail.push(`${counts.unknown} not assessable`);
        return `<tr><td><button type="button" class="hx-link" data-subject="${esc(subject.id)}">${esc(subject.id)}</button><br><small>${esc(subject.title)}</small></td><td><span class="hx-badge">${esc(label(subject.status))}</span></td><td>${postureBar(counts, detail.join(" · "))}<small>${esc(detail.join(" · "))}</small></td><td>${esc(subject.owner)}</td></tr>`;
      }).join("") || '<tr><td colspan="4">No readiness subject carries this gate posture.</td></tr>';
      return `<section class="hx-panel" aria-labelledby="hxIndexTitle"><div class="hx-head"><h2 id="hxIndexTitle">Readiness subjects</h2><span>${selection ? `${rows.length} OF ${subjects.length} SUBJECTS` : `${subjects.length} SUBJECTS`}</span></div><p class="hx-note">Recorded G0-G5 gate states across every readiness subject. Choose a figure to list the subjects it describes. Gate posture restates recorded states; it infers no approval, verification, or release decision.</p><div class="hx-gate-summary" aria-label="Recorded gate states across the listed subjects">${gateFigures}</div><div class="hx-selection">${selection ? `<strong>${esc(selection)}</strong><button type="button" class="hx-link" data-clear="1">Clear selection</button>` : `<span>No gate figure selected.</span><button type="button" class="hx-link" data-all="1">List all ${subjects.length} subjects →</button>`}</div><table class="hx-table"><thead><tr><th>Work order</th><th>Status</th><th>Gate posture</th><th>Accountable owners</th></tr></thead><tbody>${table}</tbody></table></section>`;
    }
    function subjectMarkup(subject) {
      const gates = array(subject.gates).map(gate => `<div class="hx-gate ${gate.status === "unsatisfied" ? "blocked" : gate.status === "not_assessable" ? "review" : ""}"><span class="hx-gate-code">${esc(gate.id)}</span><strong>${esc(gate.label)}</strong><span>${esc(gate.detail)}</span></div>`).join("");
      const rows = (state.filter === "all" ? subject.evidence : subject.evidence.filter(item => item.tone === state.filter));
      const evidence = rows.map(row => `<tr><td>${artifactLink(row.artifactId)}<br><small>${esc(row.label)}</small></td><td class="hx-mono">${esc(row.reference)}</td><td class="hx-mono">${esc(row.gate)}</td><td><span class="hx-badge hx-evidence ${esc(row.tone)}">${esc(label(row.status))}</span></td></tr>`).join("") || '<tr><td colspan="4">No retained evidence row carries this observed state.</td></tr>';
      const findings = subject.findings.map(finding => `<div class="hx-finding"><strong>${esc(finding.title)}</strong><span class="hx-badge ${["warning", "error", "blocking"].includes(finding.severity) ? "warning" : ""}">${esc(label(finding.severity))}</span><p>${esc(finding.summary)}</p></div>`).join("") || `<p>No explicit finding names ${esc(subject.id)}.</p>`;
      const filters = [["all", "All"], ["clear", "Satisfied"], ["blocked", "Unsatisfied"], ["review", "Not assessable"]].map(([id, text]) => `<button type="button" data-filter="${id}" aria-pressed="${String(state.filter === id)}">${text}</button>`).join("");
      return `<div class="hx-back"><button type="button" class="hx-link" data-back="1">← All readiness subjects</button></div><section class="hx-panel" aria-labelledby="hxSubjectTitle"><div class="hx-head"><div><p class="hx-kicker">Assurance subject</p><h2 id="hxSubjectTitle">${artifactLink(subject.id)} <span class="hx-badge">${esc(label(subject.status))}</span></h2><p class="hx-note">${esc(subject.title)}</p></div><label class="hx-select">Change subject<select data-subject-select="1">${state.subjects.map(item => `<option value="${esc(item.id)}"${item.id === subject.id ? " selected" : ""}>${esc(item.id)}</option>`).join("")}</select></label></div><dl class="hx-grid"><div><dt>Accountable owners</dt><dd>${esc(subject.owner)}</dd></div><div><dt>Assessed revision</dt><dd class="hx-mono">${esc(bootstrap ? bootstrap.repository_revision : "unavailable")}</dd></div><div><dt>Decision boundary</dt><dd>Gate states are derived observations; approval, verification, and release remain explicit human decisions.</dd></div></dl></section><section class="hx-panel"><div class="hx-head"><h2>Explorer gate groupings</h2><span class="hx-badge warning">NAVIGATION LABELS · NOT POLICY</span></div><div class="hx-gates">${gates}</div><p class="hx-note">Managed <code>QUALITY_GATES.md</code> owns gate meaning. These groupings order the evidence below; they restate no policy and grant no authority.</p></section><div class="hx-two"><section class="hx-panel"><div class="hx-head"><h2>Quality-gate evidence</h2><span>${state.filter === "all" ? `${subject.evidence.length} RECORDS` : `${rows.length} OF ${subject.evidence.length} RECORDS`}</span></div><div class="hx-filters" role="group" aria-label="Filter retained evidence rows by observed state">${filters}</div><table class="hx-table"><thead><tr><th>Artifact</th><th>Retained evidence</th><th>Gate</th><th>State</th></tr></thead><tbody>${evidence}</tbody></table></section><aside class="hx-panel"><div class="hx-head"><h2>Consistency</h2><span>THIS SUBJECT · EXPLICIT RECORDS</span></div>${findings}</aside></div>`;
    }
    function canonicalMarkup() {
      const provenance = state.provenance.map(item => `<article class="hx-record"><strong>${artifactLink(item.id)} · ${esc(item.kind)} · ${esc(item.status)}</strong><small class="hx-mono">commit ${esc(item.commit)} · ${esc(item.git_object_format)} · checkout ${esc(item.match_state)}</small><small>work orders: ${array(item.work_orders).map(artifactLink).join(", ") || "none"}${array(item.superseded_by).length ? ` · superseded by ${array(item.superseded_by).map(artifactLink).join(", ")}` : ""}</small>${item.supersession_authorized_by ? `<small>Supersession authorized by ${esc(item.supersession_authorized_by)}${item.superseded_at ? ` · ${esc(item.superseded_at)}` : ""}</small>` : ""}</article>`).join("") || "<p>No commit-bound verification or release record is retained.</p>";
      const experiments = state.experiments.map(item => `<article class="hx-record"><strong>${esc(item.id || item.trial || "Controlled observation")}</strong><small>${esc(item.summary || item.result || "See the retained experiment fields for this observation.")}</small></article>`).join("") || "<p>No controlled experiment is retained; effectiveness is not measured.</p>";
      const findings = state.findings.map(item => `<article class="hx-record"><strong>${esc(item.rule)} <span class="hx-badge ${["warning", "error", "blocking"].includes(item.severity) ? "warning" : ""}">${esc(label(item.severity))}</span></strong><small>${esc(item.message)}</small><small>${array(item.artifacts).map(artifactLink).join(", ")}</small></article>`).join("") || "<p>The evaluator recorded no finding for this revision.</p>";
      return `<div class="hx-two"><section class="hx-panel"><div class="hx-head"><h2>Commit-bound provenance</h2><span>VREC + RELEASE RECORDS</span></div><div class="hx-records">${provenance}</div></section><section class="hx-panel"><div class="hx-head"><h2>Findings</h2><span>${state.findings.length} RECORDED</span></div><div class="hx-records">${findings}</div></section></div><section class="hx-panel"><div class="hx-head"><h2>Controlled outcomes</h2><span>OBSERVATION, NOT AUTHORITY</span></div><div class="hx-records">${experiments}</div></section>`;
    }
    function render() {
      const subject = state.subject ? state.subjects.find(item => item.id === state.subject) : null;
      if (state.subject && !subject) state.subject = null;
      body.innerHTML = (subject ? subjectMarkup(subject) : indexMarkup()) + canonicalMarkup();
      lead.textContent = subject ? `${subject.id} is ${label(subject.status).toLowerCase()}. Gate states below are derived observations.` : `${state.subjects.length} readiness subjects · ${state.provenance.length} commit-bound records · ${state.findings.length} findings. No approval, verification, or release decision is inferred here.`;
      syncRoute();
    }
    body.addEventListener("click", event => {
      const target = event.target.closest("button");
      if (!target) return;
      if (target.dataset.gate) {
        state.all = false;
        state.subject = null;
        if (state.gate === target.dataset.gate && state.gateState === target.dataset.gateState) state.gate = null;
        else {
          state.gate = target.dataset.gate;
          state.gateState = target.dataset.gateState;
        }
      } else if (target.dataset.all) {
        state.all = true;
        state.gate = null;
      } else if (target.dataset.clear) {
        state.all = false;
        state.gate = null;
      } else if (target.dataset.subject) {
        state.subject = target.dataset.subject;
        state.filter = "all";
      } else if (target.dataset.back) {
        state.subject = null;
      } else if (target.dataset.filter) {
        state.filter = target.dataset.filter;
      } else return;
      render();
      body.scrollIntoView({ block: "start" });
    });
    body.addEventListener("change", event => {
      const target = event.target;
      if (target && target.dataset && target.dataset.subjectSelect) {
        state.subject = target.value;
        state.filter = "all";
        render();
      }
    });
    Promise.all([readiness(), bundle()])
      .then(([readinessValue, bundleValue]) => {
        state.subjects = deriveSubjects(readinessValue, bundleValue);
        state.provenance = array(readinessValue.revision_provenance);
        state.experiments = array(readinessValue.experiments);
        state.findings = array(readinessValue.findings);
        render();
      })
      .catch(error => {
        lead.textContent = "Readiness data is unavailable.";
        body.innerHTML = `<section class="hx-panel"><p class="hx-note">${esc(error && error.message ? error.message : "The readiness resource could not be verified.")}</p><button type="button" class="hx-link" data-retry="1">Retry verified load</button></section>`;
        body.querySelector("[data-retry]").addEventListener("click", () => {
          host.dataset.explorerReadiness = "";
          renderReadiness(host);
        });
      });
  }

  // ---- shell failure surface ----------------------------------------------
  function showFailure(message) {
    const surface = document.getElementById("harness-explorer-fallback");
    if (!surface) return;
    surface.hidden = false;
    surface.querySelector("[data-message]").textContent = message;
  }
  if (!bootstrap) showFailure("Dashboard bootstrap is unsupported or incomplete. Regenerate this bundle with harnessctl dashboard.");
  else if (location.protocol === "file:") showFailure("Serve this generated directory over HTTP; direct file opening cannot load progressive dashboard data.");
  else manifest().catch(error => showFailure(error && error.message ? error.message : "The dashboard manifest could not be verified."));

  window.HarnessExplorer = Object.freeze({
    bootstrap,
    manifest,
    summary,
    topology,
    readiness,
    bundle,
    artifactResponse,
    evidenceResponse,
    view,
    viewHref,
    artifactHref,
    prefs,
    renderReadiness,
    views: VIEWS,
  });
  // The component runtime refetches the page to refresh its raw template
  // unless a resource map exists; the embedded sources are the only sources.
  window.__resources = window.__resources || {};
})();

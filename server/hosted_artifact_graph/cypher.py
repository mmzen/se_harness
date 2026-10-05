"""A parsed, deliberately small Cypher read subset. Not database authorization."""
from __future__ import annotations

import json
from dataclasses import dataclass

from lark import Lark, Token, Tree, UnexpectedInput

from .protocol import Refusal, require

GRAMMAR = r"""
start: match pattern where? "RETURN"i returns "LIMIT"i INT
match: "MATCH"i -> required
     | "OPTIONAL"i "MATCH"i -> optional
pattern: node (edge node)*
node: "(" NAME ":" NAME ")"
edge: "-" "[" NAME ":" NAME length? "]" "->" -> forward
    | "<-" "[" NAME ":" NAME length? "]" "-" -> backward
length: "*" INT ".." INT
where: "WHERE"i condition
?condition: comparison ("AND"i comparison)*
comparison: property OP value
property: NAME "." NAME
?value: PARAM -> parameter
      | STRING -> string
      | SIGNED_INT -> number
returns: returned ("," returned)*
returned: property alias? | NAME alias?
alias: "AS"i NAME
OP: "=" | "<>" | "<=" | ">=" | "<" | ">"
PARAM: /\$[A-Za-z][A-Za-z0-9_]*/
NAME: /[A-Za-z][A-Za-z0-9_]*/
STRING: /'(?:[^'\\\r\n]|\\['\\])*'/ | /"(?:[^"\\\r\n]|\\["\\])*"/
%import common.INT
%import common.SIGNED_INT
%import common.WS
%ignore WS
%ignore /\/\/[^\r\n]*/
%ignore /(?s:\/\*.*?\*\/)/
"""
PARSER = Lark(GRAMMAR, parser="lalr")
PROPERTIES = {
    "Project": {"project_id", "schema_revision", "command_version"},
    "Artifact": {"project_id", "artifact_id"},
    "Revision": {"project_id", "artifact_id", "revision_id", "type", "status", "document_sha256", "envelope_json", "document_base64"},
    "Baseline": {"project_id", "baseline_id", "manifest_json"},
    "DraftContext": {"project_id", "context_id", "base_baseline_id", "work_order_id", "context_version"},
    "HAS_REVISION": set(), "SELECTS": set(), "BASED_ON": set(),
    "PROPOSES": {"artifact_id"}, "DECLARES": {"kind", "target_artifact_id"},
}
NODE_LABELS = {"Project", "Artifact", "Revision", "Baseline", "DraftContext"}
EDGE_KINDS = set(PROPERTIES) - NODE_LABELS


@dataclass
class Query:
    cypher: str
    parameters: dict
    columns: list[str]
    returned_labels: list[str | None]
    limit: int


def compile_query(query, parameters, snapshot, budget, project_id):
    try:
        ast = PARSER.parse(query)
    except UnexpectedInput as exc:
        raise Refusal(400, "QUERY_SYNTAX", "Unsupported or ambiguous Cypher read syntax.") from exc
    require(all(not k.startswith("__") for k in parameters), 400, "QUERY_SYNTAX", "Reserved query parameter.")
    match, pattern = ast.children[:2]
    limit = int(ast.children[-1])
    require(1 <= limit <= 500, 429, "RESOURCE_LIMIT", "Cypher LIMIT must be between 1 and 500.")
    labels, pieces, lengths = {}, [], {}
    for item in pattern.children:
        variable, label = map(str, item.children[:2])
        require(variable not in labels and not variable.startswith("__"), 400,
                "QUERY_SYNTAX", "Variables must be distinct public identifiers.")
        allowed = NODE_LABELS if item.data == "node" else EDGE_KINDS
        require(label in allowed, 400, "QUERY_SYNTAX", "Unknown public label or relationship.")
        labels[variable] = label
        if item.data == "node":
            pieces.append(f"({variable}:{label})")
        else:
            depth = ""
            if len(item.children) == 3:
                lower, upper = map(int, item.children[2].children)
                require(1 <= lower <= upper <= budget["depth"] <= 8, 429, "RESOURCE_LIMIT", "Cypher path exceeds the declared depth budget.")
                depth = f"*{lower}..{upper}"
                lengths[variable] = True
            require(budget["depth"] >= 1, 429, "RESOURCE_LIMIT", "Cypher relationship exceeds depth zero.")
            left, right = ("-", "->") if item.data == "forward" else ("<-", "-")
            pieces.append(f"{left}[{variable}:{label}{depth}]{right}")

    def prop(tree):
        var, field = map(str, tree.children)
        require(var in labels and var not in lengths and field in PROPERTIES[labels[var]],
                400, "QUERY_SYNTAX", "Unknown public property or unsupported path property.")
        return var + "." + field

    args = dict(parameters)
    filters = []
    # Every traversed node and edge is confined to the selected immutable revision set.
    membership = (
        "n.project_id=$__project AND ((n:Project) OR (n:Artifact AND n.artifact_id IN $__artifacts) "
        "OR (n:Revision AND n.revision_id IN $__revisions) OR (n:Baseline AND n.baseline_id=$__baseline) "
        "OR (n:DraftContext AND n.context_id=$__context))")
    filters.append("all(n IN nodes(__path) WHERE " + membership + ")")
    filters.append("all(e IN relationships(__path) WHERE type(e) IN $__edges)")
    args.update(__project=project_id, __artifacts=sorted(snapshot["revisions"]),
                __revisions=[r["revision_id"] for r in snapshot["revisions"].values()],
                __baseline=snapshot["baseline"]["baseline_id"],
                __context=snapshot["context"]["context_id"] if snapshot["context"] else "",
                __edges=sorted(EDGE_KINDS))
    where = next((c for c in ast.children if isinstance(c, Tree) and c.data == "where"), None)
    if where:
        for comparison in where.find_data("comparison"):
            field, operator, value = comparison.children
            if value.data == "parameter":
                name = str(value.children[0])[1:]
                require(name in parameters and type(parameters[name]) in (str, int, bool, type(None)),
                        400, "QUERY_SYNTAX", "A scalar query parameter is missing.")
            else:
                name = "__literal" + str(len(args))
                if value.data == "number":
                    args[name] = int(value.children[0])
                else:
                    literal = str(value.children[0])
                    args[name] = literal[1:-1].replace("\\" + literal[0], literal[0]).replace("\\\\", "\\")
            filters.append(f"({prop(field)} {operator} ${name})")
    returned = next(c for c in ast.children if isinstance(c, Tree) and c.data == "returns")
    output, columns, result_labels = [], [], []
    for item in returned.children:
        value = item.children[0]
        if isinstance(value, Tree):
            expression, label = prop(value), None
        else:
            expression = str(value)
            require(expression in labels and expression not in lengths, 400, "QUERY_SYNTAX", "Unknown returned variable.")
            label = labels[expression]
        column = str(item.children[1].children[0]) if len(item.children) == 2 else expression
        require(column not in columns, 400, "QUERY_SYNTAX", "Duplicate returned column.")
        columns.append(column)
        result_labels.append(label)
        output.append(expression + " AS __column" + str(len(output)))
    selected_limit = min(limit, budget["rows"])
    # Fetch one additional row only when the caller's row budget is below its requested LIMIT.
    fetch = selected_limit + (1 if selected_limit < limit else 0)
    compiled = ("OPTIONAL MATCH " if match.data == "optional" else "MATCH ") + "__path=" + "".join(pieces)
    compiled += " WHERE " + " AND ".join(filters) + " RETURN " + ", ".join(output) + " LIMIT " + str(fetch)
    return Query(compiled, args, columns, result_labels, selected_limit)


def public_rows(records, query):
    result = []
    for record in records:
        row = []
        for i, label in enumerate(query.returned_labels):
            value = record[i]
            if label and value is not None:
                value = {k: v for k, v in dict(value).items() if k in PROPERTIES[label]}
            row.append(value)
        result.append(row)
    return result

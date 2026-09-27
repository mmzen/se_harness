# Communication

## Purpose and claim

This policy controls eligible English prose written by agents for operators and
technical artifacts. It uses selected clarity principles based on ASD-STE100.
It is not ASD-STE100 compliance, certification, approval, or endorsement.

An agent MUST NOT download, search for, bundle, reproduce, parse, or attempt to
strictly implement ASD-STE100 or a controlled dictionary. The installed policy
is complete for its declared purpose.

## Eligible prose

Eligible prose is agent-authored English explanation that is not protected
content (see next section). For eligible prose, the agent SHOULD:

- use one stable term for one concept;
- define an uncommon project term before relying on it;
- identify the responsible actor when responsibility matters;
- state conditions, actions, and results directly;
- prefer active voice when it identifies responsibility;
- keep each sentence focused on one principal action;
- avoid ambiguous pronouns, decorative synonyms, hidden negation, vague
  references, and unnecessary introductions; and
- use a list or table when it clarifies parallel conditions, mappings, or
  ordered steps.

Sentence length is a review signal. It is not a conformance threshold and does
not justify removing necessary technical detail.

## Protected content

Exact protected content MUST remain byte-identical. It includes:

- code and inline code;
- commands, paths, identifiers, hashes, version strings, URLs, schemas, and
  field names;
- JSON, TOML, YAML, XML, and other machine-readable data;
- logs, diagnostics, evidence, evaluator output, and canonical restitution
  blocks;
- quotations; and
- operator-supplied text that is presented as supplied text.

Protected content MUST NOT be automatically paraphrased. It includes BCP 14 obligations, 
requirement statements, lifecycle and decision meanings, safety or legal qualifications, 
acceptance thresholds, formulas, and established terminology.

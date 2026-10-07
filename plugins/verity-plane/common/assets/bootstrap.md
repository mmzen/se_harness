# Select the working repository

First use the target already selected by the operator.

## Explicit hosted sandbox

If the operator selected a hosted sandbox, use the setup skill's "Hosted sandbox
selection" procedure. Retain its endpoint, project and versioned context. Leave
any existing checkout selection unchanged. This route does not activate or clear
a checkout, install a repository harness, or switch real authority to the graph.
After checking the hosted selection, follow harness-orient for reads or change
for authorized sandbox work. Do not continue into checkout activation.

## Local checkout

Use this route for work in a cloned or existing repository.

When asked to clone, clone to the intended destination, then activate that exact
checkout. For existing work, reuse the known checkout path. Ask for a path only
when the intended repository is ambiguous. Do not scan child repositories.

Use the setup skill's activation procedure with the host, session_id and
plugin data supplied with this message. It immediately returns
the selected instructions. Read that complete entry before governed work. If the
repository has no harness selection or its evaluator is missing, use the setup
skill with an explicitly selected release, then activate again. Do not choose a
release or upgrade silently.

Selection belongs only to this host session. A new session activates its own
checkout. Switching or clearing affects only this session. Activation gives no
approval, verification or delivery authority; follow the selected release for
new or resumed work and any requested push or pull request.

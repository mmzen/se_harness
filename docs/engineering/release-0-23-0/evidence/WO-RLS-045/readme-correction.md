# README length correction

CI at 321fe678d982505d55d8531c6ca63fee6b606275 ran 1,339 tests with two skips.
Its only source-suite failure was the root README: 729 words exceeded the
existing 650-word limit. This correction is within WO-RLS-045's named README
scope. It shortens the overview and release summary while retaining installation
commands, public evidence links, authority rules and the private-sandbox boundary.

The first edit still contained 660 words and failed; the final edit contains
644 words. All 34 affected public-onboarding and progressive-documentation tests
passed. [Exact CI and local results](readme-correction-checks.zip) preserve both
failures. The final complete suite must pass in CI; these focused results do not
establish that pass. The separately observed package-map failure and pending
WO-RLS-048 approval are unchanged. No new authority or test-limit change was needed.

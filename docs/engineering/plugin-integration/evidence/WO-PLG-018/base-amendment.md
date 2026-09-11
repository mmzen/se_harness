# WO-PLG-018: proposed main-baseline amendment

**Approved on 2026-09-11.** The [decision receipt](base-amendment-approval.json)
records the operator approval for both artifacts and the exact plan below.
The WO and VER carry the dated amendment; lifecycle metadata is unchanged.
Implementation follows through the delegated route after its gates pass.

## What changed

You merged PR #450 at `fc1f087371b100d5fda7a1f254ee00ebde8cbadf`. Main now contains WO-PLG-018's
approved execution delegation, satisfying the prerequisite that blocked start.
The original plan pinned the older main commit `c0451b7694b02f140f95661b07907d4722b336cd`.
Its stop condition requires a reviewed amendment when that base changes.

## The exact amendment to approve

Use [plan-main.json](plan-main.json), SHA-256
`eb0fa0a8e8e5e77428f45fdcde3c99f2080c318bdcb75a6425216081002feefb`, as the execution plan for WO-PLG-018 and the independently
pinned verification input for VER-PLG-018. Keep [plan.json](plan.json), its original
SHA-256 `68b59c5837e890396701e46f5e37cc391a3ebf91d9f71c736d27e50345155aaa`, and all earlier approvals as history.

| Item | Original plan | Proposed amendment |
| --- | --- | --- |
| Main baseline | `c0451b76` | `fc1f0873` (PR #450 merge; full identity above) |
| Delivery | Assemble in PR #450 | New PR from `work/plugin-stack-integration`; this proposal's PR later carries implementation |
| Expected combined tree | `f592089dc2e14822faea475af200dc89f9f04648` | `dbc52b56a3820c8765aec2aa5de250c3e1d7a379` |
| Preview archive entries | 9,955 before the approval packet | 9,963 including the merged approval packet |

All **3,177 imported paths**, modes, blob IDs, five source heads, allowed paths,
original VREC expectations and acceptance cases are identical to the approved
plan. The new tree includes the already-merged approval packet. Both merge
previews are conflict-free. These observations are retained in
[base-amendment-review.json](base-amendment-review.json).

On approval, append a dated amendment to WO-PLG-018 that selects this plan and
base. Update its original instruction to keep the packet on this new PR's branch,
then merge the pinned #446 head followed by the pinned #444 head after start.
Append the same independent plan digest to VER-PLG-018 for INT01–INT06.
Retain existing lifecycle events; neither artifact needs a fabricated reapproval
transition. Record the operator's exact amendment decision separately.

## What happens next

After the amendment is approved and recorded, publish that commit and require
its actual `validate` success. The released evaluator then decides whether
delegated start is legal. The same PR can carry the authorized assembly and checks.
Completion and ready VREC-PLG-011 preparation use the existing delegated route;
the operator still decides verification and the final merge.

The three new proposal files bring the prospective combined tree to **9,966
archive entries**, leaving **34** for the checker, tests, later evidence,
and governance. The final actual tree must stay at or below 10,000. This proposal
does not raise the limit, rewrite old evidence, or claim completed acceptance.

**Suggested decision:** “I approve the baseline amendment to WO-PLG-018 and
VER-PLG-018 in this PR, with the proposed plan digest above and the existing
execution delegation.”

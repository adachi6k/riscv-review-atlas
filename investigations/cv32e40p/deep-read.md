# CV32E40P: decisions from five retrieval groups

Date: 2026-09-29. Investigation [#3](https://github.com/adachi6k/riscv-review-atlas/issues/3).

## Outcome

Five selected groups contain six focused historical cases. Group #897 splits into two different mechanisms; #195 and #888 combine into one cancellation property. The result is **five source-reviewed candidate entries**, classified as **four new candidates relative to the 24 public Ibex entries and one extension**. This is not five new bug discoveries, a comprehensive project audit, or an independent reproduction.

| Retrieval group | Decision | Checklist entry |
|---|---|---|
| #195 | Combine interrupt-side cancellation evidence with #888; extend the existing execution-boundary theme | CV32E40P-001 |
| #880 / #881 | New hardware-loop zero-count property | CV32E40P-002 |
| #888 / #889 / #897 | Split cancellation from JALR/writeback contention; combine only the former with #195 | CV32E40P-001, CV32E40P-003 |
| #730 / #841 | New custom-source dependency completeness property | CV32E40P-004 |
| #723 / #824 / #860 | New split-address ownership property; retain superseded-fix lineage | CV32E40P-005 |

Read the [checklist](checklist.md) or its [structured form](checklist.json) for applicability, proposed stimulus, independent oracle, exact source revisions and limitations. “New” means absent as a specific property in this bounded Ibex checklist, not novel to verification practice. Related properties are not evidence of common patches or identical root causes.

## Why the final fix history matters

[#824](https://github.com/openhwfoundation/cv32e40p/pull/824) initially filters misaligned LSU requests while the APU is busy. [#860](https://github.com/openhwfoundation/cv32e40p/pull/860) explicitly removes that approach and replaces it with APU result/flag buffering and acceptance gating during conflicting execution phases. [#723's closure](https://github.com/openhwfoundation/cv32e40p/issues/723#issuecomment-1752556941) names #860.

Using #824 alone as a final repair template would lose this distinction. Nor is #860 the end of every shared-result arbitration change: #881 narrows some conditions and #897 adds the JALR-related case. These later edits do not, by themselves, prove the #723 defect persisted. The checklist states an invariant rather than prescribing any one historical gate.

## Evidence and review boundary

Codex reviewed cached issue bodies and available conversations, PR descriptions, review/inline discussion, and relevant final RTL diffs for PRs #195, #881, #897, #841, #824 and #860. Revision identifiers and diff hashes are recorded per entry; acquisition hashes remain in [sources.json](sources.json). PR base/head and merge revisions are not automatically known failing/passing test revisions.

The selected reports provide useful but unequal evidence:

- #880 and #889 contain ISS mismatch reports and randomized-test replay commands with verification revisions/seeds.
- #888, #730 and #723 attribute traces to OneSpin; their attachments were not inspected or rerun.
- #730 has no reported affected SHA. Its discussion distinguishes an earlier apparent fix from ongoing verification and later resolution via #841.
- #195 describes architectural-state consistency for verification and explicitly does not establish harmful functional behavior. It must not be presented as an independently confirmed functional failure.

No regression source in core-v-verif was retrieved in this pass, no historical checkout was simulated, and no new formal run was performed. The proposed stimuli/oracles are investigation outputs, not completed verification. A merged PR or closure comment is fix-linked evidence, not a reproduced result or a proof about current HEAD.

## Deferred scope

No selected property is wholly deferred: each has enough evidence for a bounded source-reviewed candidate. Stronger validation remains deferred for all five. The other four retrieval groups (#1064, #975, #466, #920) remain unadjudicated; they are not rejected or declared clean.

Do not count unrelated changes bundled into selected PRs as reviewed checklist entries. Excluded here are #881's other corrections (#731/#742/#869/#870/#876/#877), #897's #887/#896 and floating-state details, #841's #838/#840 and implementation-ID discussion, #824's #170/CSR changes, and #860's other issue fixes/vendor FPU updates. Some shared arbitration hunks inform context, but those other defect reports were not independently adjudicated. Attachments, recursive references, intermediate PR diffs, exact downstream gate-cone proofs and comprehensive cross-core ancestry remain open work.

## Practical next step

First map the five properties to a target's implemented mechanisms. Hardware loops, Zfinx, custom arithmetic, shared FP writeback and split misaligned accesses are explicit applicability conditions; an absent feature is not a missing test.

For an applicable target, choose one property and construct a minimal directed test with an independent oracle plus a negative control. Record the target SHA, configuration and reachable overlap. For historical validation, prefer a reported affected SHA and verify the later fix rather than assuming a PR base fails. CV32E40P-002 has a focused correction and a supplied replay recipe; it is a useful first reproduction candidate if the required environment is available. CV32E40P-004 needs the missing failing-revision question resolved before an exact historical replay claim.

## Cost boundary

This deep-read pass used the existing cached corpus and **made no additional Jev requests**. The earlier triage used 53 successful inputs, 556,338 input tokens and 29,146 output tokens; those numbers remain unchanged in [usage.json](usage.json). They are Jev API usage, not total Codex token consumption or billed cost. Bounded reading avoids claiming that the entire 1,052-record index has been adjudicated. For the next pass, retrieve only missing evidence for the chosen property and reuse existing payload-hash caches.

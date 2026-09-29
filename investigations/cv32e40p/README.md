# CV32E40P: bounded next-core investigation

Snapshot: 2026-09-29. Research task [#3](https://github.com/adachi6k/riscv-review-atlas/issues/3). Public master: `6033d2b1be3295ec774d17ac4cf226faacfdeb08`.

## Scope and selection

The current REST index contains 1,052 issue/PR records: 504 issues and 548 PRs. This index was collected in full; full evidence was collected only for the bounded seed set described below. Counts include requests, questions and maintenance, not just defects.

CV32E40P follows the existing roadmap after Ibex, focusing on pipeline/LSU interactions, hardware loops and multi-cycle FPU/custom-instruction hazards. It is not treated as an independent ancestry experiment: RI5CY/PULP lineage and overlapping fixes need deduplication. core-v-verif remains a supporting source to retrieve selectively, not an already-reviewed corpus.

Ten editorial seeds were chosen from title-level subsystem leads: #1064, #975, #889, #888, #880, #730, #723, #466, #920 and PR #195. This is a purposive sample, not a project-wide top-ten ranking. Five explicitly cross-referenced local PRs (#824, #860, #841, #881, #897) were then collected, giving 15 source records. Conversations and timelines were collected for each; PR detail, review summaries, inline comments and final diffs were included for all six PRs. References are not proof of fixes.

Shared PR #897 connects two seeds, yielding nine retrieval groups. Groups are retrieval units, not deduplicated defects. Attachments, external repositories, intermediate diffs and further recursive references are not included; collect them before drawing conclusions when needed. Raw discussions and code remain in the ignored local cache. Source IDs, revisions and hashes are in [sources.json](sources.json).

## Jev triage

Pinned `jev-1.13.0` assessed the collected evidence against the existing **24 public Ibex candidate properties**, using the same typed questions. No private target-design data was sent. The full group text was losslessly split at 24,000 Unicode characters, with partial-context metadata; all 53 parts completed. Usage: **556,338 input tokens and 29,146 output tokens**. This is successful API usage, not Codex billing or a monetary invoice.

Five groups contain at least one `new_candidate` part. They form the next reading queue below. Partial answers also include unclear/not-applicable/fetch-evidence labels; a positive fragment does not establish whole-group novelty or correctness. `closest_existing=none` is a model result, not proof of no overlap. The remaining four groups are retained for later review/context collection.

Ordering below is editorial: a small focused change first, then more complex multi-fix groups. It is **not a Jev severity score** or a ranking across all 1,052 records. The code and descriptions were spot-checked to phrase reading questions, but full human adjudication and RTL reproduction have not been completed.

## Next five reading groups

| Order | Sources | Topic |
|---:|---|---|
| 1 | [#195](https://github.com/openhwfoundation/cv32e40p/pull/195) | Hardware-loop state during interrupt cancellation |
| 2 | [#880](https://github.com/openhwfoundation/cv32e40p/issues/880), [#881](https://github.com/openhwfoundation/cv32e40p/pull/881) | Zero hardware-loop count |
| 3 | [#888](https://github.com/openhwfoundation/cv32e40p/issues/888), [#889](https://github.com/openhwfoundation/cv32e40p/issues/889), [#897](https://github.com/openhwfoundation/cv32e40p/pull/897) | Cancelled loop update and shared writeback |
| 4 | [#730](https://github.com/openhwfoundation/cv32e40p/issues/730), [#841](https://github.com/openhwfoundation/cv32e40p/pull/841) | Custom-instruction operand hazards |
| 5 | [#723](https://github.com/openhwfoundation/cv32e40p/issues/723), [#824](https://github.com/openhwfoundation/cv32e40p/pull/824), [#860](https://github.com/openhwfoundation/cv32e40p/pull/860) | Split memory accesses under FPU contention |

1. Inspect the interrupt/id-ready write gate and determine whether it adds a property or specializes existing cancellation rules.

2. Check decrement eligibility and zero-count semantics before deriving a counter-underflow property.

3. Separate the cancelled cv.end report from the ALU/FPU forwarding report; a shared multi-fix PR does not make them one root cause.

4. Inspect operand availability for XPULP consumers of multi-cycle FPU/Zfinx results, with explicit configuration tags.

5. Trace address ownership across split accesses and delayed writeback; distinguish the applicable extension and misalignment policies.

## Next execution boundary

Read one group at a time. Extract property, applicability, trigger, independent oracle, source revision and regression evidence. Compare mechanisms with the Ibex checklist and collapse inherited/specialized duplicates before counting new entries. Multi-fix PRs may yield several cases or none. Do not report the five groups as five new properties or verified vulnerabilities. Hardware-loop/FPU-specific questions should not be forced onto targets without those mechanisms.

Reproduction tools: `tools/cv32e40p_collect_seed.py` retrieves the bounded source set using authenticated GitHub CLI; `tools/cv32e40p_seed_triage.py` uses TYPESAFE_API_KEY from the environment and caches exact payload hashes. Maximum 128 requests per prepared seed run is enforced. Successful responses are reused on rerun. [Questions](questions.json), [part results](part-results.json), [usage](usage.json), [reading queue](next-five.json).

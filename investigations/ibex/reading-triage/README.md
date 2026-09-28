# Jev-directed reading queue

This follow-up asks Jev which history deserves detailed reading, before sending evidence to Codex. It uses the cached 2026-09-28 Ibex index with **no keyword prefilter**.

**Input:** record type, title and body only. No comments, diffs, changed paths or merge status were supplied. No raw evidence was truncated. **Model:** `jev-1.13.0`.

| Route | Records | Next action |
| --- | ---: | --- |
| `deep_read` | 552 | Read linked comments, code changes and tests; deduplicate first. |
| `fetch_evidence` | 1796 | Fetch missing context before deciding whether to read deeply. |
| `low_priority` | 133 | Retain for exclusion audits; do not discard permanently. |

Evaluated **2481 / 2481** records. Missing records: []. These are record counts, not independent bugs or deduplicated tasks.

API-reported input: **3,398,951 tokens**; output: **531,549 tokens**. At $0.042 per million input tokens and free output, the list-price calculation is **$0.142756**. This is not an invoice. Pricing reference: [official model documentation](https://docs.typesafe.ai/models), checked 2026-09-28.

Recorded failed attempts: 3. Failed HTTP responses do not supply usage and are excluded from the measured totals. After a transient HTTP 503, the run was deliberately resumed using successful-response caches; there was no automatic retry loop.

This new all-index pass is separate from the earlier 60-call pilot. Actual Codex token savings, precision and recall have not been measured. Model routes and scores are prioritization suggestions, not correctness findings or calibrated bug probabilities.

## Check against the earlier pilot

Earlier pilot routing counts: {'deep_read': 13, 'fetch_evidence': 17}. Earlier pilot records sent to low priority: [].

This is a sanity check against known reviewed cases, not an independent evaluation set. `fetch_evidence` preserves a case for follow-up; only `low_priority` postpones it. No score threshold discards records.

| PR | New route | Category |
| --- | --- | --- |
| [#157](https://github.com/lowRISC/ibex/pull/157) | deep_read | rtl |
| [#272](https://github.com/lowRISC/ibex/pull/272) | deep_read | rtl |
| [#277](https://github.com/lowRISC/ibex/pull/277) | fetch_evidence | rtl |
| [#294](https://github.com/lowRISC/ibex/pull/294) | deep_read | rtl |
| [#332](https://github.com/lowRISC/ibex/pull/332) | fetch_evidence | rtl |
| [#398](https://github.com/lowRISC/ibex/pull/398) | fetch_evidence | unclear |
| [#401](https://github.com/lowRISC/ibex/pull/401) | fetch_evidence | rtl |
| [#465](https://github.com/lowRISC/ibex/pull/465) | fetch_evidence | rtl |
| [#475](https://github.com/lowRISC/ibex/pull/475) | fetch_evidence | rtl |
| [#712](https://github.com/lowRISC/ibex/pull/712) | deep_read | rtl |
| [#742](https://github.com/lowRISC/ibex/pull/742) | fetch_evidence | rtl |
| [#792](https://github.com/lowRISC/ibex/pull/792) | fetch_evidence | rtl |
| [#813](https://github.com/lowRISC/ibex/pull/813) | deep_read | rtl |
| [#854](https://github.com/lowRISC/ibex/pull/854) | deep_read | rtl |
| [#903](https://github.com/lowRISC/ibex/pull/903) | fetch_evidence | rtl |
| [#919](https://github.com/lowRISC/ibex/pull/919) | fetch_evidence | rtl |
| [#928](https://github.com/lowRISC/ibex/pull/928) | fetch_evidence | rtl |
| [#1054](https://github.com/lowRISC/ibex/pull/1054) | fetch_evidence | rtl |
| [#1107](https://github.com/lowRISC/ibex/pull/1107) | deep_read | rtl |
| [#1136](https://github.com/lowRISC/ibex/pull/1136) | deep_read | rtl |
| [#1141](https://github.com/lowRISC/ibex/pull/1141) | fetch_evidence | rtl |
| [#1234](https://github.com/lowRISC/ibex/pull/1234) | fetch_evidence | rtl |
| [#1309](https://github.com/lowRISC/ibex/pull/1309) | fetch_evidence | rtl |
| [#1744](https://github.com/lowRISC/ibex/pull/1744) | deep_read | rtl |
| [#1813](https://github.com/lowRISC/ibex/pull/1813) | fetch_evidence | rtl |
| [#1883](https://github.com/lowRISC/ibex/pull/1883) | deep_read | verification_interface |
| [#2446](https://github.com/lowRISC/ibex/pull/2446) | deep_read | rtl |
| [#2501](https://github.com/lowRISC/ibex/pull/2501) | fetch_evidence | verification |
| [#2442](https://github.com/lowRISC/ibex/pull/2442) | deep_read | verification |
| [#2439](https://github.com/lowRISC/ibex/pull/2439) | deep_read | verification |

Two concrete sanity checks: [#1883](https://github.com/lowRISC/ibex/pull/1883) now routes to detailed reading as a verification-interface case, even though its priority score is only 0.67. A 0.70 score cutoff would lose it. Conversely, [#24](https://github.com/lowRISC/ibex/issues/24), a PDF documentation-build failure, routes to detailed reading but is categorized as tooling. The next-batch scope filter keeps it outside the RTL/verification queue. These examples support using explicit actions and scope together, not treating either scores or routes as ground truth.

## Proposed next batch

At most 30 unreviewed records: 25 from `deep_read` in RTL, verification, verification-interface, integration or unclear categories, plus five `low_priority` audit records. For deep reads, rotate across categories; within each category sort by descending review priority, then ascending record number. For audits, sort by SHA-256 of `ibex-audit-2026-09-28:NUMBER`. Exclude the previous 30 pilot PRs. This deterministic diversity rule is not a validated optimizer. Link related issues and PRs before spending the detailed-reading budget.

**These are leads, not newly verified defects.** Titles below are upstream labels, not endorsements. A model reason is not an established mechanism.

| Record | Upstream title | Category | Model reason |
| --- | --- | --- |
| [#340](https://github.com/lowRISC/ibex/issues/340) | Instruction fetch error execution | deep_read | rtl |
| [#2187](https://github.com/lowRISC/ibex/issues/2187) | [dv] Deep dive regression triage | deep_read | verification |
| [#2476](https://github.com/lowRISC/ibex/issues/2476) | rvfi_mem_rmask is non-zero on instructions that make no memory access | deep_read | verification_interface |
| [#2311](https://github.com/lowRISC/ibex/issues/2311) | [rtl] IbexSimpleSystem missing instruction address check | deep_read | integration |
| [#574](https://github.com/lowRISC/ibex/issues/574) | Fetch FIFO blocks instruction request when full. | deep_read | rtl |
| [#2511](https://github.com/lowRISC/ibex/pull/2511) | [dv] Reclaim helper objections at run_phase end | deep_read | verification |
| [#2231](https://github.com/lowRISC/ibex/issues/2231) | [rvfi] rvfi_pc_wdata doesn't consider mret/dret | deep_read | verification_interface |
| [#757](https://github.com/lowRISC/ibex/issues/757) | Ease of adapting Ibex memory protocol to tilelink for non 32-bit access | deep_read | integration |
| [#2452](https://github.com/lowRISC/ibex/issues/2452) | [BUG] Misaligned cross-page `sw` partially writes memory before store fault completes | deep_read | rtl |
| [#2314](https://github.com/lowRISC/ibex/issues/2314) | [dv,TestFW] Cosim mismatches due to dside access misidentified as iside | deep_read | verification |
| [#2015](https://github.com/lowRISC/ibex/issues/2015) | [cosim] Consider different interrupt/debug request notification mechanism | deep_read | verification_interface |
| [#2360](https://github.com/lowRISC/ibex/issues/2360) | PLIC claim process with Ibex | deep_read | integration |
| [#2473](https://github.com/lowRISC/ibex/issues/2473) | [pmp/debug]: DRET to U-mode does not clear `mstatus.MPRV` | deep_read | rtl |
| [#2461](https://github.com/lowRISC/ibex/issues/2461) | [DV] Add regression tests for Zcmp instruction traps and atomicity | deep_read | verification |
| [#2094](https://github.com/lowRISC/ibex/issues/2094) | IbexSetExceptionPCOnSpecialReqIfExpected firing when it shouldn't | deep_read | verification_interface |
| [#2323](https://github.com/lowRISC/ibex/issues/2323) | [SecureIbex] OpenOCD attach fails when SecureIbex=1 (works when SecureIbex=0) | deep_read | integration |
| [#2487](https://github.com/lowRISC/ibex/pull/2487) | ibex: clear cpuctrlsts.sync_exc_seen on dret, matching mret | deep_read | rtl |
| [#2512](https://github.com/lowRISC/ibex/pull/2512) | [dv] Fix fcov illegal bins that reject legal cases | deep_read | verification |
| [#2518](https://github.com/lowRISC/ibex/pull/2518) | [dv/cosim] Pass internal NMI mtval to Spike | deep_read | verification_interface |
| [#114](https://github.com/lowRISC/ibex/issues/114) | Data memory interface | deep_read | integration |
| [#849](https://github.com/lowRISC/ibex/issues/849) | PMP store fault does not jump to exception handler | deep_read | rtl |
| [#2515](https://github.com/lowRISC/ibex/pull/2515) | [dv] Turn on the icache ECC checks | deep_read | verification |
| [#808](https://github.com/lowRISC/ibex/issues/808) | SpecialReqAllGivesSpecialReqBranchIfBranchInst assertion failure | deep_read | verification_interface |
| [#2135](https://github.com/lowRISC/ibex/issues/2135) | Endless illegal instructions when running elf executables | deep_read | integration |
| [#864](https://github.com/lowRISC/ibex/issues/864) | PMP fetch exception causing `X` propagation through IF stage | deep_read | rtl |
| [#1085](https://github.com/lowRISC/ibex/issues/1085) | Parallelize UVM tests without LSF (in CI) | exclusion_audit | tooling |
| [#1019](https://github.com/lowRISC/ibex/issues/1019) | We should list the (non-Python) requirements to build/run Ibex examples | exclusion_audit | tooling |
| [#72](https://github.com/lowRISC/ibex/issues/72) | Reference integration for FPGA | exclusion_audit | integration |
| [#1683](https://github.com/lowRISC/ibex/issues/1683) | [dv] Generic Code Coverage Waiver Tool | exclusion_audit | verification |
| [#1841](https://github.com/lowRISC/ibex/issues/1841) | [dv] Automatically generate dump file | exclusion_audit | tooling |

## Reproduce and inspect

- [All routes and input fingerprints](results.json)
- [Sortable CSV queue](queue.csv)
- [Exact Jev questions](questions.json)
- [Usage and coverage](summary.json)
- [Proposed batch JSON](next-batch.json)

Run `python3 tools/ibex_reading_triage.py evaluate --workers 12` with `TYPESAFE_API_KEY` provided via the environment, then `python3 tools/ibex_reading_triage.py summarize`. The collector uses cached public title/body data under ignored `.local/`. Results are request-hash cached; errors stop new work without automatic retries. A 96,000-byte input limit records oversized exclusions. A 5-million-input-token per-process guardrail stops new requests; in-flight requests may finish. These guards are not a strict billing cap.

The recorded run used one forward worker process and a tail-assisting process with a 100-record prefix safety gap. This avoids overlapping submissions while reducing elapsed time. Input fingerprints and coverage are checked before publication.

## Remaining limits

Most importantly, `fetch_evidence` is still work. Counting only `deep_read` as all remaining effort would overstate savings. The queue still requires link deduplication, source-level confirmation and periodic low-priority audits. Commit-only history is not covered by this issue/PR pass.

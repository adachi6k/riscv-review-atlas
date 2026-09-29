# VexRiscv: bounded next-core selection

Date: 2026-09-29. Investigation [#11](https://github.com/adachi6k/riscv-review-atlas/issues/11). Pinned public HEAD: `baf7dc82f855eddaf5b0a20a6802c526f127e38a`.

## Why this core next

The existing catalog puts VexRiscv and NEORV32 after the Ibex/CV32E40P pilots. VexRiscv is selected for a bounded next pass on ordinary integer/pipeline and bus integration questions. Its generator/plugin configurations require explicit applicability and source-generation provenance. This is an editorial scope choice, not a quality ranking or proof of cross-core independence.

| Candidate | Catalog issue / PR counts (2026-09-28) | Decision for this pass |
|---|---:|---|
| VexRiscv | 380 / 118 | First: configuration and pipeline/bus boundary leads; review generator source before interpreting generated RTL |
| NEORV32 | 307 / 1,070 | Alternative: VHDL/CPU-SoC context, useful for a later portability comparison |
| PicoRV32 | 192 / 104 | Smaller historical source; catalog marks it archived, and its size-oriented architecture changes applicability |
| SERV | 71 / 99 | Smaller history, but bit-serial execution is a less direct next comparison for conventional pipeline timing |

Counts are metadata, not numbers of bugs or estimated reading cost. The candidates and their descriptions come from the dated [catalog](../../data/repositories.json); no fresh full history assessment of the three alternatives was performed.

## What was collected and read

A fresh VexRiscv REST index contains **499 issue/PR records: 380 issues and 119 PRs**, all states. The one-PR difference from the catalog is a later snapshot, not a defect-count change. Full index bodies were cached. Title keywords for load/store, branch, hazard, stall, JALR, forwarding, pipeline and flush provided leads; the chosen sample is not representative or exhaustive. Security assessment and modified-RTL experiments are excluded from this pass.

Bodies and all retrieved issue-conversation comments were read for #191, #318, #86, #158 and #165. PR metadata/final diffs were additionally cached for #86 and #158; detailed source adjudication remains pending. Timelines, inline reviews, attachments, complete commit history and recursive linked repositories were not collected. [sources.json](sources.json) records revisions and hashes; raw content stays in the ignored local cache.

## Three selected reading groups

| Order | Source | Evidence so far | Next question |
|---:|---|---|---|
| 1 | [#191](https://github.com/SpinalHDL/VexRiscv/issues/191) | Maintainer acknowledges a bus-size regression and says it was corrected; exact fixing commit not yet linked | Trace the AXI bridge/generator change and distinguish bytes per beat from cache-line/burst size; establish bus-width/configuration applicability |
| 2 | [#318](https://github.com/SpinalHDL/VexRiscv/issues/318), with [#158](https://github.com/SpinalHDL/VexRiscv/pull/158) as context | Discussion identifies write responses sent by the testbench in a configuration that does not expect them; reporter says correcting the driver resolves the symptom | Trace write-response eligibility and response ownership in the selected cache/bridge configuration; separate integration contract from core RTL |
| 3 | [#86](https://github.com/SpinalHDL/VexRiscv/pull/86) | Merged short-pipeline elaboration changes; discussion narrows the reporter's configuration to instruction cache only | Read each changed plugin and its stage assumptions; find evidence for functional coverage separately from successful elaboration |

Follow-up: the selected sources now have a [bounded source review](deep-read.md) and [three candidate entries](checklist.md). None is independently reproduced. #191's change predates this review and is not a new discovery. #318 must not be summarized as a proven store-to-load forwarding defect. The #86 author explicitly expresses uncertainty about hazards; a buildable generated design is not sufficient functional evidence.

## Screening prevented misleading entries

[#158's discussion](https://github.com/SpinalHDL/VexRiscv/pull/158#issuecomment-746340010) explains why the selected simple bus does not wait for write responses and therefore does not provide the proposed store-response-fault behavior. The PR is **unmerged**. Its title alone would misleadingly look like a completed defect fix. Keep it as contract/reference-model context, not a mandatory behavior for every implementation.

[#165](https://github.com/SpinalHDL/VexRiscv/issues/165) was withdrawn by the reporter after discussion of JALR's low-bit clearing. It is not a confirmed misalignment defect and is not a priority reproduction candidate. The normative ISA/configuration contract should still be consulted when deriving an alignment test.

## Bounded budget and next boundary

This pass made **zero Jev calls**. There is no measured total Codex token/billing figure. Do not extrapolate whole-history cost from issue totals. The next pass should retrieve only #191's fixing history and the source/bridge context needed for #318/#158 and #86, then extract applicability, stimulus and independent oracle before deciding whether another target needs a test. Cap the first deep-read pass at these three groups; expand only for concrete missing causal evidence. A Jev batch, if later useful, should have a measured payload estimate and a request cap before submission.

No upstream comments/issues were posted and no RTL simulation was run in this selection pass.

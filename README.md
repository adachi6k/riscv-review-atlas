# RISC-V Review Atlas

Evidence-backed review questions and verification checklists derived from public RISC-V development history.

The goal is to turn issues, discussions, fixing commits, and regression tests into reusable engineering knowledge: **what property should hold, when it applies, and how to check it**.

## Current status

This repository contains a discovery catalog and bounded Ibex/CV32E40P investigations. Evidence states distinguish source-reviewed candidates from the one bounded CV32E40P component reproduction; no whole-core validation is implied.

- **67 GitHub repositories:** 44 core candidates, 7 lineage/integration-history repositories, and 16 related verification, reference-model, or system projects.
- **3 additional GitLab candidates:** public project metadata checked; bulk history access still needs validation.
- Snapshot date: **2026-09-28**. GitHub public HEAD references and issue/PR totals were retrieved. No claim of exhaustive worldwide coverage.
- **70 repository investigation issues** are linked from the [research roadmap](https://github.com/adachi6k/riscv-review-atlas/issues/1) and [investigation index](docs/investigation-index.md).
- **Ibex pilot:** 30 historical PRs collected, 24 candidate properties extracted from 28 PRs, two broad changes deferred; 60 Jev evaluations measured. No independent RTL reproduction has been run.
- **Earlier Jev title/body triage:** all 2,481 indexed Ibex issue/PR records routed from title/body; 552 deep-read leads, 1,796 evidence-fetch leads and 133 low-priority records. This is not a source-level review.
- **Jev assessment with comments and diffs:** all 1,560 PR diffs, conversations, reviews and 27 explicitly linked standalone commits included across 1,804 retrieval groups; 807 deep-read leads, 349 needing more context, 648 low priority. See the [report](investigations/ibex/full-evidence/README.md).
- Exhaustive deep history review remains incomplete. See the [pilot report and token budget](investigations/ibex/README.md).

## Explore

- [VexRiscv next-core selection](investigations/vexriscv/README.md): five reports screened; three functional reading groups selected with explicit exclusions. No Jev calls or reproduction in this pass.
- [CV32E40P bounded investigation](investigations/cv32e40p/README.md): nine seed groups reviewed, five candidate properties, one bounded zero-count component reproduction and a source-reviewed CSR-flush extension.

- [Assessment with comments and diffs](investigations/ibex/full-evidence/README.md): comments and diffs supplied before Jev selects the reading queue, with measured usage and provenance.

- [Ibex pilot](investigations/ibex/README.md): checklist candidates, evidence, Jev comparison and bounded continuation plan.
- [Jev-directed reading queue](investigations/ibex/reading-triage/README.md): whole-index routing before detailed evidence review.

- [Repository catalog](docs/repository-catalog.md): categorized sources, counts, and history links.
- [Investigation index](docs/investigation-index.md): one task per repository and the overall roadmap.
- [Research workflow](docs/methodology.md): evidence collection, classification, and validation.
- [Checklist entry format](docs/checklist-format.md): the proposed output of each investigation.
- [Public history examples](docs/history-examples.md): initial leads, not independently verified findings.
- [JSON](data/repositories.json) / [CSV](data/repositories.csv): machine-readable catalog.

## Suggested starting points

1. **Ibex:** establish a bounded extraction workflow for CSR, trap, debug, and verification configuration.
2. **CV32E40P + core-v-verif:** compare core RTL findings with defects in verification models and oracles.
3. **VexRiscv or NEORV32:** test whether review questions transfer across independent implementations and languages.
4. **CVA6:** extend into cache, MMU, and operating-system-facing privilege behavior.
5. **Rocket, BOOM, and XiangShan:** expand into larger systems and out-of-order/speculative execution with explicit applicability tags.

These are investigation priorities, not quality or safety rankings. More reported issues do not imply worse hardware.

## Principles

- Keep every question traceable to public evidence and revisions.
- Separate reported symptoms, hypotheses, confirmed mechanisms, and reproduced behavior.
- Treat a closed issue as a workflow state, not proof of a fix.
- Deduplicate inherited or backported fixes across forks and renamed projects.
- Distinguish core RTL, verification models, reference models, and system integration.
- Preserve uncertainty and record why a check is inapplicable.
- Use Jev or other evaluation tools to assist prioritization; model scores are not calibrated bug probabilities or proof.

## Contributing and licensing

See [CONTRIBUTING.md](CONTRIBUTING.md). Original project material is available under the [MIT license](LICENSE). Linked or quoted third-party material retains its original licensing; this repository does not relicense upstream code, issue text, or datasets.

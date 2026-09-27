# RISC-V Review Atlas

Evidence-backed review questions and verification checklists derived from public RISC-V development history.

The goal is to turn issues, discussions, fixing commits, and regression tests into reusable engineering knowledge: **what property should hold, when it applies, and how to check it**.

## Current status

This repository starts with a discovery catalog, not a completed checklist or a collection of confirmed vulnerabilities.

- **67 GitHub repositories:** 44 core candidates, 7 lineage/integration-history repositories, and 16 related verification, reference-model, or system projects.
- **3 additional GitLab candidates:** public project metadata checked; bulk history access still needs validation.
- Snapshot date: **2026-09-28**. GitHub public HEAD references and issue/PR totals were retrieved. No claim of exhaustive worldwide coverage.
- Repository investigations are tracked in [GitHub Issues](https://github.com/adachi6k/riscv-review-atlas/issues).
- Full history ingestion, automated model evaluation, and independent reproductions have not been performed by this project yet.

## Explore

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

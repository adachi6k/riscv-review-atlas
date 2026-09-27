# Investigation methodology

## 1. Establish the source and scope

Confirm the canonical repository, redirects, upstream/fork relationships, license terms, default branch, and pinned revision. Check issues, comments, pull/merge requests, timeline links, commits, and regression-test access separately. Missing data is unknown, not zero.

Define a bounded initial sample and document the selection rule. A keyword-filtered sample is not representative of all defects. Archived repositories can still contain useful evidence.

## 2. Collect evidence without losing provenance

Collect relevant issue bodies and comments, fixing PRs/MRs, complete selected text diffs, and added tests. Record source URLs, timestamps, revisions, hashes, exclusions, and failures. Do not silently truncate evidence. If input must be partitioned, preserve reconstructability and document that each evaluation sees only partial context.

Do not copy entire upstream discussions or source trees into this repository by default. Publish concise original summaries, links, and permitted minimal excerpts. Preserve required attribution and inspect third-party license terms.

## 3. Triage and trace the mechanism

Classify core RTL, verification model/oracle, ISS behavior, integration, tooling, feature request, and insufficient evidence. Trace symptoms to code changes and tests. Separate the implementation mechanism from hypotheses about why it was introduced or escaped verification.

A merged PR is evidence of a change, not independent reproduction. A closed issue may be invalid, duplicate, or unresolved in the intended configuration. Record those distinctions.

## 4. Extract a reusable question

Describe the property independently of signal names, then retain configuration constraints: ISA extensions, privilege modes, pipeline organization, cache/MMU, bus, outstanding transactions, and reset/debug conditions.

Follow the [entry format](checklist-format.md). Link related questions rather than inflating the checklist with equivalent fixes. Shared ancestry and backports are not independent occurrences.

## 5. Validate applicability and record results

Select a target revision and configuration. Define the stimulus, required condition/reachability, observation, and independent expected result before judging pass/fail. Record the exact commands and outcomes if tests are run. Never label unexecuted tests as passed.

Keep scope-specific evidence states: reported, source-reviewed, fix-linked, regression-linked, independently-reproduced. These states are not interchangeable.

## 6. Evaluate the workflow

Measure traceability, deduplicated questions, applicable/inapplicable cases, testability, manual effort, and API cost. Do not claim improved recall, accuracy, or time savings without an appropriate comparison.

Model evaluations, including Jev, can support triage. Partition maxima favor larger evidence sets and may miss guards outside the partition. Preserve raw-input fingerprints and model identifiers; do not equate scores with bug probabilities.

## Discovery provenance

Starting points included the [GitHub RISC-V collection](https://github.com/collections/riscv-cores), the [RISC-V architecture ID list](https://github.com/riscv/riscv-isa-manual/blob/main/marchid.md), the [archived core list](https://github.com/riscvarchive/riscv-cores-list), and [CORE-V documentation](https://docs.openhwgroup.org/en/latest/source/cores.html). Repository metadata and HEADs were checked with GitHub REST; issue/PR totals were obtained through GraphQL. GitLab project metadata was checked separately.

The catalog is a dated snapshot. GitHub language and license detection can be misleading for generated trees and mixed repositories. A null/NOASSERTION license field requires inspecting the actual upstream terms.

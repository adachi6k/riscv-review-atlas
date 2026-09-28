# Ibex: prioritized reading shortlist

Snapshot: 2026-09-29. This is a research reading order, **not bug severity or bug probability**. No new defects were reproduced for this selection.

## Selection method

Reuse the completed full-evidence Jev triage of 1,804 retrieval groups (2,481 records), including comments, reviews and available final text diffs. Review candidate titles across the deep-read groups with new/mixed-property labels, then inspect selected source descriptions to establish concrete reading questions. The final ordering is editorial, not an additional Jev score or an exhaustive human comparison of all 807 deep-read groups. No additional Jev calls were made.

Priorities favor an explicit failure mechanism or falsifiable check, potential additions beyond the existing 24 properties, reusable lessons across configurations, and manageable reading scope. Topic diversity is deliberate. Small inputs alone do not determine rank. Previous pilot groups are excluded from the top 20. A retrieval group can contain several unrelated changes: shared references are not proof of one root cause.

P1 contains ten cases to read first; P2 contains ten subsequent cases that are more specialized, require additional adjudication, or complement P1. P3 retains other deep-read candidates. P4 requires evidence/context follow-up. P5 is retained for exclusion audits. `covered` only means the group intersects the previous pilot, not that every member was read. P4/P5 are workflow dispositions, not claims that their defects are less important.

Classification counts: P1: 10, P2: 10, P3: 760, P4: 348, P5: 648, covered: 28.

## Top 20

| Rank | Priority | Entry | Topic | Snapshot status | Group payload proxy |
|---:|---|---|---|---|---:|
| 1 | P1 | [#2166](https://github.com/lowRISC/ibex/pull/2166) | Unexpected memory responses | merged PR | 12,051 |
| 2 | P1 | [#1469](https://github.com/lowRISC/ibex/pull/1469) | Branch prediction recovery | merged PR | 13,184 |
| 3 | P1 | [#2374](https://github.com/lowRISC/ibex/pull/2374) | Expanded instruction interruption | merged PR | 27,442 |
| 4 | P1 | [#169](https://github.com/lowRISC/ibex/pull/169) | Faulting-load side effects | merged PR | 4,830 |
| 5 | P1 | [#172](https://github.com/lowRISC/ibex/pull/172) | Illegal jump side effects | merged PR | 4,003 |
| 6 | P1 | [#836](https://github.com/lowRISC/ibex/pull/836) | Stalled jump control | merged PR | 3,483 |
| 7 | P1 | [#2178](https://github.com/lowRISC/ibex/issues/2178) | RV32E source-register legality | issue report | 3,249 |
| 8 | P1 | [#2514](https://github.com/lowRISC/ibex/pull/2514) | Reset can disable the checker | unmerged PR | 7,307 |
| 9 | P1 | [#858](https://github.com/lowRISC/ibex/pull/858) | Protocol-checker correctness | merged PR | 5,850 |
| 10 | P1 | [#2142](https://github.com/lowRISC/ibex/pull/2142) | Unmapped-address handling | merged PR | 3,791 |
| 11 | P2 | [#713](https://github.com/lowRISC/ibex/pull/713) | Split instruction fault address | merged PR | 12,114 |
| 12 | P2 | [#1421](https://github.com/lowRISC/ibex/pull/1421) | Split data fault address | merged PR | 7,767 |
| 13 | P2 | [#1747](https://github.com/lowRISC/ibex/pull/1747) | Cache invalidation re-entry | merged PR | 13,054 |
| 14 | P2 | [#1036](https://github.com/lowRISC/ibex/pull/1036) | Reserved shift encodings | merged PR | 4,663 |
| 15 | P2 | [#575](https://github.com/lowRISC/ibex/pull/575) | Pending versus enabled interrupts | merged PR | 10,737 |
| 16 | P2 | [#1948](https://github.com/lowRISC/ibex/issues/1948) | Reference-model mismatch | issue report | 2,983 |
| 17 | P2 | [#2169](https://github.com/lowRISC/ibex/issues/2169) | Configuration-dependent branch stall | issue report | 3,668 |
| 18 | P2 | [#1835](https://github.com/lowRISC/ibex/pull/1835) | Write-response integrity | merged PR | 9,712 |
| 19 | P2 | [#2490](https://github.com/lowRISC/ibex/issues/2490) | Reset-time PMP legality | issue report | 3,276 |
| 20 | P2 | [#1135](https://github.com/lowRISC/ibex/pull/1135) | Security feature combinations | merged PR | 6,462 |

## What to confirm

### 1. Unexpected memory responses (P1)

Start with [[rtl] Guard against false memory responses for secure configurations](https://github.com/lowRISC/ibex/pull/2166). Check that response/error handling requires an outstanding transaction; distinguish secure hardening from the non-secure protocol assumption.

Related group sources: [#2144](https://github.com/lowRISC/ibex/issues/2144), [#2166](https://github.com/lowRISC/ibex/pull/2166), [#2213](https://github.com/lowRISC/ibex/issues/2213).

Existing-property hints from Jev: IBEX-009. These hints and novelty labels require human adjudication.

### 2. Branch prediction recovery (P1)

Start with [Move not-taken, predicted taken branch address calculation to ID stage](https://github.com/lowRISC/ibex/pull/1469). Check ownership of the recovery PC when consecutive predicted branches overlap with a skid-buffer stall.

Related group sources: [#1462](https://github.com/lowRISC/ibex/issues/1462), [#1469](https://github.com/lowRISC/ibex/pull/1469).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 3. Expanded instruction interruption (P1)

Start with [[rtl] Flush Zcmp state machine on exception or interrupt and make the committing instructions atomic](https://github.com/lowRISC/ibex/pull/2374). Check abort-state reset, atomic commit and debug boundaries; read #2461 alongside the fix to separate manual checks from regression coverage.

Related group sources: [#2374](https://github.com/lowRISC/ibex/pull/2374), [#2461](https://github.com/lowRISC/ibex/issues/2461), [#2497](https://github.com/lowRISC/ibex/pull/2497), [#2498](https://github.com/lowRISC/ibex/pull/2498).

Existing-property hints from Jev: IBEX-017. These hints and novelty labels require human adjudication.

### 4. Faulting-load side effects (P1)

Start with [ID/EX stage: do not write to register file upon load errors](https://github.com/lowRISC/ibex/pull/169). Check that a load error suppresses register writeback, including error/data arriving together.

Related group sources: [#162](https://github.com/lowRISC/ibex/issues/162), [#169](https://github.com/lowRISC/ibex/pull/169).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 5. Illegal jump side effects (P1)

Start with [Decoder: avoid setting PC upon illegal JALR instructions](https://github.com/lowRISC/ibex/pull/172). Check that illegal JALR does not redirect the PC or corrupt the exception PC.

Related group sources: [#170](https://github.com/lowRISC/ibex/issues/170), [#172](https://github.com/lowRISC/ibex/pull/172).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 6. Stalled jump control (P1)

Start with [[rtl] Fix jump signal stuck high during stall](https://github.com/lowRISC/ibex/pull/836). Check whether a preceding memory stall stretches jump control and repeats fetch activity.

Related group sources: [#836](https://github.com/lowRISC/ibex/pull/836).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 7. RV32E source-register legality (P1)

Start with [Store instructions do not always raise RV32E exceptions](https://github.com/lowRISC/ibex/issues/2178). Check the store-data register independently of the ALU immediate selection; confirm the reported behavior against the pinned implementation.

Related group sources: [#2178](https://github.com/lowRISC/ibex/issues/2178).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 8. Reset can disable the checker (P1)

Start with [[dv] Keep checking after a mid-test reset](https://github.com/lowRISC/ibex/pull/2514). Inspect the proposed reset/checker restart tests and require nonzero checked progress after reset; this PR is unmerged in the snapshot.

Related group sources: [#2514](https://github.com/lowRISC/ibex/pull/2514).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 9. Protocol-checker correctness (P1)

Start with [Fix two bugs in the icache <-> core protocol checker](https://github.com/lowRISC/ibex/pull/858). Inspect both checker fixes and derive a negative test for the checker itself; do not assume checker assertions are a trustworthy oracle.

Related group sources: [#858](https://github.com/lowRISC/ibex/pull/858).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 10. Unmapped-address handling (P1)

Start with [[bus] Return error if decode fails](https://github.com/lowRISC/ibex/pull/2142). Check that decode misses produce errors rather than aliasing a real device; applicability is the example system/interconnect.

Related group sources: [#2142](https://github.com/lowRISC/ibex/pull/2142).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 11. Split instruction fault address (P2)

Start with [[rtl] Fix mtval for unaligned instr errors](https://github.com/lowRISC/ibex/pull/713). Check that mtval identifies the faulting half of a split instruction, rather than always the instruction start.

Related group sources: [#709](https://github.com/lowRISC/ibex/issues/709), [#713](https://github.com/lowRISC/ibex/pull/713).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 12. Split data fault address (P2)

Start with [[rtl] Fix mtval for unaligned accesses](https://github.com/lowRISC/ibex/pull/1421). Check the fault address for the second aligned transfer of a misaligned load/store; compare with the instruction-fetch case without conflating them.

Related group sources: [#1421](https://github.com/lowRISC/ibex/pull/1421).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 13. Cache invalidation re-entry (P2)

Start with [[rtl] Fix scrambling key request on icache inval](https://github.com/lowRISC/ibex/pull/1747). Check that another invalidation request during an active invalidation does not request a new scrambling key.

Related group sources: [#1747](https://github.com/lowRISC/ibex/pull/1747), [#1754](https://github.com/lowRISC/ibex/issues/1754).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 14. Reserved shift encodings (P2)

Start with [[rtl] Make sure decoder also checks bits 26 and 25 for slli, srli, srai](https://github.com/lowRISC/ibex/pull/1036). Check all required encoding bits, including bits 26 and 25, when deciding shift-immediate legality.

Related group sources: [#1018](https://github.com/lowRISC/ibex/issues/1018), [#1036](https://github.com/lowRISC/ibex/pull/1036).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 15. Pending versus enabled interrupts (P2)

Start with [[rtl] Decouple `mip` and `mie` CSRs](https://github.com/lowRISC/ibex/pull/575). Check that reading interrupt-pending state does not depend on interrupt-enable bits.

Related group sources: [#567](https://github.com/lowRISC/ibex/issues/567), [#575](https://github.com/lowRISC/ibex/pull/575).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 16. Reference-model mismatch (P2)

Start with [[cosim] Sort out error/pmp failure behaviour on unaligned accesses](https://github.com/lowRISC/ibex/issues/1948). Separate permitted split-access behavior from a real RTL defect; inspect pending-access bookkeeping on PMP failure.

Related group sources: [#1948](https://github.com/lowRISC/ibex/issues/1948).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 17. Configuration-dependent branch stall (P2)

Start with [Incorrect stalling behaviour for configurations with writeback stage but without branch target ALU results in an incorrect branch target](https://github.com/lowRISC/ibex/issues/2169). Investigate the reported load/branch sequence with writeback enabled and no branch-target ALU; external reproducer is not included in the corpus.

Related group sources: [#2169](https://github.com/lowRISC/ibex/issues/2169).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 18. Write-response integrity (P2)

Start with [[rtl/dv] Bring back data integrity check on write responses](https://github.com/lowRISC/ibex/pull/1835). Check the intended integrity-alert policy for write responses even though their data payload is unused; scope the security assumptions.

Related group sources: [#1835](https://github.com/lowRISC/ibex/pull/1835).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

### 19. Reset-time PMP legality (P2)

Start with [[pmp]: Custom `PMPRstCfg` values bypass PMP WARL normalization](https://github.com/lowRISC/ibex/issues/2490). Compare configurable PMP reset values with CSR-write WARL handling; validate the report and its parameter/specification assumptions before adopting a property.

Related group sources: [#2490](https://github.com/lowRISC/ibex/issues/2490).

Existing-property hints from Jev: IBEX-011. These hints and novelty labels require human adjudication.

### 20. Security feature combinations (P2)

Start with [[rtl] Various security feature bugfixes](https://github.com/lowRISC/ibex/pull/1135). Separate parameter legality, fetch-error PC checks and dummy-instruction checks into distinct candidate properties.

Related group sources: [#1080](https://github.com/lowRISC/ibex/issues/1080), [#1094](https://github.com/lowRISC/ibex/issues/1094), [#1095](https://github.com/lowRISC/ibex/issues/1095), [#1135](https://github.com/lowRISC/ibex/pull/1135).

Existing-property hints from Jev: none. These hints and novelty labels require human adjudication.

## Reading budget and next step

The 20 complete group payloads total **159,626 cl100k proxy tokens** (P1: 85,190; P2: 74,436). This measures prepared inputs, including repeated context/questions, not unique source text, actual Codex billing, or a time estimate. Read in batches of five; do not inject the whole set into one prompt.

For each entry, read the relevant discussion and diff, record assumptions, trigger, oracle and source revision, then decide whether it adds a new property, extends an existing property, or should be rejected. Start at the representative entry and only expand related records as necessary. Merge status is snapshot metadata, not independent correctness validation. Issue reports and unmerged PR claims remain unverified here. External reproducers and attachments were not collected; fetch them selectively when needed.

This replaces the earlier budget-first `next-batch.json` as the recommended reading order; that file remains as a historical queue proposal. Low-priority audits remain a separate task, not part of these top 20.

[Machine-readable top 20](top-20.json) · [All group classifications](all-groups.csv) · [Full triage report](../README.md)

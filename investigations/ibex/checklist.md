# Ibex pilot: candidate review checklist

These are **24 candidate review properties from 28 of 30 selected historical PRs**. They are source-reviewed: 22 link to merged fixes and two to unmerged proposals (#2439 and #2442). None was independently reproduced or validated on another core. Two broad changes remain deferred. One PR can support several properties; related PRs can support one property.

Full provenance, comparison SHAs and limitations: [case manifest](cases.json). The PR base is a comparison reference, not a proven affected revision range. [Machine-readable checklist](checklist.json).

All stimuli below are proposals. No RTL simulation, formal proof or co-simulation was run in this pilot.

## IBEX-001: Debug entry and state capture agree

**Property:** Accepted debug entry must capture a matching DPC and cause; withdrawing a request must not leave entry and capture disagreeing.

**Historical mechanism:** The change aligns debug-state transitions with the conditions used to save debug CSRs when a request or step condition changes.

**Applies to:** External halt or single-step debug entry. Respect the selected debug interface request-hold contract.

**Inspect:** Controller entry gating and CSR save enables.

**Proposed stimulus:** Sweep request removal around entry, observing debug state, DPC and cause together.

**Observation/oracle:** An independently specified entry decision and PC/cause tuple. Do not assume every one-cycle pulse must be accepted.

**Sources:** [#157](https://github.com/lowRISC/ibex/pull/157). See the manifest for revision/merge status and changed paths.

## IBEX-002: Debug-only operations stay debug-only

**Property:** DRET and accesses to debug-only CSRs must follow the selected debug specification outside debug mode.

**Historical mechanism:** DRET decoding gains a non-debug legality check, and debug-only CSR checks receive the debug-mode state.

**Applies to:** Implementations with DRET and debug CSRs; distinguish privilege from debug mode.

**Inspect:** Instruction legality and CSR access checks.

**Proposed stimulus:** Execute DRET and read/write each debug-only CSR inside and outside debug mode.

**Observation/oracle:** A specification-derived legality table and trap/state observations.

**Sources:** [#272](https://github.com/lowRISC/ibex/pull/272), [#277](https://github.com/lowRISC/ibex/pull/277). See the manifest for revision/merge status and changed paths.

## IBEX-003: Interrupt cause encodes the selected source

**Property:** Cause encoding must include the correct interrupt bank offset and source index.

**Historical mechanism:** The fast interrupt cause construction is changed to include the bank offset rather than only the selected fast-source index.

**Applies to:** Ibex fast interrupt bank; other cores need their own platform interrupt map.

**Inspect:** Interrupt selection and cause concatenation.

**Proposed stimulus:** Activate each fast interrupt separately, then competing sources.

**Observation/oracle:** An independently constructed platform interrupt-to-cause map.

**Sources:** [#294](https://github.com/lowRISC/ibex/pull/294). See the manifest for revision/merge status and changed paths.

## IBEX-004: Single-step traps preserve the resume point

**Property:** A stepped instruction that traps must preserve the specified trap transition before recording the debug resume PC.

**Historical mechanism:** The change allows the exception PC redirection before debug capture during single-step exception handling.

**Applies to:** Single-step with synchronous exceptions; pin the debug specification version.

**Inspect:** Trap redirection and debug PC capture.

**Proposed stimulus:** Single-step an illegal instruction and inspect trap CSRs, DPC and resumed execution.

**Observation/oracle:** The specified trap vector and debug resume sequence, not the implementation PC mux itself.

**Sources:** [#401](https://github.com/lowRISC/ibex/pull/401). See the manifest for revision/merge status and changed paths.

## IBEX-005: Debug entry and return preserve privilege semantics

**Property:** Debug entry uses the required execution privilege and DRET restores the saved privilege.

**Historical mechanism:** Debug entry explicitly selects machine privilege; debug return restores the saved DCSR privilege.

**Applies to:** Debug entry from supported lower privilege modes.

**Inspect:** Privilege state update and DRET restore.

**Proposed stimulus:** Enter debug from U-mode and return; repeat from M-mode.

**Observation/oracle:** Expected execution privilege and saved DCSR privilege at each transition.

**Sources:** [#465](https://github.com/lowRISC/ibex/pull/465). See the manifest for revision/merge status and changed paths.

## IBEX-006: Exceptions inside debug preserve saved context

**Property:** Implicit exception entry while already in debug must not overwrite context protected by the selected debug specification.

**Historical mechanism:** The exception-save path is guarded against normal trap-state updates while already in debug mode.

**Applies to:** Debug-mode exception handling; explicit legal CSR writes are a separate operation.

**Inspect:** CSR exception-save arbitration.

**Proposed stimulus:** Create exceptions in debug and compare protected trap/debug state before and after.

**Observation/oracle:** A specification-derived set of protected registers and allowed updates.

**Sources:** [#475](https://github.com/lowRISC/ibex/pull/475). See the manifest for revision/merge status and changed paths.

## IBEX-007: Rejected fetches do not create phantom responses

**Property:** A protection-rejected fetch must complete through an error path without waiting for data from a request never sent externally.

**Historical mechanism:** Cache fill accounting excludes PMP-rejected external transfers, and error availability can complete without returned instruction data.

**Applies to:** Instruction cache with PMP rejection, fills and partially available instruction data.

**Inspect:** Cache fill counters, error availability and ordering.

**Proposed stimulus:** Reject a fill at different positions, including a split instruction, while varying real response latency.

**Observation/oracle:** External accepted-request accounting plus an independently expected instruction access fault.

**Sources:** [#712](https://github.com/lowRISC/ibex/pull/712), [#792](https://github.com/lowRISC/ibex/pull/792). See the manifest for revision/merge status and changed paths.

## IBEX-008: Overlapping PMP entries obey priority

**Property:** Permission comes from the architecturally selected matching PMP entry, not a union of permissions.

**Historical mechanism:** PMP permission selection is changed from combining matching permissions to respecting entry priority.

**Applies to:** Multiple overlapping PMP entries; include privilege and lock semantics.

**Inspect:** PMP match reduction and permission selection.

**Proposed stimulus:** Configure overlapping allow/deny regions in both index orders and attempt accesses.

**Observation/oracle:** A specification-based PMP region-priority model.

**Sources:** [#742](https://github.com/lowRISC/ibex/pull/742). See the manifest for revision/merge status and changed paths.

## IBEX-009: Protection errors do not leak into later transactions

**Property:** A prior protection failure must not poison an unrelated later legal memory operation.

**Historical mechanism:** The registered PMP error is cleared when the LSU is idle.

**Applies to:** LSU with registered PMP error state.

**Inspect:** LSU error-state lifetime and idle transition.

**Proposed stimulus:** Issue a denied access followed by idle cycles and a legal access.

**Observation/oracle:** Per-transaction expected outcomes and observed error clearing.

**Sources:** [#813](https://github.com/lowRISC/ibex/pull/813). See the manifest for revision/merge status and changed paths.

## IBEX-010: Late memory faults survive an empty decode stage

**Property:** An outstanding older memory operation can still raise a fault when decode has no valid instruction.

**Historical mechanism:** The controller no longer requires a valid decode instruction to process the relevant late LSU exception.

**Applies to:** Optional writeback stage and delayed memory errors.

**Inspect:** Fault qualification versus front-end instruction validity.

**Proposed stimulus:** Empty decode while delaying an older load/store error response.

**Observation/oracle:** A fault attributed to the outstanding instruction, with correct trap PC and address.

**Sources:** [#854](https://github.com/lowRISC/ibex/pull/854). See the manifest for revision/merge status and changed paths.

## IBEX-011: PMP address modes respect boundaries and granularity

**Property:** NA4, NAPOT and TOR matching must use the appropriate mode-specific comparisons and granularity.

**Historical mechanism:** The changes separate equality-based NA4/NAPOT matching from TOR range matching and correct the minimum-granularity NAPOT mask branch.

**Applies to:** Supported PMP modes, including the minimum-granularity configuration.

**Inspect:** PMP masks, equality/range comparisons and generate branches.

**Proposed stimulus:** Probe just below, at and above boundaries, including the smallest legal regions.

**Observation/oracle:** An independently implemented specification address-range model.

**Sources:** [#903](https://github.com/lowRISC/ibex/pull/903), [#1234](https://github.com/lowRISC/ibex/pull/1234). See the manifest for revision/merge status and changed paths.

## IBEX-012: Older faults win across pipeline stages

**Property:** A younger exception must not override an older memory fault or flush away its unresolved outcome.

**Historical mechanism:** The controller prioritizes older writeback faults and waits for writeback readiness or its exception before flushing a younger exception.

**Applies to:** Writeback-stage configurations with simultaneous or delayed exceptions.

**Inspect:** Flush entry, writeback readiness and exception-priority signals.

**Proposed stimulus:** Combine a delayed older LSU fault with a younger illegal instruction or other exception.

**Observation/oracle:** Architectural instruction order determines the trap owner and all associated metadata.

**Sources:** [#919](https://github.com/lowRISC/ibex/pull/919). See the manifest for revision/merge status and changed paths.

## IBEX-013: Interrupt and debug entry respect in-flight memory ownership

**Property:** Control redirection must preserve the completion and ownership of an already active memory operation.

**Historical mechanism:** The change distinguishes retaining decode state from halting fetch and coordinates interrupt/debug handling with ongoing LSU activity.

**Applies to:** Memory stalls around interrupt/debug acceptance.

**Inspect:** ID retention, issue gating and interrupt/debug state transitions.

**Proposed stimulus:** Vary request grants and responses while raising interrupt or debug requests.

**Observation/oracle:** Accepted transactions complete exactly once and are attributed to the correct instruction.

**Sources:** [#928](https://github.com/lowRISC/ibex/pull/928). See the manifest for revision/merge status and changed paths.

## IBEX-014: PMP address write locks use the exact conditions

**Property:** A neighboring TOR entry restricts address writes under the specified lock conditions, without blocking otherwise legal writes.

**Historical mechanism:** The PMP address write guard is corrected so the next TOR entry restricts the write in combination with its lock condition.

**Applies to:** PMP address registers with an adjacent TOR region.

**Inspect:** PMP CSR write-enable logic.

**Proposed stimulus:** Cross own-lock, next-lock and next-mode settings and write/read back the address.

**Observation/oracle:** A specification-derived write-permission truth table.

**Sources:** [#1054](https://github.com/lowRISC/ibex/pull/1054). See the manifest for revision/merge status and changed paths.

## IBEX-015: Competing debug causes select coherent state

**Property:** Concurrent debug causes must select the specified priority and a DPC corresponding to the winning event.

**Historical mechanism:** Debug arbitration changes select the EBREAK instruction PC when appropriate and correct concurrent debug-cause priority.

**Applies to:** EBREAK, halt request, stepping and supported triggers; priority is specification-version dependent.

**Inspect:** Debug cause arbitration and IF/ID PC selection.

**Proposed stimulus:** Exercise overlapping causes at the same instruction boundary.

**Observation/oracle:** A versioned priority table plus independent expected PC for each winning cause.

**Sources:** [#1107](https://github.com/lowRISC/ibex/pull/1107), [#1744](https://github.com/lowRISC/ibex/pull/1744). See the manifest for revision/merge status and changed paths.

## IBEX-016: Read-only CSR fields survive software writes

**Property:** Writes must preserve read-only fields while applying the permitted update to writable fields.

**Historical mechanism:** The DCSR software-write path preserves the existing read-only cause field.

**Applies to:** DCSR and similarly mixed-access CSRs; account for hardware-owned updates separately.

**Inspect:** CSR field merge and write arbitration.

**Proposed stimulus:** Try write/set/clear operations with values that would change read-only fields.

**Observation/oracle:** A field-access model independent of the RTL write mask.

**Sources:** [#1136](https://github.com/lowRISC/ibex/pull/1136). See the manifest for revision/merge status and changed paths.

## IBEX-017: Retirement counters track valid retirement

**Property:** Retirement counting must exclude trapping instructions and must not reuse stale pipeline bookkeeping across bubbles.

**Historical mechanism:** Retirement eligibility is carried with the instruction, qualified against faults, and later corrected to include writeback validity for speculative count bookkeeping.

**Applies to:** Performance counters, optional writeback and late memory faults.

**Inspect:** Retirement qualification, writeback validity and carried count flags.

**Proposed stimulus:** Mix normal instructions, EBREAK/ECALL, faults and bubbles; inspect count deltas.

**Observation/oracle:** An independently derived committed-instruction sequence and counter policy.

**Sources:** [#1141](https://github.com/lowRISC/ibex/pull/1141), [#2446](https://github.com/lowRISC/ibex/pull/2446). See the manifest for revision/merge status and changed paths.

## IBEX-018: Explicit counter writes arbitrate with increments

**Property:** Software writes to an instruction-retirement counter must have the specified priority over concurrent increments.

**Historical mechanism:** The retirement-count qualification excludes relevant CSR write/set/clear operations targeting MINSTRET or MINSTRETH.

**Applies to:** MINSTRET/MINSTRETH accesses and a pipeline that overlaps CSR access with retirement.

**Inspect:** CSR operation decode and counter update qualification.

**Proposed stimulus:** Exercise write/set/clear of each counter half around another retiring instruction.

**Observation/oracle:** A cycle/retirement model applying the specified CSR-write priority.

**Sources:** [#2446](https://github.com/lowRISC/ibex/pull/2446). See the manifest for revision/merge status and changed paths.

## IBEX-019: Debug interrupt tests track the actual debug boundary

**Property:** A test must distinguish interrupt handling inside debug from legal handling after DRET.

**Historical mechanism:** The DV sequence tracks DRET and actual IRQ transactions, terminating the in-debug prohibition when return has occurred.

**Applies to:** DV sequences that raise interrupts during debug, including delayed stimulus.

**Inspect:** DV fork lifetimes, monitored transactions and expected privilege.

**Proposed stimulus:** Vary IRQ assertion/drop relative to DRET and exercise enabled/disabled sources.

**Observation/oracle:** A monitor-derived debug interval and expected post-return interrupt behavior.

**Sources:** [#1309](https://github.com/lowRISC/ibex/pull/1309). See the manifest for revision/merge status and changed paths.

## IBEX-020: Debug fetches see updated program contents

**Property:** A dynamic debug program must not execute stale cached instructions, including on the first entry-cycle fetch.

**Historical mechanism:** Instruction-cache enable is suppressed both while in debug and during the entry transition.

**Applies to:** Instruction cache and mutable debug memory/program buffer.

**Inspect:** Cache-enable gating during entry and established debug mode.

**Proposed stimulus:** Change debug code between entries and observe the first instruction fetched and executed.

**Observation/oracle:** The newly installed debug program contents and the platform cache/debug contract.

**Sources:** [#1813](https://github.com/lowRISC/ibex/pull/1813). See the manifest for revision/merge status and changed paths.

## IBEX-021: Verification traces preserve exception ownership

**Property:** Verification-visible exception information must not describe a younger instruction killed by an older fault.

**Historical mechanism:** The ID exception output is masked when a writeback exception owns the event, avoiding a misleading verification trace for a killed instruction.

**Applies to:** RVFI/co-simulation and writeback exceptions. This source explicitly distinguishes trace correctness from architectural execution.

**Inspect:** ID exception output gating and RVFI consumers.

**Proposed stimulus:** Combine an older writeback fault with a younger decode exception.

**Observation/oracle:** An independently expected architectural trace with only the correct fault owner.

**Sources:** [#1883](https://github.com/lowRISC/ibex/pull/1883). See the manifest for revision/merge status and changed paths.

## IBEX-022: Simulation configuration reaches the DUT

**Property:** Requested ISA and register-file selections must be applied through the actual elaboration parameters.

**Historical mechanism:** Co-simulation parameter forwarding is corrected to use the matching parameter names, with an associated base-ISA default adjustment.

**Applies to:** Co-simulation top-level and parameter/define forwarding.

**Inspect:** Simulation defines, parameter names and defaults.

**Proposed stimulus:** Build contrasting supported configurations and inspect elaborated values and instruction behavior.

**Observation/oracle:** The requested configuration compared with elaboration evidence, not only command-line strings.

**Sources:** [#2501](https://github.com/lowRISC/ibex/pull/2501). See the manifest for revision/merge status and changed paths.

## IBEX-023: CSR stimulus and predictions use the same legal operand

**Evidence status: unmerged proposal, not an accepted upstream fix.**

**Property:** A generator must emit the operand it has constrained for field access and use that same operand in prediction.

**Historical mechanism:** The generator constructs a safe CSR operand and uses it both in emitted assembly and expected-value calculation.

**Applies to:** Generated CSR tests with read-only or constrained fields.

**Inspect:** Generator operand sanitization, emitted assembly and prediction.

**Proposed stimulus:** Generate operands with nonzero protected bits, then inspect emitted instructions and predicted values.

**Observation/oracle:** An independent field-access model plus the actual emitted operand.

**Sources:** [#2442](https://github.com/lowRISC/ibex/pull/2442). See the manifest for revision/merge status and changed paths.

## IBEX-024: Unexpected traps produce an explicit test failure

**Evidence status: unmerged proposal, not an accepted upstream fix.**

**Property:** A generated test must direct unexpected traps to a defined failure path.

**Historical mechanism:** The generated CSR test initializes MTVEC to its existing failure handler, replacing an uninitialized-vector path that could end in timeout.

**Applies to:** Bare-metal CSR tests that do not otherwise establish a trap handler.

**Inspect:** Test setup, MTVEC initialization and failure handler.

**Proposed stimulus:** Cause an unexpected illegal CSR access early in the generated program.

**Observation/oracle:** An explicit failure marker reached through the configured trap vector, rather than an eventual timeout.

**Sources:** [#2439](https://github.com/lowRISC/ibex/pull/2439). See the manifest for revision/merge status and changed paths.

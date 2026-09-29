# CV32E40P source-reviewed candidate checklist

Snapshot: 2026-09-29. Five retrieval groups yield **five candidate entries: four new relative to the public Ibex checklist and one extension**. This is an editorial mechanism comparison, not a model score or a count of newly discovered bugs. None is independently reproduced. See [review decisions](deep-read.md).

## CV32E40P-001: Cancelled hardware-loop instructions leave loop state unchanged

**Disposition:** extension. **Evidence:** source-reviewed, fix-linked.

**Property:** An instruction cancelled by interrupt or debug entry must not update hardware-loop state; saved resume state and loop state must describe the same execution boundary.

**Applicability:** Hardware-loop extension and interrupt/debug cancellation of a loop setup instruction. #888 reports XPULP=1, cluster=0, FPU=0, Zfinx=0. Historical parameter names must be mapped to the target revision.

**Mechanism:** #195 masks loop write enables on interrupt entry and requires ID readiness before selecting instruction-originated loop updates. #888 reports cv.end updating the end CSR despite trigger cancellation. #897 deasserts is_decoding_o on debug entry for COREV_PULP in two controller paths. The issue closure links that change to #888; the full downstream gate cone has not been independently proven.

**Review locations:** Controller cancellation decisions, loop write enables and data/source muxes, CSR update path, saved PC.

**Stimulus:** Arrange an interrupt at a loop setup instruction, then separately an instruction-address debug trigger on cv.end. Sweep the cancellation boundary; include an uncancelled control and resume/re-execution. Cover start/end/count state and both supported loops as proposed extensions.

**Observation and oracle:** Observe accepted cancellation, saved PC, and every loop CSR before/after. An independent execution-boundary model requires no cancelled instruction effect and exactly one effect when it later executes. Distinguish legitimate concurrent CSR writes.

**Upstream verification evidence:** #888 supplies a timed sequence, configuration, affected revision and OneSpin 2023.3_1 attribution; closure names #897. #195 supplies no replayable regression in the collected PR evidence.

**Verification record:** Not run: proposed stimulus and oracle only. Cached source bodies, discussions and relevant final PR diffs reviewed; no RTL simulation or formal run performed.

**Lineage and duplicates:** Extension of the execution-boundary theme in IBEX-001/012/013, not an identical Ibex fix. Merge #195 and #888 into one property with separate interrupt/debug evidence; do not count two new properties or infer identical root causes. Historical RI5CY/PULP ancestry is relevant.

**Limitations:** #195 explicitly frames the update suppression as verification consistency and does not establish harmful functional behavior. #888 screenshot not inspected. Generalized stimuli beyond cv.end/interrupt gating are proposals. No claim of an unfixed defect at snapshot HEAD.

**Sources and revisions:**

- [Upstream report](https://github.com/openhwfoundation/cv32e40p/issues/888): reported affected revision `ebdbbb7aabdf20fa127a6c7e9c641f89d2b62f8a`.
- [merged source change](https://github.com/openhwfoundation/cv32e40p/pull/195): base `aa13a06b4ca5bacdc59a92fd7aff75adb140cd7f`, PR head `eb07d277b462f227dae482dec987a34181d3f1a6`, merge `ab9d13a4ecf289bbe488ce3f5dc7e4c65220b6bc`.
- [merged source change](https://github.com/openhwfoundation/cv32e40p/pull/897): base `3023e88a8ce07c6854267031637403ea6a8061bb`, PR head `e6f280007d37052222c4295d8af2618186d9abfd`, merge `688a28a5815d21e0ed939270827da26781b77076`.

## CV32E40P-002: A zero hardware-loop count must not underflow

**Disposition:** new_candidate. **Evidence:** source-reviewed, fix-linked.

**Property:** At a loop-end event, an already-zero loop counter stays zero; an eligible final iteration with count one reaches zero exactly once.

**Applicability:** Hardware-loop extension with the reported zero-count semantics. Requires an independently specified loop-end convention and legal setup sequence; not a rule for all unsigned counters.

**Mechanism:** #880 reports lpcount0 changing from zero to 0xffffffff while the reference stays zero. #881 adds nonzero qualification to both loop decrement enables in the affected controller path.

**Review locations:** Loop-end comparators, decrement qualification, stall/redirect paths, both loop banks.

**Stimulus:** Configure counts 0, 1 and 2; execute the loop end with distinct signatures and compare state. Add stalls and nested-loop configurations only within documented restrictions.

**Observation and oracle:** Check count and PC against a small independent loop model, and prove the loop-end event was reached. Zero must not wrap; count one must still complete normally. A disabled decrement for all counts must fail the controls.

**Upstream verification evidence:** #880 includes DUT/reference CSR mismatch, core-v-verif revision 117ad5b120922d48e63edc0a91a81ebbd6616b5b, randomized-test command and seed 1; closure names #881. Test and attachments were not rerun/read.

**Verification record:** Not run: proposed stimulus and oracle only. Cached source bodies, discussions and relevant final PR diffs reviewed; no RTL simulation or formal run performed.

**Lineage and duplicates:** New relative to the 24 Ibex entries. IBEX-017/018 concern retirement/performance counters, not hardware-loop architectural semantics.

**Limitations:** Only the reported zero-count mismatch and matching fix were reviewed. Broader stall/nesting coverage and the target manual contract require validation. No claim of an unfixed defect at snapshot HEAD.

**Sources and revisions:**

- [Upstream report](https://github.com/openhwfoundation/cv32e40p/issues/880): reported affected revision `c520546c0cc3f64ef064d52dfdc91abbba63f181`.
- [merged source change](https://github.com/openhwfoundation/cv32e40p/pull/881): base `8a6f74b421ab7a6256b80a369234e8ff51dafd4e`, PR head `767fb0fd85d981d548ae942eb748b847a29b71f4`, merge `7df7d2dfe036da981279e89703bb5e774e4712dc`.

## CV32E40P-003: JALR observes the latest producer despite shared writeback contention

**Disposition:** new_candidate. **Evidence:** source-reviewed, fix-linked.

**Property:** A control-transfer operand must reflect its architecturally preceding producer even when an unrelated long-latency result competes for the writeback path.

**Applicability:** In-order design with a long-latency FPU/APU sharing writeback resources and an early JALR operand path. Reported configuration is pulp_fpu_zfinx_1cyclat; applicability outside it must be checked.

**Mechanism:** #889 reports fdiv writeback delaying an addi result, followed by JALR using the old x16 despite a trace showing its new value. #897 routes the decoded control-transfer type to EX and extends APU-result buffering/valid suppression for JALR with an integer ALU write and no APU read dependency.

**Review locations:** Writeback arbitration, buffered APU result lifetime, JALR dependency/stall logic and actual target operand.

**Stimulus:** Overlap a long-latency FP completion with addi updating a JALR source. Sweep completion timing. Compare with no-contention control and a separate case where JALR depends on the FP producer.

**Observation and oracle:** Use distinct old/new executable targets with independent signatures and expected JALR target calculation. Observe actual redirect/fetch and retirement, not just trace register values; also check both producers eventually commit once.

**Upstream verification evidence:** #889 provides an ISS PC mismatch, core-v-verif revision 02ee75284e34acf908dda5344f642a7cb3b0ac0c and randomized-test seed 1567674295. Closure names #897; no replay performed.

**Verification record:** Not run: proposed stimulus and oracle only. Cached source bodies, discussions and relevant final PR diffs reviewed; no RTL simulation or formal run performed.

**Lineage and duplicates:** New relative to the 24 Ibex entries. Separate from CV32E40P-004: arbitration can hide an integer producer even if FP dependencies are known. Sharing PR #897 with cancellation does not make this the same defect.

**Limitations:** Waveform screenshots not inspected; exact cycle behavior is an upstream report corroborated by a targeted diff, not independent reproduction. Other #897 changes are excluded. No claim of an unfixed defect at snapshot HEAD.

**Sources and revisions:**

- [Upstream report](https://github.com/openhwfoundation/cv32e40p/issues/889): reported affected revision `7df7d2dfe036da981279e89703bb5e774e4712dc`.
- [merged source change](https://github.com/openhwfoundation/cv32e40p/pull/897): base `3023e88a8ce07c6854267031637403ea6a8061bb`, PR head `e6f280007d37052222c4295d8af2618186d9abfd`, merge `688a28a5815d21e0ed939270827da26781b77076`.

## CV32E40P-004: Custom operand routing participates in long-latency dependency checks

**Disposition:** new_candidate. **Evidence:** source-reviewed, fix-linked.

**Property:** Every actual source-register dependency of a custom instruction must be represented in hazard detection, including alternate operand-mux paths, before the consumer executes.

**Applicability:** XPULP custom arithmetic plus multi-cycle FPU with Zfinx integer-register sharing. #730 reports XPULP=1, cluster=1, FPU=1, Zfinx=1.

**Mechanism:** #730 reports fdiv.s producing x5 after cv.addunr has already consumed its stale value. #841 adds OP_A_REGC_OR_FWD to the APU dependency mapping and changes the corresponding operand-C valid qualification. Physical source mapping must be traced through the target decoder; signal suffixes alone are insufficient.

**Review locations:** Custom decode source mapping, operand mux controls, APU read-register vectors and valid bits, producer completion/stall logic.

**Stimulus:** Use the reported fdiv.s x5 -> cv.addunr consuming x5 pattern with old/new values chosen to produce different outputs. Enumerate actual source routes for ADD/SUB variants and include independent-source controls.

**Observation and oracle:** Independently decode the instruction sources and compute its arithmetic result from the completed producer value. Observe producer availability and consumer acceptance to prove the intended overlap.

**Upstream verification evidence:** #730 attributes its trace to OneSpin 2022.3_1 and provides a VCD attachment not inspected here. Discussion first mentions commit 6cfb7438ba62fb433823c85d04e2e001d56e5b81 with verification still ongoing, and later explicitly resolves via #841. No formal results replayed.

**Verification record:** Not run: proposed stimulus and oracle only. Cached source bodies, discussions and relevant final PR diffs reviewed; no RTL simulation or formal run performed.

**Lineage and duplicates:** New relative to the 24 Ibex entries. Related to CV32E40P-003 by shared resources, but this property concerns complete dependency declaration rather than contested writeback of a different producer.

**Limitations:** #730 leaves the affected git hash as TBU. A historical failing revision cannot be assigned from the PR base alone. Broader variants and cluster-off applicability remain proposed checks. No claim of an unfixed defect at snapshot HEAD.

**Sources and revisions:**

- [Upstream report](https://github.com/openhwfoundation/cv32e40p/issues/730): reported affected revision `not supplied`.
- [merged source change](https://github.com/openhwfoundation/cv32e40p/pull/841): base `25907a07dc1e4557141e2bca957f35ce28cf6dad`, PR head `0491837ebe928770ef46d57efecb73f43839c9b8`, merge `c02a42b6e846b9c71b9726bfefbafbc0a4e127e3`.

## CV32E40P-005: Split memory accesses retain their address owner across FP completion

**Disposition:** new_candidate. **Evidence:** source-reviewed, fix-linked.

**Property:** Every beat of a split memory operation must derive its address from that operation, without contamination by another execution-unit result; deferred results must remain intact until accepted.

**Applicability:** Implemented split misaligned accesses overlapping multi-cycle FP/APU completion. #723 reports XPULP=0, cluster=0, FPU=1, Zfinx=1. Trap-on-misalignment targets need a different property.

**Mechanism:** #723 reports fsqrt.s followed by a misaligned lw: second address 0x80000004 rather than 0xa0002000. #824 initially blocks misaligned LSU requests while the APU is busy. #860 explicitly removes that fix and instead buffers multi-cycle APU results/flags and suppresses their acceptance during misaligned phases (among other conflicts). The diff supports a result-arbitration repair; exact internal address contamination is still an upstream explanation.

**Review locations:** Split-access address generation/state, EX result arbitration, APU response buffer and valid/flag lifetime, bus acceptance.

**Stimulus:** Overlap fsqrt completion with each phase of a crossing-word load. Sweep response/grant delays and choose FP result bits unrelated to the address. Add stores as a proposed extension and aligned/no-FP controls.

**Observation and oracle:** A bus scoreboard derives accepted beat addresses/byte enables from the original effective address and access size, then checks loaded bytes or written memory independently. Observe both accepted beats and eventual FP result/flags; a final register-only check is insufficient.

**Upstream verification evidence:** #723 supplies affected revision, configuration, a sequence and OneSpin 2022.3_1 attribution. Closure explicitly names #860. The collected evidence does not include a replayed before/after regression.

**Verification record:** Not run: proposed stimulus and oracle only. Cached source bodies, discussions and relevant final PR diffs reviewed; no RTL simulation or formal run performed.

**Lineage and duplicates:** New relative to the 24 Ibex entries. IBEX-009/013 concern fault lifetime and interrupt/debug around memory; they do not cover split-address ownership under FP arbitration. #824 is superseded by #860, not independent confirming evidence. Later #881/#897 further refine shared APU buffering conditions; do not treat #860 as the final general arbitration implementation.

**Limitations:** VCD not inspected. No proof of all misaligned loads/stores or all FPU modes. Other issues and vendor fixes bundled in #860 are outside this entry. No claim of an unfixed defect at snapshot HEAD.

**Sources and revisions:**

- [Upstream report](https://github.com/openhwfoundation/cv32e40p/issues/723): reported affected revision `d0d1c25374e3770c4335568ef16e84404cedbdea`.
- [superseded fix](https://github.com/openhwfoundation/cv32e40p/pull/824): base `d011f05092839e7c9ec1af380aebcfc129ab6582`, PR head `00bb726c53ed45ab6ff9674bb9f71693141e6b22`, merge `b883519a4cd784453f8c3253e10eec7cdc8509c9`.
- [merged source change](https://github.com/openhwfoundation/cv32e40p/pull/860): base `c36466bd930e9204fdf63d1b2f33535196a03060`, PR head `f3a904fe5293f93cd4f0488af1a4ad21df281982`, merge `9470ac13a5ceaa400a0734a38ae2c5866bf2f54b`.

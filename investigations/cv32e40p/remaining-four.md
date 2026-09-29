# Remaining four seed groups: functional review decisions

Date: 2026-09-29. This completes a bounded reading of the original nine retrieval groups, not a comprehensive review of the 1,052-record index. The evidence below is the previously collected snapshot plus the final diff and PR metadata for #977. No additional Jev requests were made. This pass excludes security assessment and modified-RTL experiments.

## Decisions

| Source | Evidence classification | Checklist disposition |
|---|---|---|
| [#1064](https://github.com/openhwfoundation/cv32e40p/issues/1064) | Unresolved integration report; no established fix/root cause in captured discussion | Retain fetch-stall/JALR functional review lead; do not count as a confirmed core defect |
| [#975](https://github.com/openhwfoundation/cv32e40p/issues/975), [#977](https://github.com/openhwfoundation/cv32e40p/pull/977) | Reported functional failure with a merged targeted correction | Extend CV32E40P-002 with CSR-flush completion qualification; this added case is not independently reproduced |
| [#466](https://github.com/openhwfoundation/cv32e40p/issues/466) | Upstream explicitly describes observed completion ordering as by design | Retain checker-contract guidance; do not require all implementations to finish independent instructions in order |
| [#920](https://github.com/openhwfoundation/cv32e40p/issues/920) | Discussion of intended custom-instruction behavior/encoding choice | Applicability-specific specification question; not a confirmed RTL defect or automatic illegal-encoding test |

No new standalone checklist ID is added in this pass. One existing entry gains a distinct functional case; the other reports remain contextual guidance or an unresolved lead.

## #1064: return under instruction-fetch stalls

The report describes a skipped `ret` with an integrated cache that stalls. The discussion asks for configuration and points to the verification environment; the reporter states default parameters and a hello-world program with random memory stalls. The captured material does not supply a pinned failing SHA, complete cache/driver implementation, or a reviewed correction. Screenshots were not inspected. A core bug, an integration/protocol issue and other explanations cannot be distinguished from this evidence.

A portable functional question is nevertheless useful: does an accepted return instruction eventually redirect to the architectural target when instruction requests or responses are delayed, without wrong-path architectural effects? A directed test should use a known target signature, explicitly count accepted target requests, prove stalls were exercised and include a no-backpressure control. Observe architectural completion as well as internal redirect signals. Respect the target's bus contract; do not assume the reporter's cache integration is correct. This is a test proposal, not an upstream reproduction claim.

## #975: loop-end CSR flush must still complete the loop update

The report identifies tag `cv32e40p_v1.7.0` and core-v-verif revision `6d973dda74bb666697f93d8ba0ba6131933ca4ad`. It describes an inner loop ending in a flushing CSR access, with DUT count 10 versus reference count 9 and a nonterminating run without ISS checking. The closure explicitly names #977.

The final #977 diff changes the ID-stage qualification of the hardware-loop register valid signal to include `csr_status` in addition to instruction validity before applying the clear/consumption qualification. This is evidence of a completion-qualification correction; it is not the same zero-underflow mechanism as #880. Both belong under the broader question of whether the loop count updates exactly once for an eligible loop-end instruction.

Proposed added case: compare a loop ending in a normal instruction with one ending in a documented flushing CSR access; use counts 1 and greater than 1, independently expected iteration counts and a bounded completion timeout. Inspect both CSR effects and loop count. Instruction-valid deassertion during the flush must not silently lose the architectural loop completion. No claim is made that the existing zero-count component test covers the ID-stage wiring or this case.

PR #977 is merged: base `b11c5f3d49a0c11ad76afd65995e7e15c379f723`, head `ad7efbf0aee56be9cde52e55994685751412fc6d`, merge `58cb2f1ab1eb5026b247a2f05ab4e624e6438494`. [Supplemental provenance](remaining-four.json) records the diff hash. Only PR metadata/final diff were additionally fetched; PR review history and the original test were not retrieved/replayed.

## #466: distinguish completion ordering from an architectural failure

The report shows a delayed load followed by an independent CSR or ALU instruction and explicitly does not demonstrate a functional defect. Upstream explains that the observed ordering is by design and discusses the consequences for whole-state ISS comparison. Thus, converting this report to “all later writes must wait for every earlier load” would invent a requirement.

The useful review question is whether trace/checker sampling matches the implementation's architectural observation contract. Comparing a whole register file at an intermediate completion event may require different bookkeeping than checking the owning instruction's result. This relates to event ownership and reference-model integration themes already present in the atlas; it does not prove a checker bug in another design. No blanket suppression of mismatches is proposed.

## #920: same pointer/destination in a custom post-increment load

This is a design-choice discussion about whether a post-increment load with equal destination/base register indices should be legal. A comment initially invokes register contents in the legality argument, and subsequent discussion corrects that to register indices. Do not carry the initial argument into a checklist as fact. The discussion also notes compiler-generation considerations.

Before writing a test, obtain the applicable versioned extension specification and establish the permitted encoding and writeback precedence for the equal-index case. The linked manual screenshot/latest page was not reviewed here, so this pass does not assert a normative final-value rule. Targets without these custom instructions have no direct instance of this question. The thread is not evidence that the core currently mishandles the case.

## Scope and next boundary

The five original candidate entries remain; one has the previously published zero-count component reproduction. The CSR-flush extension is source-reviewed/fix-linked only. #1064 remains unresolved, and #466/#920 are not classified as defects. “All seed groups read” does not mean all referenced evidence or all core behavior was validated.

Select further work by target applicability, not by issue count. Ordinary fetch-flow and checker-contract questions transfer more broadly than hardware-loop or post-increment extensions. For #1064 specifically, collect the missing versioned integration evidence before attributing the report to core RTL. No upstream contact or issue submission was made.

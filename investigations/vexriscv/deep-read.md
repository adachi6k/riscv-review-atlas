# VexRiscv: three-group source review

Date: 2026-09-29. [Investigation #11](https://github.com/adachi6k/riscv-review-atlas/issues/11).

## Outcome

The selected three groups yield [three candidate entries](checklist.md): one new bus-size property and two extensions of response/topology ownership themes. They are source-reviewed only; VEX-001 and VEX-003 link to an explicit historical correction. VEX-002 records an integration contract, not a confirmed core defect. No simulations, generator elaborations, security assessments or modified-RTL experiments were performed. Additional Jev calls: zero.

## #191: exact correcting commit recovered

The bounded July 2021 commit query found [3028c19389ae5a6589c561db5c65ab573a6af913](https://github.com/SpinalHDL/VexRiscv/commit/3028c19389ae5a6589c561db5c65ab573a6af913), whose message explicitly names #191. The single changed assignment in `DataCacheMemBus.toAxi4Shared` replaces the maximum of internal command size and bus-byte-width logarithm with the latter alone. Nearby code retains a separate burst-length assignment and write byte masks.

This supports a specific bridge-size interpretation correction. It does not justify a universal rule that all AXI transactions must have full-width beats. Applicability depends on the adapter's documented transfer policy. The test proposal varies line size independently from bus width and checks command fields plus transferred bytes. The fixing SHA and parent are recorded in [deep-sources.json](deep-sources.json); introduction was not bisected, and neither revision was executed.

## #318 / #158: a response contract, not two bugs

The #318 maintainer identifies write responses produced by the testbench in a configuration that does not expect them; the reporter says adapting the driver fixes the symptom. The pinned public HEAD's cache configuration derives `withWriteResponse` from `withExclusive`. Its BMB adapter records write context and filters corresponding responses when write responses are disabled. This is corroborating current source context, not a recovered failing revision of the original report.

The historical #158 base waits for response completion and checks response errors only for non-store operations. The rejected proposal removes that qualification and chooses a store fault code based on the current operation, but does not establish an acknowledged-write protocol. Its discussion explains why the proposed behavior is outside that interface contract. The PR is unmerged. A GitHub `merge_commit_sha` field for an unmerged PR must not be interpreted as a landed repair; [checklist.json](checklist.json) records base/head and `merged: false` instead.

The portable review question is agreement among core, bus adapter, driver and reference checker about response eligibility and ownership. Tests should use normal contract-conforming transactions; deliberately issuing unsupported responses is not part of this work.

## #86: topology changes need both functional and selection evidence

The merged diff adapts several plugins to absent stages. The reviewed hazard helper treats a null runtime-bypass qualifier as true; the changed call uses that behavior when memory is the final stage. Multiplier plugins adapt bypass metadata and result/flush placement. Cache changes align merged stages, data/tag timing, MMU/management ownership and configuration restrictions. These are related topology assumptions, not proof that every modified path had a runtime bug.

The regression source adds a `MulDivFpgaSimple` expression ending in `:: l`, but at the reviewed merge revision it does not assign the resulting list back to `l`. Later options explicitly assign to `l`, and selection ends in `random(r, l)`. This source-level observation means the added expression alone is not evidence that the new option is selectable through this list. It is a historical coverage concern, **not an executed failing test or a current-HEAD defect claim**. We did not run Scala, inspect all constructor side effects, or trace every alternative selection route. Accordingly, require an actual generated configuration manifest before crediting coverage.

The discussion also narrows the original author's successful setup to instruction cache only; do not generalize that statement to the data-cache adaptations. A successful generator build and a functional dependency/stall regression are separate evidence levels.

## Evidence boundary and next work

Issue bodies/conversation comments, selected final PR diffs, the exact #191 correcting diff and five pinned surrounding source files were read. Source hashes and revisions are retained. Attachments, inline review history, complete ancestor history and upstream execution logs were not independently validated.

For a target transfer, first determine which bridge/response policies and optional pipeline stages actually exist. VEX-001 is the most focused next check when a burst/width-converting bridge is present. VEX-002 is broadly useful for integration-contract review, while VEX-003 needs genuine configurable topology. No private target identity or implementation details are published here. Do not assume all three represent missing tests in another core.

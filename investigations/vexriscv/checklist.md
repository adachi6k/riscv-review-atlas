# VexRiscv source-reviewed candidate checklist

Three entries from three reading groups: one new bus-size property and two extensions of existing ownership/configuration themes. None is independently reproduced. These are review candidates, not three newly discovered defects. See [review decisions](deep-read.md).

## VEX-001: Preserve beat-size meaning across a cache-to-bus bridge

**Property:** A bridge must encode each outgoing beat size according to the bus width and supported transfer policy, while representing the overall transfer length separately.

**Applicability:** Cache refill/burst adapter to AXI. The historical bridge uses full-width beats. Narrow-transfer adapters must use their own contract rather than copying the constant-size implementation.

**Mechanism:** #191 reports a 32-bit interface emitting size 5 instead of size 2. Commit 3028c193 explicitly names #191 and replaces max(internal command size, log2(memory bytes)) with log2(memory bytes); burst length remains a separate assignment. This supports a size-domain confusion mechanism.

**Review locations:** DataCacheMemBus.toAxi4Shared: internal size/beat-count interpretation, outgoing command size/length, byte enables and data width.

**Stimulus:** For supported configurations, vary cache-line length independently of memory bus width; exercise refill and supported writes with normal ordered responses and backpressure. Include single-beat and multi-beat transfers.

**Observation and oracle:** An independent transaction scoreboard computes legal bytes per beat from the bus contract and total transferred bytes from accepted beats/byte enables. Check command fields and actual transfer counts, not just final load data.

**Verification record:** Not run: source review only. No generator elaboration, RTL simulation or before/after execution performed.

**Lineage and duplicates:** New specific property relative to the public Ibex/CV32E40P entries. CV32E40P-005 addresses split-address ownership, not bus size translation.

**Limitations:** No independent reproduction or current-HEAD defect claim. No statement that every AXI transfer must be full bus width. The upstream issue provides two revisions; exact introduction has not been bisected.

**Evidence:** source-reviewed, fix-linked.

**Sources:**

- [Source](https://github.com/SpinalHDL/VexRiscv/issues/191)
- [Source](https://github.com/SpinalHDL/VexRiscv/commit/3028c19389ae5a6589c561db5c65ab573a6af913)
- [Source](https://github.com/SpinalHDL/VexRiscv/blob/3028c19389ae5a6589c561db5c65ab573a6af913/src/main/scala/vexriscv/ip/DataCache.scala)
Exact revisions and roles are retained in [checklist.json](checklist.json), [deep-sources.json](deep-sources.json) and [initial provenance](sources.json).

## VEX-002: Match response production to the configured request contract

**Property:** Core, adapter, testbench and reference checker must agree which accepted commands produce responses and which operation owns each response.

**Applicability:** Interfaces whose write-response behavior depends on cache/coherency configuration, or bridges translating between acknowledged external writes and a read-response-only core interface.

**Mechanism:** #318 identifies a testbench emitting write responses in a non-exclusive cache configuration that expects none; the reporter says correcting the driver resolves the symptom. Pinned current DataCache defines withWriteResponse from withExclusive and its BMB bridge filters write responses when disabled. #158 is an unmerged proposal: historical DBusSimplePlugin waits/checks response faults for reads, not ordinary writes.

**Review locations:** Configuration flags, response context/tags, bridge filtering, pending-operation ownership, simulator bus driver and error-checker assumptions.

**Stimulus:** Run ordinary store-then-load sequences using the documented response policy in each supported configuration. On an acknowledged external bus, verify the bridge consumes write acknowledgements without forwarding them as load data when the core does not expect write responses.

**Observation and oracle:** Independent command ledger derives expected response count/type from the interface contract. Check returned load data against a byte-addressed memory model and count correctly translated responses. An unsupported store-fault mode must not be reported as a failed promised feature.

**Verification record:** Not run: source review only. No generator elaboration, RTL simulation or before/after execution performed.

**Lineage and duplicates:** Extends existing response-ownership and checker-contract themes rather than counting #318 and #158 as two RTL bugs. No shared implementation lineage with Ibex is asserted.

**Limitations:** No illegal-response or modified-RTL experiment performed. Current pinned context corroborates a contract; it does not pin the unreported historical SHA of #318. Do not infer identical response policy for every bridge or optional atomic mode.

**Evidence:** source-reviewed.

**Sources:**

- [Source](https://github.com/SpinalHDL/VexRiscv/issues/318#issuecomment-1450684467)
- [Source](https://github.com/SpinalHDL/VexRiscv/issues/318#issuecomment-1450756276)
- [Source](https://github.com/SpinalHDL/VexRiscv/pull/158)
- [Source](https://github.com/SpinalHDL/VexRiscv/blob/baf7dc82f855eddaf5b0a20a6802c526f127e38a/src/main/scala/vexriscv/ip/DataCache.scala)
- [Source](https://github.com/SpinalHDL/VexRiscv/blob/d2855fcfca5410c6986b0c3e816cbb867e9b22b9/src/main/scala/vexriscv/plugin/DBusSimplePlugin.scala)
Exact revisions and roles are retained in [checklist.json](checklist.json), [deep-sources.json](deep-sources.json) and [initial provenance](sources.json).

## VEX-003: Keep result and control ownership coherent when pipeline stages are removed

**Property:** Every supported generated pipeline topology must attach results, hazards, stalls, flushes and exceptions to stages that exist and preserve the architectural dependencies of those operations.

**Applicability:** Configurable pipeline with optional memory/writeback stages and plugin-specific requirements. Unsupported combinations should be rejected explicitly; fixed-topology cores need only the corresponding shared invariant.

**Mechanism:** #86 changes last-stage hazard handling, multiplier result placement, iterative-unit flush attachment, and cache stage mappings. The cache can merge execute/memory timing when writeback is absent, with early-mux/hit restrictions. This is a collection of related topology adaptations, not a single independently reproduced runtime defect.

**Review locations:** HazardSimplePlugin runtime bypass qualification; MulSimplePlugin injection/final stage; MulDivIterativePlugin flush stage; DBusCachedPlugin management/MMU/exception stages; cache tag/data/request alignment.

**Stimulus:** Enumerate supported topologies explicitly; generate each with exact plugin settings and run dependent MUL/DIV consumers, load/store sequences, normal stalls and applicable flush/exception cases. Record actual generated stage/plugin manifests before functional runs.

**Observation and oracle:** Check elaboration separately from execution. Use independently computed arithmetic/memory signatures and one-time completion, then show each required topology was actually generated and exercised. A random generator containing an option declaration is not evidence that the option was sampled.

**Verification record:** Not run: source review only. No generator elaboration, RTL simulation or before/after execution performed.

**Lineage and duplicates:** Related to CV32E40P-003/004 dependency questions, but extends them to topology-dependent ownership. Configuration reachability also extends IBEX-022. Do not count every modified plugin as a separate bug.

**Limitations:** No generator/toolchain run or functional reproduction. The reporter narrowed their tested setup to instruction cache only. A candidate-list reachability concern in the merged test generator is documented in deep-read.md; no current regression failure is claimed.

**Evidence:** source-reviewed, fix-linked.

**Sources:**

- [Source](https://github.com/SpinalHDL/VexRiscv/pull/86)
- [Source](https://github.com/SpinalHDL/VexRiscv/blob/49944643d222fc72b800bb2fa1880f6ef91618c6/src/test/scala/vexriscv/TestIndividualFeatures.scala)
- [Source](https://github.com/SpinalHDL/VexRiscv/blob/49944643d222fc72b800bb2fa1880f6ef91618c6/src/main/scala/vexriscv/plugin/HazardSimplePlugin.scala)
Exact revisions and roles are retained in [checklist.json](checklist.json), [deep-sources.json](deep-sources.json) and [initial provenance](sources.json).

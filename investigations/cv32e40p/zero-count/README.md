# Zero-count hardware-loop component reproduction

On 2026-09-29, the **unmodified historical controller and hardware-loop register modules** reproduced the zero-count underflow mechanism from [CV32E40P #880](https://github.com/openhwfoundation/cv32e40p/issues/880). The same harness passed on the merged [#881](https://github.com/openhwfoundation/cv32e40p/pull/881) revision.

This is ordinary functional verification. No security assessment or modified-RTL experiment is included.

## Results

| Revision | Count 0, no stall / 2 stalled cycles | Count 1 and 2, both timing cases |
|---|---|---|
| Reported affected `c520546c0cc3f64ef064d52dfdc91abbba63f181` | Both detect `0xffffffff` instead of zero | All four pass |
| Merged fix `7df7d2dfe036da981279e89703bb5e774e4712dc` | Both retain zero and pass | All four pass |

**12/12 outcomes match the declared expectations:** two historical failures detected and ten functional passes. This does not mean the affected RTL passed all tests. Counts 1 and 2 exercise normal decrement behavior and prevent an implementation that simply never decrements from satisfying all cases. Each case also checks the unchanged outer counter and absence of an extra decrement after leaving the end. Results, source SHA-256 values, tool version and observations are in [results.json](results.json).

## Harness and independent expectation

[tb.sv](tb.sv) instantiates the real upstream controller and loop-register module with COREV_PULP=1, COREV_CLUSTER=0, FPU=0. It does not force internal controller state. After reset and fetch enable, it configures an active outer loop with count 3, start 0x100 and exclusive end 0x140. The inner loop spans 0x104 through 0x10c (exclusive end 0x110) with initial count 0, 1 or 2. The outer loop supplies a normal path into DECODE_HWLOOP even when the inner count is zero.

The harness drives sequential instruction PCs through 0x100, 0x104, 0x108 and 0x10c. At the inner end it optionally withholds instruction consumption for two cycles, verifies state retention, and accepts the end once. A reachability check requires DECODE_HWLOOP, active decoding and no ID halt. The expected post-consumption count is derived independently as zero for initial zero, otherwise initial count minus one. The test observes the actual upstream register state, not a reimplementation of its decrement logic.

The loop-register `valid_i` models instruction consumption. The upstream ID stage uses `instr_valid_i & clear_instr_valid_o`, with clear including ID readiness. The test drives this consistently for its ordinary no-halt/no-branch path; it does not instantiate that ID-stage wiring or validate every cancellation path. Unused controller inputs are explicitly tied off; clock, reset, readiness, PC and loop-state ports are connected by a generated wrapper. Upstream assertions are enabled. Reset is explicitly pulsed before the first clock edge so one-hot debug-state assertions see initialized state.

## Re-run

Prerequisites: Python 3, Verilator with timing support, a C++ compiler and make. Tested with the version recorded in results.json.

```sh
python3 investigations/cv32e40p/zero-count/run.py
```

[run.py](run.py) fetches only three public RTL files at each pinned revision if absent. It checks their hashes against [source-hashes.json](source-hashes.json), compiles separate binaries and runs the twelve cases. Source files, generated bindings, build output and detailed logs stay under ignored `.local/cv32e40p/zero-count/`. Network access is needed only for missing source files; cached reruns are offline. Upstream source retains its upstream license and is not redistributed in this directory.

The runner only accepts a historical failure when the end was reached, the counter mismatch marker appeared, the process exited unsuccessfully and no PASS marker appeared. A build error, timeout or unrelated assertion is not a successful reproduction. Any unexpected case makes the runner fail.

## Limits

This is a bounded **controller-plus-register component reproduction**, not the original randomized core-v-verif test, instruction execution, ISS comparison, or full-core proof. The externally driven PC sequence does not validate the fetch unit's reaction to hardware-loop redirects. The test covers inner bank 0 while outer bank 1 is active, not the symmetric bank case, all legal nesting combinations, simultaneous setup/decrement, interrupts, debug or arbitrary backpressure. It demonstrates the zero-count update mechanism without requiring the FPU present in the original report's configuration. It does not identify a new unfixed defect or establish behavior at current master.

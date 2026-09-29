#!/usr/bin/env python3
"""Fetch pinned public RTL and run a bounded controller + loop-register test."""
import argparse
import hashlib
import json
import pathlib
import re
import resource
import subprocess
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REVISIONS = {
    "affected": "c520546c0cc3f64ef064d52dfdc91abbba63f181",
    "fixed": "7df7d2dfe036da981279e89703bb5e774e4712dc",
}
FILES = ["rtl/include/cv32e40p_pkg.sv", "rtl/cv32e40p_controller.sv", "rtl/cv32e40p_hwloop_regs.sv"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=pathlib.Path, default=ROOT / ".local/cv32e40p/zero-count")
    args = parser.parse_args()
    cache = args.cache.resolve()
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    expected_hashes = json.loads((HERE / "source-hashes.json").read_text())
    hashes = {}
    for label, rev in REVISIONS.items():
        d = cache / label
        d.mkdir(parents=True, exist_ok=True)
        hashes[label] = {}
        for path in FILES:
            f = d / pathlib.Path(path).name
            if not f.exists():
                url = f"https://raw.githubusercontent.com/openhwfoundation/cv32e40p/{rev}/{path}"
                f.write_bytes(urllib.request.urlopen(url, timeout=60).read())
            hashes[label][path] = hashlib.sha256(f.read_bytes()).hexdigest()
            if hashes[label][path] != expected_hashes[label][path]:
                raise SystemExit(f"Source hash mismatch: {label}/{path}")
    rows = []
    for label in ["affected", "fixed"]:
        d = cache / label
        header = (d / "cv32e40p_controller.sv").read_text().split("module cv32e40p_controller", 1)[1].split(");", 1)[0]
        ports = re.findall(r"^\s*(input|output)\s+(?:logic\s*(?:\[[^\]]+\]\s*)*|PrivLvl_t\s+)(\w+)\s*[,\n]", header, re.M)
        assert len(ports) > 90
        driven = {"clk", "rst_n", "fetch_enable_i", "instr_valid_i", "id_ready_i", "id_valid_i", "pc_id_i", "hwlp_start_addr_i", "hwlp_end_addr_i", "hwlp_counter_i", "hwlp_dec_cnt_o"}
        constants = {"clk_ungated_i": "clk", "current_priv_lvl_i": "PRIV_LVL_M", "ex_valid_i": "1'b1", "wb_ready_i": "1'b1"}
        bindings = []
        for direction, name in ports:
            value = name if name in driven else constants.get(name, "'0" if direction == "input" else "")
            bindings.append(f".{name}({value})")
        (d / "controller_instance.svh").write_text("cv32e40p_controller #(.COREV_PULP(1), .COREV_CLUSTER(0), .FPU(0)) dut (\n" + ",\n".join(bindings) + "\n);\n")
        cmd = ["verilator", "--binary", "--timing", "--assert", "-DCV32E40P_ASSERT_ON", "-Wno-fatal", "--top-module", "tb", "--Mdir", str(d / "obj"), "-I" + str(d)]
        cmd += [str(d / pathlib.Path(f).name) for f in FILES] + [str(HERE / "tb.sv")]
        with (d / "build.log").open("w") as log:
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True)
        for count in [0, 1, 2]:
            for stalls in [0, 2]:
                run = subprocess.run([str(d / "obj/Vtb"), f"+COUNT={count}", f"+STALLS={stalls}"], capture_output=True, text=True, timeout=15)
                output = run.stdout + run.stderr
                (d / f"count-{count}-stall-{stalls}.log").write_text(output)
                expected_fail = label == "affected" and count == 0
                passed = run.returncode == 0 and "PASS_ZERO_COUNT_COMPONENT" in output
                detected = run.returncode != 0 and "COUNTER_MISMATCH" in output and "REACHED" in output and "PASS_ZERO_COUNT_COMPONENT" not in output
                ok = detected if expected_fail else passed
                row = dict(variant=label, count=count, stalls=stalls, returncode=run.returncode, expected="counter_mismatch" if expected_fail else "pass", outcome="expected_failure_detected" if detected else "pass" if passed else "unexpected", matched_expectation=ok, observations=[s for s in output.splitlines() if s.startswith(("REACHED", "OBSERVED"))])
                rows.append(row)
                print(label, count, stalls, row["outcome"], flush=True)
    result = dict(scope="controller_plus_hwloop_registers_only", revisions=REVISIONS, source_sha256=hashes, verilator=subprocess.check_output(["verilator", "--version"], text=True).strip(), cases=rows)
    (HERE / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    if not all(r["matched_expectation"] for r in rows):
        raise SystemExit("Unexpected test results; inspect local logs")
    print("PASS: 12/12 outcomes matched the declared expectations")

if __name__ == "__main__":
    main()

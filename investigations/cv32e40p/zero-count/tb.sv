// Original Atlas component test; upstream RTL is fetched separately.
module tb;
  import cv32e40p_pkg::*;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 1;
  logic fetch_enable_i = 0, instr_valid_i = 0;
  logic id_ready_i = 1, id_valid_i = 0;
  logic [31:0] pc_id_i = 0;
  logic [1:0][31:0] hwlp_start_addr_i, hwlp_end_addr_i, hwlp_counter_i;
  logic [1:0] hwlp_dec_cnt_o;
  logic [2:0] setup_we = 0;
  logic setup_bank = 0;
  logic [31:0] setup_start, setup_end, setup_count;
  // Valid models instruction consumption, not mere decode visibility.
  logic consume = 0;
  `include "controller_instance.svh"
  cv32e40p_hwloop_regs regs (
    .clk(clk), .rst_n(rst_n), .hwlp_start_data_i(setup_start),
    .hwlp_end_data_i(setup_end), .hwlp_cnt_data_i(setup_count),
    .hwlp_we_i(setup_we), .hwlp_regid_i(setup_bank), .valid_i(consume),
    .hwlp_dec_cnt_i(hwlp_dec_cnt_o), .hwlp_start_addr_o(hwlp_start_addr_i),
    .hwlp_end_addr_o(hwlp_end_addr_i), .hwlp_counter_o(hwlp_counter_i)
  );
  task automatic tick;
    @(posedge clk); #1; @(negedge clk); #1;
  endtask
  task automatic setup_loop(input bit bank, input int start_pc, end_pc, count);
    setup_bank=bank; setup_start=start_pc; setup_end=end_pc;
    setup_count=count; setup_we=7; tick(); setup_we=0;
  endtask
  int count, stalls, expected;
  initial begin
    if (!$value$plusargs("COUNT=%d",count)) count=0;
    if (!$value$plusargs("STALLS=%d",stalls)) stalls=0;
    #1; rst_n=0;
    tick(); tick(); rst_n=1;
    // Active outer loop makes the inner zero-count end reachable in DECODE_HWLOOP.
    // Inner body has three instructions; distinct ends meet nesting constraints.
    setup_loop(1, 'h100, 'h140, 3);
    setup_loop(0, 'h104, 'h110, count);
    fetch_enable_i=1;
    repeat(4) tick();
    if (dut.ctrl_fsm_cs != DECODE) $fatal(1,"HARNESS_NOT_DECODE");
    instr_valid_i=1; id_valid_i=1; consume=1; pc_id_i='h100; tick();
    if (dut.ctrl_fsm_cs != DECODE_HWLOOP) $fatal(1,"HARNESS_NOT_HWLOOP");
    pc_id_i='h104; tick();
    pc_id_i='h108; tick();
    pc_id_i='h10c;
    // Hold at end without instruction consumption, then accept exactly once.
    id_ready_i=0; id_valid_i=0; consume=0;
    repeat(stalls) begin
      tick();
      if (hwlp_counter_i[0] != count) $fatal(1,"STALL_CHANGED_COUNTER");
    end
    id_ready_i=1; id_valid_i=1; consume=1; #1;
    if (dut.ctrl_fsm_cs != DECODE_HWLOOP || !dut.is_decoding_o || dut.halt_id_o)
      $fatal(1,"HARNESS_END_NOT_REACHED");
    $display("REACHED count=%0d stalls=%0d pc=%08x decrement=%0d",count,stalls,pc_id_i,hwlp_dec_cnt_o[0]);
    expected = count == 0 ? 0 : count-1;
    tick();
    $display("OBSERVED counter=%08x expected=%08x outer=%0d",hwlp_counter_i[0],expected,hwlp_counter_i[1]);
    if (hwlp_counter_i[0] != expected) $fatal(1,"COUNTER_MISMATCH");
    if (hwlp_counter_i[1] != 3) $fatal(1,"OUTER_CHANGED");
    // Leave the tested end; verify there was no duplicate decrement.
    consume=0; instr_valid_i=0; id_valid_i=0; pc_id_i='h114; tick();
    if (hwlp_counter_i[0] != expected) $fatal(1,"DUPLICATE_DECREMENT");
    $display("PASS_ZERO_COUNT_COMPONENT"); $finish;
  end
  initial begin #2000; $fatal(1,"TIMEOUT"); end
endmodule

# Initial public-history leads

These short original summaries are based on public PR descriptions sampled during discovery. They are leads, not independently reproduced findings. Merge status, fixing revisions, complete diffs, and regression coverage still need investigation.

| Source | Description-based lead | Possible review question |
| --- | --- | --- |
| [Ibex #2501](https://github.com/lowRISC/ibex/pull/2501) | Co-simulation parameter names did not match expected defines. | Does the reference model actually use the DUT configuration? |
| [core-v-verif #2748](https://github.com/openhwfoundation/core-v-verif/pull/2748) | Write-response tracking needed per-ID state for out-of-order responses. | Is response ownership preserved independently for each transaction ID? |
| [core-v-verif #2747](https://github.com/openhwfoundation/core-v-verif/pull/2747) | Exclusive-failure and reservation handling in the memory model needed correction. | Can a failed exclusive operation still mutate the oracle's memory? |
| [CVA6 #3586](https://github.com/openhwfoundation/cva6/pull/3586) | Non-power-of-two associativity could produce an invalid replacement index. | Are all representable indices valid for the selected configuration? |
| [VexRiscv #481](https://github.com/SpinalHDL/VexRiscv/pull/481) | MMIO access size needed preservation on a wider bus. | Is the original access width preserved for uncached/peripheral requests? |
| [NEORV32 #1654](https://github.com/stnolting/neorv32/pull/1654) | Counter writes and automatic increments required explicit priority. | Does an explicit CSR write override the side-effect update correctly? |
| [VeeR EL2 #551](https://github.com/chipsalliance/Cores-VeeR-EL2/pull/551) | ICCM word/address association affected decoding and ECC behavior. | Does each data word retain the address metadata needed to interpret it? |

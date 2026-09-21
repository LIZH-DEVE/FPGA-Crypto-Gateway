# RX50T 当前 Baseline

本文记录 `main` 分支当前用于公开展示的 RX50T pure-PL 主线。

## 1. 系统定位

RX50T 版本采用 pure-PL 架构，不依赖 ARM/PS、DMA 或 DDR。主线目标是在资源受限 FPGA 上保留可完整验证的硬件数据通路，并提供必要的 runtime observability。

当前主线：

```text
UART RX
  → Parser
  → Protocol Dispatcher
  → contest_crypto_axis_core
      ├── contest_acl_axis_core
      ├── contest_axis_block_packer
      ├── contest_crypto_block_engine
      └── contest_axis_block_unpacker
  → UART TX
```

旧版 `contest_acl_core` 与 `contest_crypto_bridge` 仍保留用于 legacy probe 和 unit test，但不属于当前 Crypto Probe 默认主线。

## 2. Board Baseline

- Board：RX50T
- FPGA：Xilinx Artix-7 XC7A50T
- Clock：50 MHz
- UART：2,000,000 baud
- UART RX：K1
- UART TX：J1
- Reset：J20

当前 board top 的默认参数可在 `contest_project/rtl/contest/rx50t_uart_crypto_probe_board_top.sv` 中核对。

## 3. 当前功能

### UART / Parser

- framed UART ingress / egress；
- SOF + LEN + PAYLOAD 自定义帧；
- frame timeout 与 protocol error handling。

### ACL

- AXI-Stream 数据接口；
- 8-slot runtime rule table；
- rule hit counter；
- block pulse / slot observability；
- runtime rule update。

### Crypto datapath

- byte stream → 128-bit block packing；
- AES-128 / SM4-128；
- 128-bit block → byte stream unpacking；
- 支持 16B / 32B / 64B / 128B 数据路径；
- AXI-Stream backpressure。

### Observability

- frame / ACL / AES / SM4 / error counters；
- PMU snapshot 与 clear；
- host-side query tooling；
- on-chip benchmark path。

### Host side

- CLI probe；
- protocol layer；
- worker；
- Tkinter GUI。

## 4. 代表性验证

AXIS v1.1 baseline 已记录：

- Implementation WNS：6.392 ns；
- Implementation WHS：0.035 ns；
- Slice LUTs：3794（11.64%）；
- Slice Registers：5449（8.36%）；
- Block RAM Tile：4.5（6.00%）；
- DSP：0。

板级 smoke test 包括：

- stats query；
- PMU clear / query；
- AES known vector；
- SM4 known vector；
- ACL block / recovery；
- multi-block file traffic。

已记录的 UART end-to-end 文件流量：

- 32 KB AES / SM4：约 0.780 Mbps；
- 512 KB AES / SM4：约 0.787 Mbps。

## 5. Feature Branches

仓库中还保留：

- clock gating；
- trace buffer；
- portability handoff；

等进一步实验分支。它们与 `main` baseline 分开记录，避免把 branch-level feature 与稳定主线混为同一版本。

## 6. 当前边界

该仓库不以以下内容为当前目标：

- ARM/PS；
- DMA / DDR / PBM；
- full Ethernet/IP/UDP stack；
- persistent ACL storage；
- PUF / hardware key derivation。

更详细的代码级说明见 [CODE_ANALYSIS_REPORT.md](CODE_ANALYSIS_REPORT.md)。

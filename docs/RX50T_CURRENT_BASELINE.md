# RX50T Current Baseline

本文记录 `main` 分支当前 RX50T pure-PL 主线的硬件配置、功能范围和验证结果。

## 系统结构

```text
UART RX
  → Parser / Control Dispatcher
  → contest_crypto_axis_core
      ├── contest_acl_axis_core
      ├── contest_axis_block_packer
      ├── contest_crypto_block_engine
      └── contest_axis_block_unpacker
  → UART TX
```

主数据通路之外还包含：

- ingress / egress CDC；
- watchdog；
- PMU；
- trace buffer；
- on-chip benchmark；
- ACL runtime update 与 hit counters。

## Board Baseline

| 项目 | 配置 |
| --- | --- |
| Board | RX50T |
| FPGA | Xilinx Artix-7 XC7A50T |
| Part | `xc7a50tfgg484-1` |
| Root Clock | 50 MHz |
| UART | 2,000,000 baud |
| UART RX | K1 |
| UART TX | J1 |
| Reset | J20 |

当前 board top：

```text
contest_project/rtl/contest/rx50t_uart_crypto_probe_board_top.sv
```

## 功能

### UART / Parser

- framed UART ingress / egress；
- SOF + LEN + PAYLOAD frame；
- protocol error handling；
- control command / data request 分流。

### ACL

- AXI-Stream interface；
- 8-slot runtime rule table；
- runtime rule update；
- per-rule hit counter；
- pass / block path。

### Crypto Datapath

- byte stream → 128-bit block；
- AES-128 / SM4-128；
- 128-bit block → byte stream；
- 16B / 32B / 64B / 128B request path；
- AXI-Stream backpressure。

当前 baseline 使用固定的标准测试向量 key 进行功能验证。

### CDC / Buffering

- async AXIS FIFO；
- ingress clock domain bridge；
- UART egress bridge；
- skid buffer；
- reset synchronization。

### Observability

- frame / ACL / AES / SM4 / error counters；
- PMU snapshot / clear；
- trace buffer；
- on-chip benchmark；
- host-side CLI / GUI readback。

## 验证记录

代表性 implementation 结果：

| 指标 | 结果 |
| --- | ---: |
| WNS | 6.392 ns |
| WHS | 0.035 ns |
| Slice LUTs | 3794（11.64%） |
| Slice Registers | 5449（8.36%） |
| Block RAM Tile | 4.5（6.00%） |
| DSP | 0 |

板级验证包括：

- stats / PMU query；
- AES known vector；
- SM4 known vector；
- ACL block / recovery；
- watchdog；
- multi-block traffic；
- trace readback。

记录的 UART end-to-end 文件流量约为：

- 32 KB AES / SM4：0.780 Mbps；
- 512 KB AES / SM4：0.787 Mbps。

该结果主要受 2 Mbps UART transport 限制。

## Legacy Probes

仓库同时保留 UART echo、parser、ACL 与 SM4 单功能 probe，用于 bring-up 和模块级故障定位。

这些 probe 的 board top 默认使用 115200 baud，不属于当前 2 Mbps crypto gateway 主线。

## 相关文档

- [Build and Test](BUILD_AND_TEST.md)
- [Implementation Guide](IMPLEMENTATION_GUIDE.md)
- [Architecture Overview](RX50T_ARCHITECTURE_OVERVIEW.md)
- [Current Board Test](RX50T_UART_CRYPTO_PROBE_BOARD_TEST.md)

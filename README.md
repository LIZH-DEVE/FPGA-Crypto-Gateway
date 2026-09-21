# FPGA 加密网关：RX50T 板级完整实现

基于 **Xilinx Artix-7 XC7A50T / RX50T 开发板** 的 pure-PL 加密网关工程。

项目从 UART 输入开始，在 FPGA 内完成协议解析、ACL 过滤、AES / SM4 数据处理、运行状态统计与异常恢复，并通过 UART 返回结果。仓库包含 RTL、SystemVerilog testbench、Vivado 构建脚本和上位机调试工具。

## 数据通路

```text
UART RX
  → Parser
  → Protocol Dispatcher
  → AXI-Stream ACL
  → 8→128 Block Packer
  → AES / SM4 Block Engine
  → 128→8 Block Unpacker
  → UART TX
```

## 主要功能

- **UART**：2,000,000 baud 板级通信；
- **Protocol Parser**：帧解析、长度检查与错误处理；
- **ACL**：8-slot runtime rule table、hit counter 与 block path；
- **AXI-Stream**：valid / ready backpressure 与 block stream pipeline；
- **AES / SM4**：128-bit block encryption，覆盖 16B / 32B / 64B / 128B 数据路径；
- **Watchdog**：stream / crypto timeout recovery；
- **PMU**：运行周期、stall、ACL block 与数据流统计；
- **Trace Buffer**：板上事件记录与 UART readback；
- **Host Tools**：Python CLI、协议工具与 Tkinter GUI。

## 代码结构

```text
contest_project/
├── rtl/contest/       # FPGA RTL
├── tb/contest/        # SystemVerilog testbench
├── constraints/       # RX50T constraints
├── scripts/           # Vivado build / simulation
└── tools/             # CLI / GUI / protocol tools

docs/                  # 架构、baseline 与板级测试记录
daily-progress/        # 开发过程记录
reference/             # 参考 RTL
```

## RTL

核心代码位于 `contest_project/rtl/contest/`，包括：

- `contest_uart_rx.sv` / `contest_uart_tx.sv`
- `contest_parser_core.sv`
- `contest_acl_axis_core.sv`
- `contest_axis_block_packer.sv`
- `contest_crypto_block_engine.sv`
- `contest_axis_block_unpacker.sv`
- `contest_trace_buffer.sv`
- CDC / FIFO / skid buffer
- RX50T board-level top

当前板级顶层：

`rx50t_uart_crypto_probe_board_top.sv`

## 验证

主线完成 simulation、implementation 与 real-board 验证。

代表性 implementation 结果：

| 指标 | 结果 |
| --- | ---: |
| WNS | **6.392 ns** |
| WHS | **0.035 ns** |
| Slice LUTs | **3794（11.64%）** |
| Slice Registers | **5449（8.36%）** |
| Block RAM Tile | **4.5（6.00%）** |
| DSP | **0** |

板级验证覆盖：

- AES / SM4 known vector；
- ACL block / recovery；
- stats / PMU query；
- watchdog；
- multi-block file traffic；
- trace readback。

## 上位机工具

`contest_project/tools/` 包含：

- UART probe CLI；
- protocol handling；
- board worker；
- Tkinter GUI；
- stats / PMU / trace readback。

## 文档

- [当前 baseline](docs/RX50T_CURRENT_BASELINE.md)
- [架构说明](docs/RX50T_ARCHITECTURE_OVERVIEW.md)
- [源码分析](docs/CODE_ANALYSIS_REPORT.md)
- [开发记录](daily-progress/README.md)

## 第三方代码

AES / SM4 算法核心采用公开参考实现，并保留原始版权与许可信息。

详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

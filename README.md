# FPGA Crypto Gateway

这是 FPGA 加密网关的公开源码仓库，保存 **RTL、testbench、Vivado 构建脚本、板级调试工具和相关技术文档**。

当前代码以 RX50T / Artix-7 上的 pure-PL 实现为主，重点是协议处理、ACL、AES / SM4 数据通路、AXI-Stream 流控、运行状态观测与板级验证。

## 数据通路

```text
UART RX
  → Parser
  → Protocol Dispatcher
  → AXI-Stream ACL
  → Block Packer
  → AES / SM4 Block Engine
  → Block Unpacker
  → UART TX
```

## 目录结构

```text
contest_project/
├── rtl/contest/       # 主要 RTL
├── tb/contest/        # SystemVerilog testbench
├── tools/             # Python CLI / GUI / protocol tools
├── scripts/           # Vivado build / simulation scripts
└── constraints/       # RX50T pin / timing constraints

docs/                  # 架构、baseline 与板级测试记录
daily-progress/        # 开发过程记录
reference/             # 参考 RTL
```

## 主要 RTL

核心代码位于 `contest_project/rtl/contest/`，包括：

- UART RX / TX；
- protocol parser；
- ACL rule path；
- AXI-Stream packer / unpacker；
- AES / SM4 block engine integration；
- FIFO / skid buffer；
- CDC ingress / egress；
- watchdog；
- PMU / trace buffer；
- board-level top。

当前 board top：

`contest_project/rtl/contest/rx50t_uart_crypto_probe_board_top.sv`

默认板级配置：

- FPGA：Xilinx Artix-7 XC7A50T；
- clock：50 MHz；
- UART：2,000,000 baud。

## Testbench

`contest_project/tb/contest/` 保存 RTL 验证代码，覆盖：

- UART；
- parser；
- ACL；
- AXI-Stream crypto path；
- CDC；
- watchdog；
- clock gating；
- PMU / benchmark；
- trace buffer。

## Host Tools

`contest_project/tools/` 保存上位机调试工具，包括：

- UART probe CLI；
- protocol handling；
- board worker；
- Tkinter GUI；
- stats / PMU / trace readback。

这些工具用于驱动开发板并核对 FPGA 返回结果。

## 构建与仿真

`contest_project/scripts/` 保存 Vivado build 与 simulation scripts，可用于：

- module-level simulation；
- RX50T top-level build；
- bitstream generation；
- board-oriented regression。

## 技术文档

- [当前 baseline](docs/RX50T_CURRENT_BASELINE.md)
- [架构说明](docs/RX50T_ARCHITECTURE_OVERVIEW.md)
- [源码分析](docs/CODE_ANALYSIS_REPORT.md)
- [开发记录](daily-progress/README.md)

## 第三方代码

AES / SM4 算法核心包含公开参考实现，并保留原始源码中的版权和许可信息。

详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 项目展示

PC–ESP32–FPGA–STM32 安全控制系统的整体架构、比赛背景、个人工作与验证结果见：

**LIZH-DEVE/fpga-secure-control-system**

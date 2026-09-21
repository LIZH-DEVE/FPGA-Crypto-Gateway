# FPGA Crypto Gateway

本仓库用于集中保存 **FPGA 加密网关相关源码、testbench、构建脚本和调试工具**。

项目代码以 RX50T / Artix-7 上的 pure-PL 加密数据通路为主，同时保留一组 Zynq / AXI 数据搬运模块。这里的重点是源码组织与工程实现，不承担比赛项目展示页的角色。

## 代码入口

### RX50T 主线

`contest_project/` 是当前主要 FPGA 实现：

```text
UART RX
  → Parser
  → Protocol Dispatcher
  → AXI-Stream ACL
  → Block Packer
  → AES / SM4 Engine
  → Block Unpacker
  → UART TX
```

主要目录：

```text
contest_project/
├── rtl/contest/       # RTL
├── tb/contest/        # SystemVerilog testbench
├── tools/             # Python CLI / GUI / protocol tools
├── scripts/           # Vivado build / simulation scripts
└── constraints/       # RX50T constraints
```

### Zynq / AXI 数据通路

`zynq-datapath/` 保存与 SoC 数据搬运相关的独立模块：

```text
zynq-datapath/
├── rtl/
│   ├── control/       # AXI-Lite CSR
│   ├── cdc/           # async FIFO
│   ├── buffer/        # PBM / FIFO
│   ├── datapath/      # Gearbox
│   ├── dma/           # DMA engine / descriptor fetcher
│   └── interfaces/    # AXI-Lite / AXI-Stream definitions
├── tb/
└── docs/
```

这部分保留 AXI、CDC、DMA、buffer management 与 descriptor-driven execution 等代码，不重复保存 RX50T 主线已经覆盖的 AES / SM4、parser 和 TX 实现。

## RX50T RTL

当前主线核心模块位于：

`contest_project/rtl/contest/`

其中包括：

- UART RX / TX；
- protocol parser；
- ACL；
- AXI-Stream packer / unpacker；
- AES / SM4 block engine integration；
- FIFO / skid buffer；
- CDC bridge；
- watchdog；
- PMU / trace buffer；
- board-level top。

当前 board top：

`rx50t_uart_crypto_probe_board_top.sv`

默认配置：

- FPGA：Xilinx Artix-7 XC7A50T；
- clock：50 MHz；
- UART：2,000,000 baud。

## Testbench 与验证

`contest_project/tb/contest/` 保存主线 testbench，覆盖：

- UART；
- parser；
- ACL；
- AXI-Stream crypto path；
- watchdog；
- clock gating；
- PMU / benchmark；
- trace buffer；
- CDC ingress / egress。

Zynq 数据通路还保留：

`zynq-datapath/tb/tb_dma_boundary.sv`

用于检查 AXI4 DMA 跨 4 KB boundary 时的 Burst split。

## Host Tools

`contest_project/tools/` 包含：

- UART probe CLI；
- protocol handling；
- board worker；
- Tkinter GUI；
- stats / PMU / trace readback 工具。

这些工具用于驱动真实开发板并核对 FPGA 返回结果。

## 构建脚本

`contest_project/scripts/` 保存 Vivado build 与 simulation scripts。

常用入口包括 RX50T Crypto Probe 的 RTL simulation、bitstream build 与各模块 testbench。

## 文档

代码相关说明位于：

- [当前 baseline](docs/RX50T_CURRENT_BASELINE.md)
- [架构说明](docs/RX50T_ARCHITECTURE_OVERVIEW.md)
- [源码分析](docs/CODE_ANALYSIS_REPORT.md)
- [Zynq Datapath](zynq-datapath/README.md)
- [迁移审计](zynq-datapath/docs/migration-audit.md)

## 第三方代码

AES / SM4 算法核心包含公开参考实现，并保留原始源码中的版权与许可信息。

第三方模块说明见：

[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

## 对应项目展示

完整的 PC–ESP32–FPGA–STM32 安全控制系统、系统架构、个人工作和验证结果见：

**LIZH-DEVE/fpga-secure-control-system**

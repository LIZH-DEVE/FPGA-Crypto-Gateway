# FPGA 开发：RX50T 实机系统与 Zynq 数据通路

本仓库集中整理两类互补的 **FPGA / RTL 开发实践**：

1. **RX50T pure-PL 实机系统**：面向真实 Artix-7 开发板，完成 UART、protocol parser、ACL、AES / SM4、PMU / trace、watchdog、host tools 与板级验证；
2. **Zynq heterogeneous datapath**：面向 SoC data movement，保留 AXI-Lite、AXI4、CDC、FIFO、Gearbox、PBM、DMA 与 descriptor ring 等模块。

两部分分别覆盖“**真实 FPGA 板级实现**”与“**PS/PL 数据搬运与异构互联**”，避免将同类 crypto / parser 代码重复维护。

## 1. RX50T pure-PL 主线

当前主要开发线基于 **RX50T / Xilinx Artix-7 XC7A50T**。

数据通路：

```text
UART RX
  → Parser
  → Protocol Dispatcher
  → contest_crypto_axis_core
      ├── AXIS ACL
      ├── 8→128 Packer
      ├── AES / SM4 Block Engine
      └── 128→8 Unpacker
  → UART TX
```

### 技术内容

- **UART datapath**：2M baud 板级通信与 buffering；
- **Protocol parser**：帧解析、长度检查与 error handling；
- **ACL**：8-slot runtime rule table、hit counter 与 block path；
- **AXI-Stream pipeline**：backpressure-aware ACL / packer / block engine / unpacker；
- **AES / SM4 integration**：128-bit block path，覆盖 16B / 32B / 64B / 128B；
- **Observability**：statistics、PMU、on-chip benchmark；
- **Fault handling**：watchdog 与 fatal response；
- **Host tools**：Python CLI、protocol layer、worker 与 Tkinter GUI。

feature branches 还保留 clock gating、trace buffer 与 portability handoff 等实验。

### 实机与实现结果

| 指标 | 结果 |
| --- | ---: |
| Implementation WNS | **6.392 ns** |
| Implementation WHS | **0.035 ns** |
| Slice LUTs | **3794（11.64%）** |
| Slice Registers | **5449（8.36%）** |
| Block RAM Tile | **4.5（6.00%）** |
| DSP | **0** |

板级验证包括：

- stats / PMU query；
- AES / SM4 known vector；
- ACL block / recovery；
- multi-block file traffic。

已有 UART end-to-end 文件流量记录：

| Workload | 时间 | 有效吞吐 |
| --- | ---: | ---: |
| 32 KB SM4 | 0.336 s | 0.780 Mbps |
| 32 KB AES | 0.336 s | 0.780 Mbps |
| 512 KB SM4 | 5.331 s | 0.787 Mbps |
| 512 KB AES | 5.331 s | 0.787 Mbps |

这些数字描述的是当前 UART-bound end-to-end datapath，而不是 cipher core 的峰值吞吐。

## 2. Zynq / AXI Datapath

原 `fpga-heterogeneous-datapath` 中与 RX50T 主线互补的部分已经整理到：

[`zynq-datapath/`](zynq-datapath/README.md)

主要保留：

- **AXI-Lite CSR**：software / PS control interface；
- **AXI4 DMA**：Burst write、4 KB boundary split 与 backpressure；
- **Descriptor fetcher**：descriptor ring 基础执行路径；
- **CDC**：async FIFO 与 Gray-code pointer synchronization；
- **Buffer management**：PBM reserve / commit / rollback；
- **Width conversion**：128-bit → 32-bit Gearbox；
- **Interface definitions**：AXI-Lite / AXI-Stream interface 与 package；
- **Verification**：DMA 4 KB boundary testbench。

该目录不再重复迁移 AES / SM4 算法核心、UART parser 和 TX stack。

## 3. 仓库结构

```text
.
├── contest_project/          # RX50T 主线 RTL / TB / tools / build scripts
├── zynq-datapath/            # AXI / CDC / DMA / PBM / descriptor ring
├── docs/                     # RX50T architecture / baseline / board tests
├── daily-progress/           # RX50T 开发记录
├── reference/                # 参考 RTL
├── THIRD_PARTY_NOTICES.md
└── README.md
```

### RX50T

```text
contest_project/
├── rtl/contest/
├── tb/contest/
├── tools/
├── scripts/
└── constraints/
```

### Zynq datapath

```text
zynq-datapath/
├── rtl/
│   ├── control/
│   ├── cdc/
│   ├── buffer/
│   ├── datapath/
│   ├── dma/
│   └── interfaces/
├── tb/
└── docs/
```

## 4. 文档入口

### RX50T

- [当前 baseline](docs/RX50T_CURRENT_BASELINE.md)
- [架构说明](docs/RX50T_ARCHITECTURE_OVERVIEW.md)
- [代码实现分析](docs/CODE_ANALYSIS_REPORT.md)
- [开发记录](daily-progress/README.md)

### Zynq / data movement

- [Zynq Datapath 概览](zynq-datapath/README.md)
- [开发内容摘要](zynq-datapath/docs/development-overview.md)

## 5. 第三方代码

AES / SM4 部分使用公开参考实现，原始版权与许可信息保留在源码中。主要工程工作集中在 RTL integration、stream / memory datapath、protocol processing、runtime observability、fault handling、host tooling 与板级验证。

详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

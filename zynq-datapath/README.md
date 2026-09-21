# Zynq / AXI Datapath 实验

该目录由原 `fpga-heterogeneous-datapath` 仓库中整理迁入，保留与 RX50T pure-PL 主线互补的 **AXI / CDC / DMA / buffer / Zynq data movement** 内容。

这里不再重复 AES / SM4 算法核心、UART parser 或完整安全网关逻辑；这些内容在 RX50T 主线中已有更完整的实现和板级验证。

## 保留内容

- **AXI-Lite CSR**：PS / software control register interface；
- **AXI4 DMA**：Burst write、4 KB boundary split、backpressure；
- **Descriptor fetcher**：descriptor ring 的基础 read path；
- **CDC**：async FIFO 与 Gray-code pointer synchronization；
- **Buffer management**：PBM reserve / commit / rollback；
- **Datapath width conversion**：128-bit → 32-bit Gearbox；
- **Interface definitions**：AXI-Lite / AXI-Stream interface 与 package；
- **Verification sample**：DMA 4 KB boundary testbench。

## 目录结构

```text
zynq-datapath/
├── README.md
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

## 与 RX50T 主线的区别

RX50T 主线强调：

```text
real board
+ pure-PL stream datapath
+ ACL / AES / SM4
+ PMU / trace / watchdog
+ GUI / CLI
```

本目录强调：

```text
AXI / CDC
+ DMA / DDR data movement
+ buffer ownership
+ descriptor-driven execution
+ Zynq PS/PL interface
```

两部分合并后，仓库同时覆盖了 **板级 RTL implementation** 与 **SoC data movement / heterogeneous integration** 两类 FPGA 开发经验。

## 说明

该目录是从原独立仓库中抽取的可复用部分。原仓库中的 crypto / parser / TX 等重复模块没有再次迁入，避免与 RX50T 主线形成重复展示。

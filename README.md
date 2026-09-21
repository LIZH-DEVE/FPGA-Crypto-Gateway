# RX50T Crypto Gateway

基于 **RX50T / Artix-7** 的 pure-PL 安全数据通路项目，主要用于 FPGA RTL、流式数据处理、runtime observability 与板级验证实践。

当前主线不使用 ARM/PS、DMA 或 DDR，而是在资源受限的 FPGA 上保留完整的硬件闭环：

```text
UART RX
  → Parser
  → Protocol Dispatcher
  → AXIS ACL
  → 8→128 Packer
  → AES / SM4 Block Engine
  → 128→8 Unpacker
  → UART TX
```

## 技术内容

- **UART datapath**：2M baud 板级通信、RX/TX buffering；
- **Protocol parser**：自定义帧解析、长度检查与错误处理；
- **ACL**：8-slot runtime rule table、hit counter 与 block path；
- **AXI-Stream pipeline**：backpressure-aware ACL、packer、crypto block engine 与 unpacker；
- **AES / SM4**：128-bit block encryption，支持 16B / 32B / 64B / 128B 数据路径；
- **Observability**：统计计数、PMU snapshot、on-chip benchmark；
- **Fault handling**：watchdog 与 fatal response；
- **Host tools**：Python CLI、protocol layer、worker 与 Tkinter GUI。

仓库中的 feature branches 还保留了 clock gating、trace buffer 和 portability handoff 等进一步实验。

## 硬件基线

| 项目 | 配置 |
| --- | --- |
| Board | RX50T |
| FPGA | Xilinx Artix-7 XC7A50T |
| Clock | 50 MHz |
| UART | 当前主线支持 2,000,000 baud |
| UART RX / TX | K1 / J1 |
| Reset | J20 |

不同开发阶段曾使用不同 UART 配置；具体 board baseline 与测试条件以对应开发记录为准。

## 当前主线

当前主线以 `contest_crypto_axis_core` 为核心：

```text
Parser
  → Protocol Dispatcher
  → contest_crypto_axis_core
      ├── contest_acl_axis_core
      ├── contest_axis_block_packer
      ├── contest_crypto_block_engine
      └── contest_axis_block_unpacker
  → UART TX
```

旧版 `contest_acl_core` 与 `contest_crypto_bridge` 仍保留，用于独立 Probe 与对应 unit test，不属于当前 Crypto Probe 的默认主线。

## 代表性验证结果

AXIS v1.1 主线完成过完整的 simulation、implementation 与 real-board 验证。

### Implementation

- Implementation WNS：**6.392 ns**
- Implementation WHS：**0.035 ns**
- Slice LUTs：**3794（11.64%）**
- Slice Registers：**5449（8.36%）**
- Block RAM Tile：**4.5（6.00%）**
- DSP：**0**

### 板级验证

已记录的主线 smoke test 包括：

- stats query；
- PMU clear / query；
- AES known vector；
- SM4 known vector；
- ACL block / recovery；
- multi-block file traffic。

已有板级文件传输记录：

| Workload | 时间 | 有效吞吐 |
| --- | ---: | ---: |
| 32 KB SM4 | 0.336 s | 0.780 Mbps |
| 32 KB AES | 0.336 s | 0.780 Mbps |
| 512 KB SM4 | 5.331 s | 0.787 Mbps |
| 512 KB AES | 5.331 s | 0.787 Mbps |

这些结果用于描述当前 UART-bound end-to-end datapath，而不是算法核的峰值吞吐。

## 代码结构

```text
contest_project/
├── rtl/contest/       # 主线 RTL
├── tb/contest/        # SystemVerilog testbench
├── tools/             # CLI / protocol / worker / GUI
├── scripts/           # Vivado build / simulation scripts
└── constraints/       # RX50T constraints

docs/                  # 架构、baseline、board test 与 runbook
daily-progress/        # 开发过程记录
reference/             # 参考模块与基础 RTL
```

## 常用入口

- [代码实现分析](docs/CODE_ANALYSIS_REPORT.md)
- [当前 baseline](docs/RX50T_CURRENT_BASELINE.md)
- [架构说明](docs/RX50T_ARCHITECTURE_OVERVIEW.md)
- [开发记录](daily-progress/README.md)

## 设计边界

当前主线聚焦 pure-PL datapath，以下内容不作为该仓库的目标：

- ARM/PS；
- DMA / DDR / PBM；
- full Ethernet/IP/UDP stack；
- persistent ACL storage；
- PUF / hardware key derivation。

## 第三方代码

AES / SM4 部分使用公开参考实现，原始版权与许可信息保留在源码中。项目工作主要集中在协议解析、ACL、AXIS datapath、接口适配、observability、fault handling、host tooling 与板级验证。

详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

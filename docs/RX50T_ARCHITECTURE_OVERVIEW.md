# RX50T 架构说明

## 1. 主线结构

当前 RX50T 主线是一个 pure-PL stream datapath：

```text
UART RX
  │
  v
Parser
  │
  v
Protocol Dispatcher
  │
  v
contest_crypto_axis_core
  ├── ACL AXIS
  ├── 8→128 Packer
  ├── AES / SM4 Block Engine
  └── 128→8 Unpacker
  │
  v
UART TX
```

控制与 observability 逻辑并行提供 stats、ACL 配置、PMU 与 benchmark query。

## 2. UART

### RX

负责将异步 UART serial input 转换为内部 byte stream，并进行 start / data / stop bit 处理。

### TX

负责将处理后的 byte stream 发送回 host，并通过 ready / valid 机制接受上游数据。

当前 Crypto Probe board top 默认使用 50 MHz clock 与 2,000,000 baud。

## 3. Parser

`contest_parser_core` 解析：

```text
SOF(0x55) + LEN + PAYLOAD
```

并输出 payload stream、frame boundary 与 error information。

## 4. Protocol Dispatcher

Protocol Dispatcher 负责区分：

- data path request；
- stats / PMU / ACL query；
- ACL update；
- benchmark / control command。

这样数据处理与控制命令可以共享 UART transport，但在内部进入不同处理路径。

## 5. AXIS ACL

`contest_acl_axis_core` 位于主数据通路前段：

- 使用 AXI-Stream style valid / ready；
- 维护 8 个 runtime rule slot；
- 对数据流执行 pass / block；
- 记录 hit counter；
- 向上层输出 ACL block event。

## 6. Packer / Crypto / Unpacker

### Packer

将 8-bit byte stream 聚合为 128-bit block，并保留 last / valid-byte metadata。

### Crypto Block Engine

支持 AES-128 与 SM4-128。内部使用 buffer 将 UART 速率与 block cipher execution 解耦。

### Unpacker

将 128-bit result 按有效字节数重新展开为 8-bit stream。

## 7. Observability

主线提供多层 observability：

- frame / error counters；
- ACL hit counters；
- PMU counters；
- on-chip benchmark；
- host-side query / GUI。

feature branches 进一步扩展了 clock gating 与 trace buffer。

## 8. 为什么采用 pure-PL

该架构刻意不引入 ARM/PS、DMA/DDR 和完整网络协议栈，目的是：

- 缩短 board-level datapath；
- 将 FPGA resource 与 timing 约束集中在关键 RTL；
- 简化 real-board reproduction；
- 保留足够的 observability 用于定位 bottleneck。

因此 RX50T 仓库更适合作为 FPGA datapath / runtime observability 项目，而不是完整 heterogeneous SoC。

# RX50T Architecture Overview

## 主线数据通路

```text
UART RX
  │
  v
Parser / Protocol Dispatcher
  │
  v
contest_crypto_axis_core
  ├── AXI-Stream ACL
  ├── 8-to-128 Packer
  ├── AES / SM4 Block Engine
  └── 128-to-8 Unpacker
  │
  v
UART TX
```

控制与观测逻辑并行提供 ACL 配置、stats、PMU、trace 和 on-chip benchmark。

## UART

`contest_uart_rx.sv` 与 `contest_uart_tx.sv` 负责串行输入输出。

当前主线 board top：

```text
50 MHz root clock
2,000,000 baud
```

UART RX / TX 与主数据通路之间通过 FIFO / skid buffer 处理 backpressure。

## Parser / Control Dispatcher

`contest_parser_core.sv` 解析 frame boundary、length 与 payload。

控制命令和数据请求共享 UART transport，但在内部进入不同路径：

- crypto data；
- stats / PMU query；
- ACL query / update；
- trace query；
- benchmark control。

## AXI-Stream ACL

`contest_acl_axis_core.sv` 位于 crypto path 前段。

主要功能：

- AXI-Stream valid / ready；
- 8 个 runtime rule slots；
- pass / block；
- per-rule hit counters；
- runtime rule update。

## Block Crypto Path

### Packer

`contest_axis_block_packer.sv` 将 8-bit byte stream 聚合为 128-bit block，并维护 block boundary / valid-byte metadata。

### Crypto Engine

`contest_crypto_block_engine.sv` 支持 AES-128 与 SM4-128。

当前 board baseline 使用固定标准测试向量 key，用于验证算法接口与数据通路；runtime key provisioning 未包含在该版本中。

### Unpacker

`contest_axis_block_unpacker.sv` 将 128-bit result 重新展开为 byte stream。

## CDC / Buffering

当前主线包含：

- `contest_async_axis_fifo.sv`
- `contest_async_mailbox.sv`
- `contest_async_pulse.sv`
- `contest_byte_skid_buffer.sv`
- `contest_crypto_cdc_ingress_bridge.sv`
- `contest_uart_cdc_egress_bridge.sv`
- `contest_uart_cdc_ingress_frontend.sv`

用于连接 ingress、crypto/control 与 UART egress 的不同执行阶段。

## Observability

`contest_uart_crypto_probe.sv` 集成：

- frame / crypto / ACL counters；
- PMU；
- watchdog；
- trace buffer；
- on-chip benchmark；
- control response path。

host 端通过 CLI / worker / GUI 查询这些状态。

## Pure-PL 设计

当前 RX50T 工程不依赖 ARM/PS、DMA 或 DDR。

这样可以把板级验证集中在：

- RTL data path；
- handshake / backpressure；
- CDC；
- resource / timing；
- protocol-level observability。

更完整的模块索引见 [Implementation Guide](IMPLEMENTATION_GUIDE.md)。

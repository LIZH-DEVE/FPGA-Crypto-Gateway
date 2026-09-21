# Implementation Guide

## 1. 主数据通路

当前 RX50T 主线：

```text
UART RX
  → Parser
  → Protocol / Control Dispatcher
  → AXI-Stream ACL
  → 8-to-128 Block Packer
  → AES / SM4 Block Engine
  → 128-to-8 Block Unpacker
  → UART TX
```

板级顶层：

```text
rx50t_uart_crypto_probe_board_top.sv
```

主要实现集中在：

```text
contest_project/rtl/contest/
```

## 2. UART 与协议入口

- `contest_uart_rx.sv`
- `contest_uart_tx.sv`
- `contest_parser_core.sv`

UART 将串行输入转换为 byte stream，parser 解析 frame boundary、length 与 payload。控制命令与数据请求随后进入不同处理路径。

## 3. ACL

主线 ACL：

```text
contest_acl_axis_core.sv
```

功能包括：

- AXI-Stream valid / ready；
- runtime rule slots；
- hit counters；
- pass / block；
- rule update；
- block-event observability。

早期 `contest_acl_core.sv` 仍保留给 legacy probe 和单元测试使用。

## 4. Crypto Datapath

### Packer

```text
contest_axis_block_packer.sv
```

把 byte stream 聚合为 128-bit block，并携带 block boundary / valid-byte metadata。

### Block Engine

```text
contest_crypto_block_engine.sv
```

负责 AES-128 / SM4-128 block operation，并通过 FIFO 与 stream datapath 解耦。

当前 board baseline 使用固定的标准测试向量 key 进行验证；runtime key provisioning 不在当前实现范围内。

### Unpacker

```text
contest_axis_block_unpacker.sv
```

把 128-bit result 恢复为 byte stream。

## 5. CDC 与 Buffering

相关模块包括：

- `contest_async_axis_fifo.sv`
- `contest_async_mailbox.sv`
- `contest_async_pulse.sv`
- `contest_byte_skid_buffer.sv`
- `contest_crypto_cdc_ingress_bridge.sv`
- `contest_uart_cdc_egress_bridge.sv`
- `contest_uart_cdc_ingress_frontend.sv`

这些模块用于分离 UART / ingress 与 crypto/control 时钟域，并处理 backpressure。

## 6. Runtime Observability

主线提供：

- frame / error counters；
- ACL hit counters；
- PMU；
- on-chip benchmark；
- trace buffer；
- host-side query。

主要模块：

```text
contest_trace_buffer.sv
contest_uart_crypto_probe.sv
```

对应 host tooling 位于：

```text
contest_project/tools/
```

## 7. Host Tooling

- `crypto_gateway_protocol.py`：frame / command protocol
- `crypto_gateway_worker.py`：serial worker
- `send_rx50t_crypto_probe.py`：CLI
- `rx50t_crypto_gui.py`：Tkinter GUI

板级查询、known-vector、PMU、trace 与 file path 都通过同一套 protocol / worker 逻辑访问。

## 8. Reference RTL

`reference/` 中包含 AES / SM4 等公开参考 RTL 与对应 testbench。

第三方代码版权与许可说明见根目录 `THIRD_PARTY_NOTICES.md`。

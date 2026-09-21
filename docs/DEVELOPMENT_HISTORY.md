# Development History

该工程从板级 UART bring-up 逐步扩展到完整 crypto datapath、runtime observability 与多时钟域处理。

## UART Bring-up

初期先验证：

- 50 MHz board clock；
- UART RX / TX pin mapping；
- echo path；
- parser frame handling。

独立 echo / parser probe 仍保留在仓库中，便于板级定位。

## ACL 与 Crypto Integration

在 UART / parser 稳定后加入：

- ACL block path；
- SM4 single-block probe；
- AES / SM4 dual-algorithm datapath；
- multi-block stream；
- host-side known-vector test。

随后将数据通路整理为 AXI-Stream 风格的 packer / crypto engine / unpacker。

## Host Tooling

逐步增加：

- command-line probe；
- protocol layer；
- worker abstraction；
- Tkinter GUI；
- file-oriented transfer path。

## Observability

后续加入：

- frame / crypto / ACL counters；
- per-rule hit counters；
- PMU；
- on-chip benchmark；
- trace buffer；
- watchdog / recovery path。

## CDC 与 Throughput Path

为分离不同执行阶段，进一步加入：

- async FIFO；
- ingress / egress CDC；
- skid buffer；
- 125 MHz ingress path；
- 50 MHz crypto / control path。

当前 `main` 的结构、接口与验证结果以根目录 README、`RX50T_CURRENT_BASELINE.md` 和 `BUILD_AND_TEST.md` 为准。

# RX50T UART Crypto Gateway Board Test

## Board Baseline

- Board: `RX50T`
- FPGA: `xc7a50tfgg484-1`
- Clock: `50 MHz`
- UART: `2,000,000 8N1`
- UART RX: `K1`
- UART TX: `J1`

串口号由主机实际枚举结果决定，以下命令统一使用 `<PORT>`。

## Bitstream

默认构建输出：

```text
contest_project\build\rx50t_uart_crypto_probe\
  rx50t_uart_crypto_probe.runs\impl_1\
  rx50t_uart_crypto_probe_board_top.bit
```

构建和烧录方法见 [BUILD_AND_TEST.md](BUILD_AND_TEST.md)。

## Python Dependency

```powershell
py -3 -m pip install -r requirements-dev.txt
```

## Stats Query

```powershell
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --query-stats
```

## SM4 Known Vector

```powershell
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --sm4-known-vector
```

Expected ciphertext:

```text
68 1e df 34 d2 06 96 5e 86 b3 e9 4f 53 6e 42 46
```

## AES Known Vector

```powershell
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --aes-known-vector
```

Expected ciphertext:

```text
69 c4 e0 d8 6a 7b 04 30 d8 cd b7 80 70 b4 c5 5a
```

## ACL Block Path

```powershell
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --block-ascii XYZ
```

## PMU / Trace

```powershell
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --query-pmu
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --query-trace
```

## Validation Key Scope

当前 board baseline 使用固定的 AES / SM4 标准测试向量 key 进行功能验证。runtime key provisioning 不属于当前实现范围。

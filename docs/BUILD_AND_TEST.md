# Build and Test

本文给出当前 RX50T 主线的最小构建、仿真和板级验证入口。

## 1. 依赖

- Xilinx Vivado 2024.1
- Python 3.10+
- PowerShell
- `pyserial`
- `pytest`

安装 Python 依赖：

```powershell
py -3 -m pip install -r requirements-dev.txt
```

如果 Vivado 不在默认安装目录，可以设置：

```powershell
$env:VIVADO_BIN = "C:\Xilinx\Vivado\2024.1\bin\vivado.bat"
```

也可以使用 `RX50T_VIVADO_BAT`。

## 2. 主线构建

当前主线顶层：

```text
contest_project/rtl/contest/rx50t_uart_crypto_probe_board_top.sv
```

执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\contest_project\scripts\build_rx50t_uart_crypto_probe.ps1
```

默认构建目录：

```text
contest_project/build/rx50t_uart_crypto_probe/
```

对应 bitstream：

```text
contest_project/build/rx50t_uart_crypto_probe/
  rx50t_uart_crypto_probe.runs/impl_1/
  rx50t_uart_crypto_probe_board_top.bit
```

构建脚本同时生成 implementation timing、utilization、DRC 和 CDC report。

## 3. RTL / Testbench

代表性 testbench：

```text
tb_contest_crypto_axis_core.sv
tb_uart_crypto_probe.sv
tb_uart_crypto_probe_acl_v2.sv
tb_uart_crypto_probe_cdc_ingress.sv
tb_uart_crypto_probe_cdc_egress.sv
tb_uart_crypto_probe_watchdog.sv
tb_uart_crypto_probe_trace.sv
```

对应 PowerShell / TCL 入口位于：

```text
contest_project/scripts/
```

例如：

```powershell
powershell -ExecutionPolicy Bypass -File .\contest_project\scripts\build_tb_contest_crypto_axis_core.ps1
powershell -ExecutionPolicy Bypass -File .\contest_project\scripts\build_tb_uart_crypto_probe_watchdog.ps1
```

## 4. Python 测试

```powershell
py -3 -m pytest .\contest_project\tools -q
```

Python 测试覆盖 protocol handling、worker、GUI logic 与 host-side probe behavior。

## 5. 板卡烧录

列出 JTAG 设备：

```powershell
powershell -ExecutionPolicy Bypass -File .\contest_project\scripts\program_hw_target.ps1 -ListDevices
```

烧录默认主线 bitstream：

```powershell
powershell -ExecutionPolicy Bypass -File .\contest_project\scripts\program_hw_target.ps1
```

如果同时连接多个 JTAG 设备：

```powershell
powershell -ExecutionPolicy Bypass -File .\contest_project\scripts\program_hw_target.ps1 -HwDeviceIndex 0
```

## 6. UART Smoke Test

主线 board top 默认使用：

```text
50 MHz clock
2,000,000 baud
```

串口号由实际机器决定，不在源码中固定。

查询 counters：

```powershell
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --query-stats
```

验证 AES / SM4 known vector：

```powershell
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --aes-known-vector
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --sm4-known-vector
```

查询 PMU 与 trace：

```powershell
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --query-pmu
py -3 .\contest_project\tools\send_rx50t_crypto_probe.py --port <PORT> --baud 2000000 --query-trace
```

## 7. Legacy Bring-up Probes

仓库保留 UART echo、parser、ACL 和 SM4 单功能 probe，主要用于板卡 bring-up 与模块级定位。

这些 probe 的 board top 默认仍为 115200 baud，与 2 Mbps 的当前 crypto gateway 主线分开。

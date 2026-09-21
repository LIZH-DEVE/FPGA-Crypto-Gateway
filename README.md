# FPGA 加密网关：RX50T 板级完整实现

基于 **Xilinx Artix-7 XC7A50T / RX50T** 的 pure-PL 加密网关工程。

主线从 UART 输入开始，在 FPGA 内完成协议解析、ACL 过滤、AES / SM4 数据处理、运行状态观测与异常恢复，并通过 UART 返回结果。仓库包含 RTL、SystemVerilog testbench、Vivado 构建脚本和 Python 上位机工具。

## 数据通路

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

## 主要功能

- **UART**：当前主线 2,000,000 baud 板级通信；
- **Protocol Parser**：frame、length、payload 与错误处理；
- **ACL**：8-slot runtime rule table、hit counter、pass / block；
- **AXI-Stream**：valid / ready backpressure 与 block stream；
- **AES / SM4**：128-bit block processing，覆盖 16B / 32B / 64B / 128B 路径；
- **CDC / Buffering**：async FIFO、skid buffer 与 ingress / egress bridge；
- **Watchdog**：stream / crypto timeout recovery；
- **PMU**：运行周期、stall、ACL block 与 stream counters；
- **Trace Buffer**：板上事件记录与 UART readback；
- **Host Tools**：CLI、protocol layer、worker 与 Tkinter GUI。

## 代码结构

```text
contest_project/
├── rtl/contest/       # 主 RTL
├── tb/contest/        # SystemVerilog testbench
├── constraints/       # RX50T constraints
├── scripts/           # Vivado build / simulation / programming
├── tools/             # Python CLI / GUI / protocol tools
└── demo_assets/       # known-vector / demo inputs

docs/                  # 架构、构建、验证与开发记录
reference/             # 第三方/参考 RTL 与 testbench
```

## 当前主线

板级顶层：

```text
contest_project/rtl/contest/rx50t_uart_crypto_probe_board_top.sv
```

默认配置：

| 项目 | 配置 |
| --- | --- |
| FPGA | Xilinx Artix-7 XC7A50T |
| Clock | 50 MHz |
| UART | 2,000,000 baud |
| UART RX / TX | K1 / J1 |

核心实现包括：

- `contest_parser_core.sv`
- `contest_acl_axis_core.sv`
- `contest_axis_block_packer.sv`
- `contest_crypto_block_engine.sv`
- `contest_axis_block_unpacker.sv`
- `contest_async_axis_fifo.sv`
- `contest_trace_buffer.sv`
- `contest_uart_crypto_probe.sv`

更完整的模块关系见 [Implementation Guide](docs/IMPLEMENTATION_GUIDE.md)。

## Build / Test

安装 Python 依赖：

```powershell
py -3 -m pip install -r requirements-dev.txt
```

构建主线：

```powershell
powershell -ExecutionPolicy Bypass -File .\contest_project\scripts\build_rx50t_uart_crypto_probe.ps1
```

如果 Vivado 不在默认位置：

```powershell
$env:VIVADO_BIN = "C:\Xilinx\Vivado\2024.1\bin\vivado.bat"
```

运行 host-side tests：

```powershell
py -3 -m pytest .\contest_project\tools -q
```

完整构建、仿真、烧录和板级 smoke test 入口见 [Build and Test](docs/BUILD_AND_TEST.md)。

## 验证

当前主线完成 simulation、implementation 与 real-board 验证。

代表性 implementation 结果：

| 指标 | 结果 |
| --- | ---: |
| WNS | **6.392 ns** |
| WHS | **0.035 ns** |
| Slice LUTs | **3794（11.64%）** |
| Slice Registers | **5449（8.36%）** |
| Block RAM Tile | **4.5（6.00%）** |
| DSP | **0** |

板级验证覆盖：

- AES / SM4 known vector；
- ACL block / recovery；
- stats / PMU query；
- watchdog；
- multi-block file traffic；
- trace readback。

当前 UART end-to-end 文件流量记录约为：

- 32 KB AES / SM4：0.780 Mbps；
- 512 KB AES / SM4：0.787 Mbps。

该结果主要受 2 Mbps UART 链路约束，不代表密码核心峰值吞吐。

## Validation Key

当前 board baseline 使用固定的 AES / SM4 标准测试向量 key 进行功能和数据通路验证。

runtime key provisioning 不属于当前实现范围。

## 上位机工具

`contest_project/tools/` 包含：

- `send_rx50t_crypto_probe.py`：板级 CLI；
- `crypto_gateway_protocol.py`：protocol handling；
- `crypto_gateway_worker.py`：serial worker；
- `rx50t_crypto_gui.py`：Tkinter GUI；
- 对应 host-side tests。

串口号不在源码中绑定到具体开发机；GUI 只在检测到唯一串口时自动选择。

## 文档

- [Build and Test](docs/BUILD_AND_TEST.md)
- [Implementation Guide](docs/IMPLEMENTATION_GUIDE.md)
- [当前 Baseline](docs/RX50T_CURRENT_BASELINE.md)
- [架构说明](docs/RX50T_ARCHITECTURE_OVERVIEW.md)
- [开发历程](docs/DEVELOPMENT_HISTORY.md)
- [当前板级验证](docs/RX50T_UART_CRYPTO_PROBE_BOARD_TEST.md)

## Legacy Bring-up Probes

仓库保留 UART echo、parser、ACL 与 SM4 单功能 probe，用于板级 bring-up 和模块级故障定位。

这些 probe 的 board top 默认使用 115200 baud，与当前 2 Mbps crypto gateway 主线分开。

## 第三方代码

AES / SM4 算法核心采用公开参考实现，并保留原始版权与许可信息。

详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

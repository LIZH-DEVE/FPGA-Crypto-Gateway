# 开发内容概览

## AXI-Lite control path

实现 `axil_csr.sv`，用于将 software-side register access 转换为 DMA / runtime control signals，并维护 status 与 descriptor-ring 相关寄存器。

## AXI4 DMA write path

`dma_master_engine.sv` 处理：

- AXI4 write address / data / response channel；
- multi-burst transfer；
- 4 KB boundary split；
- 32-bit data path；
- downstream backpressure。

## Descriptor ring

`dma_desc_fetcher.sv` 维护 hardware head pointer，并根据 software tail pointer 从 DDR 中读取 descriptor，再触发 DMA 执行。

## CDC

`async_fifo.sv` 使用 binary / Gray-code pointer 与双级同步器处理跨时钟域数据传输。

## Buffer management

`pbm_controller.sv` 使用 reserve / commit pointer 区分正在写入与已提交数据，并在 error 条件下执行 rollback。

## Width conversion

`gearbox_128_to_32.sv` 将 128-bit block 拆分为四个 32-bit beat，用于连接宽计算数据与较窄 DMA path。

## 验证

`tb/tb_dma_boundary.sv` 用于检查跨 4 KB boundary 的 Burst 拆分行为。

这些内容来自原 Zynq heterogeneous datapath 开发过程，迁入后作为 RX50T pure-PL 主线之外的 SoC / data movement 补充。

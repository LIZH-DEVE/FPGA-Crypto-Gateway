# Zynq Datapath 迁移审计

本文件记录从原 `fpga-heterogeneous-datapath` 合并到当前仓库时的取舍，目的是区分“遗漏”与“有意不迁移”。

## 已逐字迁移并核对 blob identity

以下文件在迁移前后 Git blob SHA 一致：

- `rtl/core/axil_csr.sv`
- `rtl/core/async_fifo.sv`
- `rtl/core/gearbox_128_to_32.sv`
- `rtl/core/pbm/pbm_controller.sv`
- `rtl/core/dma/dma_master_engine.sv`
- `rtl/core/dma/dma_desc_fetcher.sv`
- `rtl/if/axi_lite_if.sv`
- `rtl/if/axi_stream_if.sv`
- `rtl/inc/pkg_axi_stream.sv`
- `rtl/inc/sync_fifo.sv`
- `tb/tb_dma_boundary.sv`

这些文件均为 byte-identical copy，没有在迁移过程中被改写。

## 有意不迁移：与 RX50T 主线重复

以下内容在 RX50T 主线已有更完整实现，因此不重复迁移：

- AES / SM4 第三方算法核心；
- crypto dispatcher / crypto wrapper；
- Ethernet / IP / UDP parser；
- TX stack；
- display driver；
- crypto golden vectors。

## 有意不迁移：旧 top-level 依赖重复模块

以下文件没有迁入当前 active tree：

- `rtl/top/dma_subsystem.sv`
- `rtl/top/crypto_dma_subsystem.sv`
- `rtl/core/dma/dma_subsystem_wrapper.v`

原因是这些 top-level 同时依赖旧 parser、TX、display 或 crypto path。单独复制会形成 unresolved dependency；把全部依赖一起迁移又会重新制造与 RX50T 主线的重复代码。

因此当前 `zynq-datapath/` 定位为经过整理的 **AXI / CDC / DMA / buffer 模块集合**，不是原 Zynq Vivado 工程的 byte-for-byte standalone clone。

## 有意不迁移：已过期或与现行 RTL 不一致

### `tb/tb_dma_master_engine.sv`

旧 testbench 仍连接 `o_error`，而现行 `dma_master_engine` 已没有该 port。直接迁入会导致编译接口不一致，因此没有作为当前验证入口。

当前保留 `tb_dma_boundary.sv`，用于验证 4 KB boundary split。

### `software/zynq_crypto_control.c`

旧示例把 `0x10` 当作 `algo_sel` register，但现行 `axil_csr.sv` 中：

- `0x00` 是 control register；
- `algo_sel` 位于 control bit 2；
- `0x10` 是 key word 0。

因此该软件示例与当前 CSR map 不一致，不迁入 active tree。

### `vivado/system.bd`

该 Block Design snapshot 引用旧 `dma_subsystem_wrapper` 和原工程生成 IP。由于 wrapper/top-level 没有迁入，单独放入当前目录会制造一个无法独立复现的 Vivado 工程入口，因此不作为 active source 迁入。

## 已以整理版保留

原 `doc/development-history.md` 的有效内容已整理到：

- `docs/development-overview.md`

原 DMA Done stall 调试记录保留在：

- `docs/dma-done-stall.md`

## 结论

本次合并不是整仓复制，而是一次有意的 curated migration：

- 保留与 FPGA data movement 直接相关、且可独立理解的模块；
- 去掉 RX50T 已覆盖的重复 crypto / protocol 内容；
- 不把接口已经过期或依赖不完整的旧文件放进 active tree；
- 原仓库仍保留完整历史，可用于追溯。

因此不存在已迁移文件内容损坏；未迁入内容均已在本审计中分类说明。

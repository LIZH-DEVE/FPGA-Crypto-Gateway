# DMA Done stall 调试记录

## 现象

subsystem testbench 在等待 `dma_done` 时超时。

## 排查路径

主要检查了四类可能原因：

1. PBM 输入是否遵守 `valid / ready` 握手；
2. Crypto Bridge 状态机是否完成当前 transaction；
3. DMA engine 是否接收到有效启动条件；
4. Descriptor fetcher 是否正确解析任务描述。

## 根因与修正

测试数据注入阶段没有等待 `rx_wr_ready`，可能在 PBM 尚未接受数据时继续推进输入。

修正后的 testbench 在发送每个 word 前等待 handshake 条件满足，再继续下一个 word。随后重新验证 descriptor trigger 与 DMA completion path。

## 调试方法

该问题采用逐层隔离方式处理：

- 先验证 PBM 写入；
- 再验证 Crypto / Gearbox；
- 再绕开 Fetcher 使用 CSR 直接启动 DMA；
- 最后恢复 descriptor path。

这种方式可以将“系统级 timeout”缩小为具体模块之间的 handshake 问题。

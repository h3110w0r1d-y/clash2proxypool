# 代理池脚本

## 功能简介

脚本主要为了解决 glider 配置复杂、不支持部分 协议/vless链接 的问题，可直接将clash订阅配置拆分成每个只包含一个节点的配置文件，批量启动mihomo，通过glider提供自动切换节点的功能。

## 快速使用

1. 下载对应平台的[Glider](https://github.com/nadoo/glider/releases)和[Mihomo](https://github.com/MetaCubeX/mihomo/releases)
2. 重命名可执行文件为 `glider` 和 `mihomo`, 放到项目根目录并给执行权限
3. 将Clash配置文件重命名为 `mihomo.yaml` 放到项目根目录
4. 启动脚本

    ```bash
    python3 main.py
    # 按 Ctrl+C 退出
    ```

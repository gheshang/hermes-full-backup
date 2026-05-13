---
title: VPS 初始化脚本
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [vps, self-hosted, deploy]
sources: [raw/articles/vps-init-script-guide.md]
---

# VPS 初始化脚本

Ubuntu/Debian服务器一键初始化，交互菜单版，14项功能。

## 4组架构

| 组 | 功能 | 数量 |
|----|------|------|
| 基础环境 | 系统更新/时区/DNS优化 | 3 |
| 内核调优 | BBR/Swap/IPv4优先 | 3 |
| 工具安装 | 基础工具/Docker | 2 |
| 系统加固 | SSH/防火墙/Fail2Ban/自动更新/内核加固/禁用服务 | 6 |

## 关键设计决策

- **交互菜单** — 每项独立函数`stepN_xxx()`，可单跑/全跑/退出
- **组4有依赖** — SSH端口变更→防火墙必须联动放行新端口
- **每步立即生效** — sysctl写完就`sysctl --system`，不攒

## 7个踩坑

1. DNS锁定：不管有没有NetworkManager都`chattr +i`
2. Swap：用`dd`不用`fallocate`（兼容ZFS/Btrfs）
3. Fail2Ban：必须补[DEFAULT]段
4. NTP：云服务器不支持，删掉
5. GitHub下载：必须用raw链接
6. 端口+防火墙顺序：先放行再启
7. sysctl：每步立即生效

## 不纳入的功能

AIDE/RKHunter/auditd太重误报多；创建非root用户需交互密码；logwatch需邮件服务器。

## 关联

- [[hermes-agent]] — 部署在VPS上的agent
- [[hermes-config-setup]] — VPS初始化后的Hermes配置

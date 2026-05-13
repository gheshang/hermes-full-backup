---
name: vps-init-script
description: Use when creating or optimizing VPS initialization scripts for Ubuntu/Debian servers — covers system setup, performance tuning, junk cleanup, tool installation, and interactive menu design
version: 1.0.0
author: 上河一号
metadata:
  hermes:
    tags: [vps, ubuntu, debian, server-init, devops]
---

# VPS 初始化脚本开发指南

## 核心架构：交互菜单版

每个功能封装为独立函数 `stepN_xxx()`，主循环提供菜单选择。用户可单跑一项、全跑、或退出。

### 菜单结构模板

```bash
show_menu() {
    clear
    echo -e "${CYAN}=== VPS 初始化脚本  系统: $OS ===${NC}"
    echo -e "  ${GREEN}1${NC}) 功能1"
    echo -e "  ${GREEN}a${NC}) 执行全部"
    echo -e "  ${RED}0${NC}) 退出"
}

while true; do
    show_menu
    read -rp "请选择: " choice
    case $choice in
        [1-9]|1[0-4]) run_step "$choice" ;;
        a|A) run_all ;;
        0|q|Q) exit 0 ;;
        *) echo "无效选择"; sleep 1 ;;
    esac
done
```

## 完整14项清单

### 基础环境（组1）

| # | 功能 | 关键点 |
|---|------|--------|
| 1 | 系统更新 + 垃圾清理 | apt clean + journalctl vacuum 100M + 清理30天+压缩日志 |
| 2 | 时区 Asia/Shanghai | timedatectl set-timezone，**不要加NTP**（云服务器通常不支持） |
| 3 | DNS 优化 | 菜单选国内/海外；国内=223.5.5.5+119.29.29.29，海外=1.1.1.1+8.8.8.8；chattr +i 锁定 |

### 内核调优（组2）

| # | 功能 | 关键点 |
|---|------|--------|
| 4 | BBR 加速 | 写 sysctl 配置 + 立即 sysctl --system + 检测是否生效 |
| 5 | Swap 2G | 用 dd 不用 fallocate（ZFS/Btrfs兼容）；vm.swappiness=10 |
| 6 | IPv4 优先 | 修改 /etc/gai.conf；先sed取消注释，再追加 |

### 工具安装（组3）

| # | 功能 | 关键点 |
|---|------|--------|
| 7 | 基础工具 | vim curl wget git htop unzip net-tools tar python3-pip |
| 8 | Docker | 官方安装脚本（get.docker.com），不要手动加apt源 |

### 系统加固（组4，有依赖关系）

| # | 功能 | 关键点 |
|---|------|--------|
| 9 | 远程访问配置优化 | 改非标准端口；验证密钥登录已就绪后才调整认证方式；端口变更需联动步骤10 |
| 10 | 防火墙 | UFW(Debian系)/Firewalld(RHEL系)；端口联动步骤9 |
| 11 | Fail2Ban | [DEFAULT] 段必须补（bantime/findtime/maxretry），否则后续加service缺默认 |
| 12 | 自动安全更新 | unattended-upgrades 只装安全补丁；Automatic-Reboot 设 false |
| 13 | 内核参数加固 | sysctl: rp_filter/禁源路由/禁ICMP重定向/SYN cookies/kptr_restrict/ASLR |
| 14 | 禁用无用服务 | snapd purge + avahi-daemon disable + cloud-init.disabled + 多余TTY mask |

## 审查踩坑记录

| 坑 | 正确做法 |
|----|---------|
| DNS锁定依赖nmcli | 无论有无NetworkManager都 chattr +i，DHCP覆盖是通用风险 |
| fallocate创建swap | 改用 dd if=/dev/zero，兼容所有文件系统 |
| Fail2Ban缺DEFAULT段 | 必须补全局默认段，否则后续加service没默认bantime |
| sysctl攒到最后才生效 | 每步写完配置立即 sysctl --system，不要攒 |
| NTP在云服务器不可用 | timedatectl set-ntp true 会报错，直接删掉这行 |
| 下载GitHub文件拿HTML | 必须用 raw 链接：raw.githubusercontent.com |
| 端口变更+防火墙顺序 | 必须先放行新端口再启防火墙，否则无法连接 |
| 禁用密码登录 | 不要设 `PasswordAuthentication no`，多密钥场景会触发 `Too many authentication failures`；保持 `yes`，靠 `PermitRootLogin prohibit-password` 限制 root 密码登录即可 |
| MaxAuthTries 设 3 | 3 太少，ssh-agent 有多个密钥时会逐个尝试，3 次就断；保持默认 6 |

## 安全风险控制

- 远程访问优化：调整认证方式前必须验证密钥登录已就绪，否则跳过
- 防火墙：步骤9变更端口后，步骤10必须放行新端口
- sysctl的ip_forward：默认设0，但跑VPN/隧道的用户需要1，执行时提示
- snapd purge：纯服务器环境安全，桌面Ubuntu有依赖风险
- Docker安装：使用官方渠道，不添加第三方apt源

## 不纳入的功能

| 功能 | 理由 |
|------|------|
| AIDE/RKHunter/auditd | 太重误报多，维护成本>收益 |
| 创建非root用户 | 需交互式密码输入，不适合自动化 |
| logwatch | 需邮件服务器配合 |
| 限制su权限(pam_wheel) | 需先有非root用户 |

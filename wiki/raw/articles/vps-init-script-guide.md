---
source_url: https://github.com/hermes-agent/skills/tree/main/devops/vps-init-script
ingested: 2026-04-24
sha256: embedded-from-skill
---

# VPS 初始化脚本开发指南

## 完整14项清单

### 基础环境（组1）
1. 系统更新+垃圾清理 — apt clean + journalctl vacuum 100M + 清理30天+压缩日志
2. 时区Asia/Shanghai — timedatectl set-timezone，不要加NTP（云服务器通常不支持）
3. DNS优化 — 菜单选国内/海外；国内=223.5.5.5+119.29.29.29，海外=1.1.1.1+8.8.8.8；chattr +i锁定

### 内核调优（组2）
4. BBR加速 — 写sysctl配置+立即sysctl --system+检测是否生效
5. Swap 2G — 用dd不用fallocate（ZFS/Btrfs兼容）；vm.swappiness=10
6. IPv4优先 — 修改/etc/gai.conf；先sed取消注释，再追加

### 工具安装（组3）
7. 基础工具 — vim curl wget git htop unzip net-tools tar python3-pip
8. Docker — 官方安装脚本（get.docker.com），不要手动加apt源

### 系统加固（组4，有依赖关系）
9. 远程访问配置优化 — 改非标准端口；验证密钥登录已就绪后才调整认证方式；端口变更需联动步骤10
10. 防火墙 — UFW(Debian系)/Firewalld(RHEL系)；端口联动步骤9
11. Fail2Ban — [DEFAULT]段必须补（bantime/findtime/maxretry），否则后续加service缺默认
12. 自动安全更新 — unattended-upgrades只装安全补丁；Automatic-Reboot设false
13. 内核参数加固 — sysctl: rp_filter/禁源路由/禁ICMP重定向/SYN cookies/kptr_restrict/ASLR
14. 禁用无用服务 — snapd purge + avahi-daemon disable + cloud-init.disabled + 多余TTY mask

## 审查踩坑记录

| 坑 | 正确做法 |
|----|---------|
| DNS锁定依赖nmcli | 无论有无NetworkManager都chattr +i，DHCP覆盖是通用风险 |
| fallocate创建swap | 改用dd if=/dev/zero，兼容所有文件系统 |
| Fail2Ban缺DEFAULT段 | 必须补全局默认段，否则后续加service没默认bantime |
| sysctl攒到最后才生效 | 每步写完配置立即sysctl --system，不要攒 |
| NTP在云服务器不可用 | timedatectl set-ntp true会报错，直接删掉这行 |
| 下载GitHub文件拿HTML | 必须用raw链接：raw.githubusercontent.com |
| 端口变更+防火墙顺序 | 必须先放行新端口再启防火墙，否则无法连接 |

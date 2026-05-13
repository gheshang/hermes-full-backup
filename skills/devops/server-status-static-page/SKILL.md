---
name: server-status-static-page
description: 采集服务器硬件/系统/服务信息，生成单文件静态HTML展示页。适用于VPS状态展示、服务器信息归档、内部运维看板。
version: 1.0
---

# 服务器状态静态页生成

## 触发条件
- 用户要做服务器信息展示网站/页面
- 用户要查看服务器配置并要求可视化
- 用户说"服务器状态页"/"server status page"/"homelab dashboard"

## 流程

### 1. 数据采集（10项）

```bash
hostname                    # 主机名
cat /etc/os-release         # OS版本
uname -r                    # 内核
lscpu                       # CPU型号/核心/线程
free -h                     # 内存
df -h                       # 磁盘
uptime -p                   # 运行时长
ip -4 addr show             # 网络接口
cat /proc/loadavg           # 负载
swapon --show               # Swap
```

可选采集（按需）：
```bash
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader  # GPU
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'                   # Docker容器
systemctl list-units --type=service --state=running --no-pager                    # 运行中服务
```

### 2. 公网IP采集（坑点）

**不要用** `curl ifconfig.me` 或 `curl ip.sb`——在很多VPS环境会超时60秒无返回。

替代方案（按优先级）：
1. `ip route get 1.1.1.1 | awk '{print $7; exit}'` ——只取内网IP，秒回
2. 如果确实需要公网IP，用 `curl -s --connect-timeout 3 ipinfo.io/ip`，设超时防卡死
3. 采集超时则跳过，页面标注"未获取"

### 3. 生成HTML

- 单文件HTML，内联CSS，零外部依赖
- 暗色主题（#0a0e17背景），运维风格
- 卡片式布局，grid自适应
- 用量条用颜色梯度：绿(<60%) / 黄(60-85%) / 红(>85%)
- 服务列表用tag式排列

### 4. 输出路径

默认 `~/server-status/index.html`，用户可指定。

### 5. 自动刷新方案（用户追问时给）

- **Cron重新生成**：写采集脚本+cron定时跑，输出覆盖同一HTML文件
- **动态化**：Python Flask/FastAPI 后端实时采集，页面JS轮询刷新

## 坑点
- 公网IP采集接口不稳定，必须设超时或跳过
- `lscpu`输出格式因CPU不同有差异，只grep固定字段
- Docker未安装时`docker ps`会报错，必须2>/dev/null兜底
- `systemctl`在非systemd环境无效，同样需要错误处理

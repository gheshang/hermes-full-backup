# UV 缓存清理陷阱 — `~/.cache/uv` vs `~/.local/share/uv`

## 问题描述

用户执行 `uv cache clean` 后，发现只释放了约 170M 空间，但 `du -sh ~/.local/share/uv` 显示有 5.7G。

## 根因

`uv cache clean` **只清理 `~/.cache/uv/`**，**不触碰 `~/.local/share/uv/`**。

| 目录 | 内容 | 命令 | 大小 |
|------|------|------|------|
| `~/.cache/uv/` | 临时缓存、下载缓存 | `uv cache clean` | ~175M |
| `~/.local/share/uv/` | 已安装包、索引、项目 | **无自动清理命令** | 可达 5G+ |

## `~/.local/share/uv/` 目录结构

```
~/.local/share/uv/
├── builds/       # 已安装的 wheel 包（可删，下次安装会重新下载）
├── index/        # 包索引缓存（可删，下次会重新拉取）
├── projects/     # 项目虚拟环境（谨慎删除，可能正在使用）
└── wheels/       # 预构建的 wheel 文件（可删）
```

## 清理策略

### 安全清理（推荐）

```bash
# 只删 builds 和 index，保留 projects
rm -rf ~/.local/share/uv/builds ~/.local/share/uv/index
```

释放空间：通常 2-5G

### 激进清理（最大释放）

```bash
rm -rf ~/.local/share/uv/builds ~/.local/share/uv/index ~/.local/share/uv/projects
```

⚠️ **警告**：这会删除所有 UV 创建的项目虚拟环境，需要重新安装依赖。

## 诊断命令

```bash
# 查看 UV 各目录占用
du -sh ~/.local/share/uv/* 2>/dev/null | sort -hr

# 查看 uv cache 目录（uv cache clean 实际清理的）
du -sh ~/.cache/uv 2>/dev/null

# 查看 uv 缓存目录位置
uv cache dir
```

## 预防措施

### 1. 定期清理 builds 和 index

```bash
# 每月执行一次
rm -rf ~/.local/share/uv/builds ~/.local/share/uv/index
```

### 2. 使用 `uv cache prune` 代替 `uv cache clean`

```bash
uv cache prune --ci  # 清理未使用的缓存
```

### 3. 监控 UV 数据大小

在磁盘监控脚本中加入：

```bash
UV_SIZE=$(du -sh ~/.local/share/uv 2>/dev/null | awk '{print $1}')
UV_CACHE_SIZE=$(du -sh ~/.cache/uv 2>/dev/null | awk '{print $1}')
echo "UV data: $UV_SIZE, UV cache: $UV_CACHE_SIZE"
```

## 参考

- [UV 官方文档 - 缓存管理](https://docs.astral.sh/uv/concepts/cache/)
- [UV 官方文档 - 目录结构](https://docs.astral.sh/uv/concepts/cache/#cache-directories)

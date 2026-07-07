#!/usr/bin/env python3
"""
连州及广东省招聘信息每日爬取脚本 — 模板
监控站点：
  1. 连州市公务员招考: https://www.lianzhou.gov.cn/xxgk/rsxx/gwyzk/
  2. 连州市事业单位招聘: https://www.lianzhou.gov.cn/xxgk/rsxx/sydwzp/
  3. 清远教师招聘网: https://www.jrzhufu.com/news/news_81.html
  4. 清远事业单位招聘汇总: https://www.yingyudengji.com/news/news_81.html
  5. 广东省人力资源和社会保障厅: https://hrss.gd.gov.cn/
  6. 广东组织工作网: https://www.gdzz.gov.cn/tzgg/

用法:
  python3 lianzhou_jobs_crawler.py

部署到 crontab:
  0 8 * * * cd /home/hangskf && python3 ~/.hermes/scripts/lianzhou_jobs_crawler.py >> ~/.hermes/cron/lian-zhou-jobs/cron.log 2>&1

依赖:
  pip install requests beautifulsoup4
"""

import json
import logging
import os
import re
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ── 配置 ──────────────────────────────────────────────────────────────
BASE_DIR = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
JOB_DIR = BASE_DIR / "cron" / "lian-zhou-jobs"
HISTORY_FILE = JOB_DIR / "history.json"
LOG_FILE = JOB_DIR / "cron.log"
FEISHU_TARGET = "oc_addcf625fbc28593ae333213a775661e"

# 站点定义: (name, url, parser_func)
SITES = [
    ("连州市公务员招考", "https://www.lianzhou.gov.cn/xxgk/rsxx/gwyzk/", parse_lianzhou_gwy),
    ("连州市事业单位招聘", "https://www.lianzhou.gov.cn/xxgk/rsxx/sydwzp/", parse_lianzhou_sydw),
    ("清远教师招聘网", "https://www.jrzhufu.com/news/news_81.html", parse_qyjszp),
    ("清远事业单位招聘汇总", "https://www.yingyudengji.com/news/news_81.html", parse_yydwzp),
    ("广东省人社厅", "https://hrss.gd.gov.cn/", parse_gd_hrss),
    ("广东组织工作网", "https://www.gdzz.gov.cn/tzgg/", parse_gd_organ),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
REQUEST_TIMEOUT = 15

# ── 日志 ──────────────────────────────────────────────────────────────
JOB_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("jobs_crawler")


# ── 工具 ──────────────────────────────────────────────────────────────
def fetch(url: str) -> Optional[str]:
    """GET 请求，失败返回 None。"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        log.error(f"GET {url} 失败: {e}")
        return None


def url_hash(url: str) -> str:
    """URL 唯一标识。"""
    return hashlib.md5(url.encode()).hexdigest()[:12]


def extract_links(soup: BeautifulSoup, base_url: str, selector: str,
                  title_tag: str = "a", title_attr: str = "text",
                  link_attr: str = "href") -> list[dict]:
    """通用链接提取。"""
    results = []
    for el in soup.select(selector):
        a = el.select_one(title_tag)
        if not a:
            continue
        title = a.get_text(strip=True)
        if not title:
            continue
        href = a.get(link_attr, "")
        if not href:
            continue
        url = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
        results.append({"title": title, "url": url})
    return results


def clean_date(raw: str) -> Optional[str]:
    """尝试解析日期字符串为 YYYY-MM-DD。"""
    patterns = [
        r"(\d{4})[-/\.](\d{1,2})[-/\.](\d{1,2})",
        r"(\d{1,2})月(\d{1,2})日",
    ]
    for pat in patterns:
        m = re.search(pat, raw)
        if m:
            groups = m.groups()
            if len(groups) == 3 and len(groups[0]) == 4:
                return f"{groups[0]}-{int(groups[1]):02d}-{int(groups[2]):02d}"
            elif len(groups) == 2:
                year = datetime.now().year
                return f"{year}-{int(groups[0]):02d}-{int(groups[1]):02d}"
    return datetime.now().strftime("%Y-%m-%d")


# ── 站点解析器 ────────────────────────────────────────────────────────
# 注意：各网站 HTML 结构可能变化，首次运行后需检查 cron.log 确认每个站点
# 是否成功提取了数据。如果某个站点提取数为 0，需要调整对应解析器。

def parse_lianzhou_gwy(html: str, base_url: str) -> list[dict]:
    """连州市公务员招考列表页。"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for row in soup.select("li, .list-item, .news-list li, ul li"):
        a = row.select_one("a")
        if not a:
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 3:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
        date_text = row.get_text()
        date_str = clean_date(date_text)
        items.append({"title": title, "url": url, "date": date_str, "source": "连州市公务员招考"})
    return items


def parse_lianzhou_sydw(html: str, base_url: str) -> list[dict]:
    """连州市事业单位招聘列表页。"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for row in soup.select("li, .list-item, .news-list li, ul li"):
        a = row.select_one("a")
        if not a:
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 3:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
        date_text = row.get_text()
        date_str = clean_date(date_text)
        items.append({"title": title, "url": url, "date": date_str, "source": "连州市事业单位招聘"})
    return items


def parse_qyjszp(html: str, base_url: str) -> list[dict]:
    """清远教师招聘网。"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for row in soup.select("tr, .news-item, .list-item"):
        a = row.select_one("a")
        if not a:
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 3:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
        items.append({"title": title, "url": url, "date": datetime.now().strftime("%Y-%m-%d"), "source": "清远教师招聘网"})
    return items


def parse_yydwzp(html: str, base_url: str) -> list[dict]:
    """清远事业单位招聘汇总。"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for row in soup.select("li, .news-item, .list-item, .article-item"):
        a = row.select_one("a")
        if not a:
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 3:
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
        items.append({"title": title, "url": url, "date": datetime.now().strftime("%Y-%m-%d"), "source": "清远事业单位招聘汇总"})
    return items


def parse_gd_hrss(html: str, base_url: str) -> list[dict]:
    """广东省人社厅 — 搜索招聘公告。"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for a in soup.select("a"):
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        if not any(kw in title for kw in ["招聘", "公告", "录用", "招考", "聘用", "选聘"]):
            continue
        href = a.get("href", "")
        if not href:
            continue
        url = href if href.startswith("http") else "https://hrss.gd.gov.cn" + href
        items.append({"title": title, "url": url, "date": datetime.now().strftime("%Y-%m-%d"), "source": "广东省人社厅"})
    return items


def parse_gd_organ(html: str, base_url: str) -> list[dict]:
    """广东组织工作网 — 通知公告。"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for row in soup.select("li, .news-item, .list-item, .tzgg-item"):
        a = row.select_one("a")
        if not a:
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        if not any(kw in title for kw in ["招聘", "公告", "录用", "招考", "聘用", "选聘", "通知"]):
            continue
        href = a.get("href", "")
        url = href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
        items.append({"title": title, "url": url, "date": datetime.now().strftime("%Y-%m-%d"), "source": "广东组织工作网"})
    return items


# ── 核心逻辑 ──────────────────────────────────────────────────────────

def load_history() -> dict:
    """加载历史记录。"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            log.warning("history.json 损坏，重置为空")
    return {"seen_urls": {}, "daily_reports": {}}


def save_history(history: dict):
    """保存历史记录，保留最近 90 天。"""
    cutoff = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    daily_reports = {k: v for k, v in history.get("daily_reports", {}).items() if k >= cutoff}
    history["daily_reports"] = daily_reports
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def crawl_all() -> tuple[list[dict], dict]:
    """爬取所有站点，返回去重后的新职位列表。"""
    history = load_history()
    seen = history.get("seen_urls", {})
    new_jobs = []

    for name, url, parser in SITES:
        log.info(f"爬取: {name} ({url})")
        html = fetch(url)
        if html is None:
            continue
        try:
            items = parser(html, url)
        except Exception as e:
            log.error(f"{name} 解析失败: {e}")
            continue
        log.info(f"  → 提取 {len(items)} 条")

        for item in items:
            h = url_hash(item["url"])
            if h in seen:
                continue
            seen[h] = datetime.now().strftime("%Y-%m-%d")
            item["hash"] = h
            new_jobs.append(item)

    history["seen_urls"] = seen
    return new_jobs, history


def generate_report(jobs: list[dict], today: str) -> str:
    """生成 Markdown 日报。"""
    if not jobs:
        return f"# 招聘信息日报 — {today}\n\n今日无新增岗位。"

    lines = [f"# 招聘信息日报 — {today}", "", f"**今日新增 {len(jobs)} 条**", ""]
    for i, job in enumerate(jobs, 1):
        lines.append(f"### {i}. {job['title']}")
        lines.append(f"- **来源**: {job['source']}")
        lines.append(f"- **链接**: [{job['url']}]({job['url']})")
        if job.get("date"):
            lines.append(f"- **日期**: {job['date']}")
        lines.append("")

    from collections import Counter
    source_counts = Counter(j["source"] for j in jobs)
    lines.append("---")
    lines.append("")
    lines.append("## 来源分布")
    for src, cnt in source_counts.most_common():
        lines.append(f"- {src}: {cnt} 条")

    return "\n".join(lines)


def send_feishu(jobs: list[dict], today: str, total: int):
    """通过飞书 Bot API 发送到飞书群组。"""
    env_file = BASE_DIR / ".env"
    app_id = ""
    app_secret = ""
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("FEISHU_APP_ID="):
                app_id = line.split("=", 1)[1].strip()
            elif line.startswith("FEISHU_APP_SECRET="):
                app_secret = line.split("=", 1)[1].strip()

    if not app_id or not app_secret:
        log.error("飞书凭证未配置，跳过推送")
        return

    # 1. 获取 tenant_access_token
    token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    try:
        token_resp = requests.post(
            token_url,
            json={"app_id": app_id, "app_secret": app_secret},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        token_data = token_resp.json()
        if token_data.get("code") != 0:
            log.error(f"获取 tenant_access_token 失败: {token_data}")
            return
        access_token = token_data["tenant_access_token"]
    except Exception as e:
        log.error(f"请求飞书 token 失败: {e}")
        return

    # 2. 构建消息内容
    if total == 0:
        text = f"📋 招聘信息日报 ({today}) — 今日无新增岗位。"
    else:
        lines = [f"📋 招聘信息日报 ({today}) — 今日新增 {total} 条"]
        for job in jobs[:10]:
            lines.append(f"• {job['title']} [{job['source']}]")
        if total > 10:
            lines.append(f"... 还有 {total - 10} 条，详见日报文件")
        text = "\n".join(lines)

    # 3. 发送消息
    msg_url = "https://open.feishu.cn/open-apis/im/v1/messages"
    try:
        msg_resp = requests.post(
            msg_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={
                "receive_id": FEISHU_TARGET,
                "receive_id_type": "open_chat_id",
                "content_type": "text",
                "content": json.dumps({"text": text}, ensure_ascii=False),
            },
            timeout=10,
        )
        msg_data = msg_resp.json()
        if msg_data.get("code") != 0:
            log.error(f"飞书发送失败: {msg_data}")
        else:
            log.info(f"飞书推送成功: {FEISHU_TARGET}")
    except Exception as e:
        log.error(f"飞书发送异常: {e}")


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    log.info(f"========== 招聘信息爬取开始 ({today}) ==========")

    jobs, history = crawl_all()
    total = len(jobs)
    log.info(f"今日新增 {total} 条岗位")

    # 保存日报
    report_md = generate_report(jobs, today)
    report_file = JOB_DIR / f"{today}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_md)
    log.info(f"日报已保存: {report_file}")

    # 保存历史
    history["daily_reports"][today] = {
        "total": total,
        "jobs": [{k: v for k, v in j.items() if k != "hash"} for j in jobs],
    }
    save_history(history)
    log.info("历史记录已更新")

    # 飞书推送
    send_feishu(jobs, today, total)

    log.info(f"========== 招聘信息爬取结束 ({today}) ==========")
    return 0


if __name__ == "__main__":
    sys.exit(main())

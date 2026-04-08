---
name: baike-spider
description: 百度百科爬虫工具，支持抓取词条标题、摘要、正文内容及关联词条链接。触发场景：用户要求爬取百度百科词条、采集百科数据、抓取百科页面内容、分析词条关系等。
---

# 百度百科爬虫 (BaiDuBaiKeSpider)

## 运行爬虫

用户直接输入词条名称，自动处理 URL 和输出文件名：

```bash
python scripts/spider_main.py <词条名称> --count <页面数>
```

**示例：**
```bash
python scripts/spider_main.py Python --count 5
python scripts/spider_main.py 人工智能 --count 10
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `name` | 词条名称（必填），如：`Python`、`人工智能` | - |
| `--count` | 最大爬取页面数 | `10` |

## 输出

- `{name}.html` — 带样式 HTML 报告
- `{name}.json` — JSON 数据（含 title、summary、content、url）

每次运行生成独立的文件，文件名即词条名称，互不覆盖。

## 架构

```
spider_main.py        # 主程序（用户输入词条名，自动处理URL和输出）
├── url_manager.py     # URL 管理（去重、队列）
├── html_downloader.py  # 页面下载（Cookie + 多编码）
├── html_parser.py     # 内容解析（标题/摘要/正文/链接）
└── html_outputer.py   # 输出器（HTML + JSON）
```

## 反爬绕过

使用 `urllib.request` + `HTTPCookieProcessor` 管理 Cookie，完整请求头，多编码自动尝试（utf-8 → gbk → gb2312 → gb18030）。

## 扩展

- **数据库存储**：在 `html_outputer.py` 的 `collect_data()` 中添加 SQL
- **并发爬取**：用 `threading` / `asyncio` 重构 `spider_main.py`
- **增量爬取**：将 `old_urls` 持久化到文件
- **更多字段**：修改 `html_parser.py` 的 `_get_new_data()`

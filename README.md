# BaiDuBaiKeSpider

百度百科爬虫 — Python 编写的轻量级百科词条采集工具。

## 功能特性

- 抓取百度百科词条的**标题、摘要、正文内容**
- 自动发现并爬取关联词条链接（BFS 广度优先）
- 支持**中文 URL** 自动编码
- 绕过百度百科反爬机制（Cookie + 多编码兼容）
- 输出 **HTML** 和 **JSON** 两种格式
- 纯标准库 + BeautifulSoup，无重型依赖

---

## Claude Code Skill 一键安装

### 第一步：安装 Skill 文件

**方式 A：直接下载 .skill 文件（推荐）**

下载 `baike-spider.skill` 文件，放入 Claude Code 的 skills 目录：

```
~/.claude/skills/baike-spider/
```

**方式 B：从源码安装**

```bash
# Windows
xcopy /E /I BaiDuBaiKeSpider %USERPROFILE%\.claude\skills\baike-spider

# macOS / Linux
cp -r BaiDuBaiKeSpider ~/.claude/skills/baike-spider
```

### 第二步：添加权限

在 `~/.claude/settings.local.json` 的 `permissions.allow` 中添加：

```json
"Skill(baike-spider)"
```

### 第三步：安装 Python 依赖

```bash
pip install beautifulsoup4 brotli
```

### 使用

安装完成后，在 Claude Code 中直接说：

- "爬取 Python 词条"
- "爬取人工智能相关词条，5个页面"
- "采集机器学习的百科数据"

或使用命令：

```
/baike-spider 爬取人工智能词条，count=5
```

---

## 直接运行（不作为 Skill）

```bash
pip install beautifulsoup4 brotli
python spider_main.py --url https://baike.baidu.com/item/Python --count 5
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url` | 起始词条 URL | `https://baike.baidu.com/item/Python` |
| `--name` | 输出文件名（不含扩展名），默认为URL中的词条名 | 自动从URL提取 |
| `--count` | 最大爬取页面数 | `10` |

## 输出文件

- `{name}.html` — 带样式的 HTML 报告
- `{name}.json` — 结构化 JSON 数据

每次运行生成独立的文件，文件名即词条名称，互不覆盖。

## 用法示例

```bash
# 使用URL中的词条名作为文件名
python scripts/spider_main.py --url https://baike.baidu.com/item/辽宁号航空母舰 --count 20
# 输出: 辽宁号航空母舰.json, 辽宁号航空母舰.html

# 使用用户指定的有区分度的名称
python scripts/spider_main.py --url https://baike.baidu.com/item/辽宁号航空母舰 --name 辽宁舰 --count 20
# 输出: 辽宁舰.json, 辽宁舰.html
```

## 架构

```
spider_main.py        # 主程序（调度流程 + 中文URL处理）
├── url_manager.py     # URL 管理（去重、队列）
├── html_downloader.py  # 页面下载（Cookie + 多编码）
├── html_parser.py    # 内容解析（标题/摘要/正文/链接）
└── html_outputer.py  # 输出器（HTML + JSON）
```

## License

MIT

import json
import os


class HtmlOutputer(object):
    def __init__(self, entry_name='output'):
        self.entry_name = entry_name
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        filename = self.entry_name + '.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('<html><head><meta charset="utf-8">')
            f.write('<title>百度百科爬虫结果 - ' + self.entry_name + '</title>')
            f.write('<style>')
            f.write('body { font-family: "Microsoft YaHei", sans-serif; margin: 20px; background: #f5f5f5; }')
            f.write('.item { background: #fff; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }')
            f.write('.title { font-size: 22px; font-weight: bold; color: #333; }')
            f.write('.url { color: #666; font-size: 14px; margin: 5px 0; }')
            f.write('.url a { color: #4a90d9; text-decoration: none; }')
            f.write('.summary { color: #555; margin: 10px 0; line-height: 1.6; }')
            f.write('.content { color: #333; line-height: 1.8; white-space: pre-wrap; }')
            f.write('</style></head><body>')
            f.write('<h1>百度百科爬虫结果 - ' + self.entry_name + '</h1>')
            for data in self.datas:
                f.write('<div class="item">')
                f.write(f'<div class="title">{_escape(data.get("title", ""))}</div>')
                f.write(f'<div class="url"><a href="{_escape(data.get("url", ""))}">'
                        f'{_escape(data.get("url", ""))}</a></div>')
                f.write(f'<div class="summary">{_escape(data.get("summary", ""))}</div>')
                f.write(f'<div class="content">{_escape(data.get("content", ""))}</div>')
                f.write('</div>')
            f.write('</body></html>')
        print(f'[*] HTML 结果已保存到 {os.path.abspath(filename)}')

    def output_json(self):
        filename = self.entry_name + '.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.datas, f, ensure_ascii=False, indent=2)
        print(f'[*] JSON 结果已保存到 {os.path.abspath(filename)}')


def _escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

import argparse
import time
import random
import urllib.parse
import url_manager
import html_downloader
import html_parser
import html_outputer


def build_url(keyword):
    """将用户输入的词条名转换为百度百科URL"""
    encoded = urllib.parse.quote(keyword)
    return f'https://baike.baidu.com/item/{encoded}'


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    return name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('?', '_')


class SpiderMain(object):
    def __init__(self, entry_name):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer(entry_name)

    def craw(self, root_url, max_count=10):
        count = 0
        self.urls.add_new_url(root_url)

        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                count += 1
                print(f'[+] 爬取第 {count} 个页面: {new_url}')

                html_cont = self.downloader.download(new_url)
                if html_cont is None:
                    print('  [-] 下载失败，跳过')
                    continue

                new_urls, new_data = self.parser.parse(new_url, html_cont)
                if new_data is None:
                    print('  [-] 解析失败，跳过')
                    continue

                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                title = new_data.get('title', '')
                if title:
                    print(f'  [*] 标题: {title}')

                if count >= max_count:
                    print(f'\n[*] 已达到最大爬取数量 ({max_count})，停止爬取')
                    break

                time.sleep(random.uniform(1.0, 2.5))

            except Exception as e:
                print(f'  [!] 爬取出错: {e}')
                continue

        self.outputer.output_html()
        self.outputer.output_json()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='百度百科爬虫')
    parser.add_argument('name', help='词条名称，如：Python、人工智能')
    parser.add_argument('--count', type=int, default=10,
                        help='最大爬取页面数量 (默认: 10)')
    args = parser.parse_args()

    # 用户直接输入词条名，自动处理URL和文件名
    entry_name = sanitize_filename(args.name)
    url = build_url(args.name)

    print(f'[*] 百度百科 Spider 启动')
    print(f'[*] 词条名称: {args.name}')
    print(f'[*] 最大爬取数: {args.count}')
    print('=' * 50)

    spider = SpiderMain(entry_name)
    spider.craw(url, max_count=args.count)

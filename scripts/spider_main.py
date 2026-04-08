import argparse
import time
import random
import urllib.parse
import url_manager
import html_downloader
import html_parser
import html_outputer


def normalize_url(url):
    """将中文URL转换为编码后的URL"""
    # 解析 URL，判断是否包含非ASCII字符
    parsed = urllib.parse.urlparse(url)
    # 如果 netloc 或 path 包含非ASCII字符，需要编码
    if parsed.netloc or parsed.path:
        try:
            parsed.path.encode('ascii')
        except UnicodeEncodeError:
            # 对 path 进行 URL 编码
            encoded_path = urllib.parse.quote(parsed.path, safe='/:?#[]@!$&\'()*+,;=')
            url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, encoded_path,
                parsed.params, parsed.query, parsed.fragment
            ))
    return url


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url, max_count=10):
        count = 0
        # 自动处理中文URL
        root_url = normalize_url(root_url)
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
    parser.add_argument('--url', type=str,
                        default='https://baike.baidu.com/item/Python',
                        help='起始爬取URL (默认: Python词条)')
    parser.add_argument('--count', type=int, default=10,
                        help='最大爬取页面数量 (默认: 10)')
    args = parser.parse_args()

    print(f'[*] 百度百科 Spider 启动')
    print(f'[*] 起始 URL: {args.url}')
    print(f'[*] 最大爬取数: {args.count}')
    print('=' * 50)

    spider = SpiderMain()
    spider.craw(args.url, max_count=args.count)

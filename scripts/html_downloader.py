import urllib.request
import urllib.error
import time
import random


class HtmlDownloader(object):
    def __init__(self):
        # 使用文章中的方法：urllib.request + Request 对象
        self.opener = urllib.request.build_opener()
        # 添加 Cookie 支持（文章 5.1.1 节的 CookieJar 方案）
        cookie_handler = urllib.request.HTTPCookieProcessor()
        self.opener.add_handler(cookie_handler)
        # 添加 User-Agent
        self.opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')]

    def download(self, url, retry=3):
        if url is None:
            return None
        for i in range(retry):
            try:
                # 文章 4.1.1 节：创建 Request 对象模拟浏览器
                request = urllib.request.Request(url)
                request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
                request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
                request.add_header('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8')
                request.add_header('Referer', 'https://baike.baidu.com/')

                # 文章 4.1.2 节：检查 HTTP 状态码
                response = self.opener.open(request, timeout=15)
                if response.status == 200:
                    # 文章 4.1.2 节：处理编码问题
                    raw_data = response.read()
                    # 尝试多种编码
                    for encoding in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
                        try:
                            html_content = raw_data.decode(encoding)
                            return html_content
                        except (UnicodeDecodeError, LookupError):
                            continue
                    # 最后尝试自动检测编码
                    import codecs
                    html_content = raw_data.decode('utf-8', errors='replace')
                    return html_content
                else:
                    print(f'  [!] 状态码: {response.status}')
            except urllib.error.HTTPError as e:
                print(f'  [!] HTTP 错误 (第{i+1}次): {e.code}')
                if e.code == 403:
                    print(f'  [!] 被反爬拦截，延时重试...')
                    time.sleep(random.uniform(5, 10))
                else:
                    time.sleep(random.uniform(1, 3))
            except urllib.error.URLError as e:
                print(f'  [!] 请求错误 (第{i+1}次): {e.reason}')
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f'  [!] 下载失败 (第{i+1}次): {e}')
                time.sleep(random.uniform(1, 3))
        return None

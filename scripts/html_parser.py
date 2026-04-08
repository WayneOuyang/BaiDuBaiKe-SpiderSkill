from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'/item/'))
        for link in links:
            new_url = link.get('href', '')
            if not new_url or new_url == '/item/' or new_url.startswith('/item/#'):
                continue
            new_full_url = urljoin(page_url, new_url)
            # 只保留百度百科的词条链接
            if re.match(r'https?://baike\.baidu\.com/item/', new_full_url):
                new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {'url': page_url}

        # 提取标题
        title_node = None
        # 新版百度百科
        title_node = soup.find('h1')
        if title_node is None:
            title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title')
        if title_node:
            res_data['title'] = title_node.get_text().strip()
        else:
            res_data['title'] = ''

        # 提取摘要
        summary_node = soup.find('div', class_='lemma-summary')
        if summary_node is None:
            summary_node = soup.find('div', class_='J-lemma-summary')
        if summary_node is None:
            # 尝试从 meta description 获取
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                res_data['summary'] = meta_desc.get('content', '').strip()
            else:
                res_data['summary'] = ''
        else:
            res_data['summary'] = summary_node.get_text().strip()

        # 提取正文内容
        content_parts = []
        para_nodes = soup.find_all('div', class_='para')
        if not para_nodes:
            para_nodes = soup.find_all('div', class_='J-lemma-content')
        for para in para_nodes:
            text = para.get_text().strip()
            if text:
                content_parts.append(text)
        res_data['content'] = '\n'.join(content_parts)

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return None, None
        # 尝试 lxml 解析器，失败则用 html.parser
        for parser in ['lxml', 'html.parser']:
            try:
                soup = BeautifulSoup(html_cont, parser)
                new_urls = self._get_new_urls(page_url, soup)
                new_data = self._get_new_data(page_url, soup)
                return new_urls, new_data
            except Exception:
                continue
        return None, None

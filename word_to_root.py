import requests
import random
from lxml import etree
from lib.constants import user_agent_list


class WordToRoot(object):
    """
    Get word from a word.
    It's use youdao, baidu and jinshan service.
    """

    def __init__(self, word, max_retry=10):
        super(WordToRoot, self).__init__()
        self.word = word
        self.max_retry = max_retry

    def run(self):
        for _ in range(self.max_retry):
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,pt;q=0.6',
                'Connection': 'keep-alive',
                'Host': 'dict.youdao.com',
                'User-Agent': random.choice(user_agent_list)}
            try:
                resp = requests.get(url=f'http://dict.youdao.com/w/{self.word}/',
                                    headers=headers,
                                    allow_redirects=True,
                                    timeout=10)
                if resp.ok:
                    if '您要找的是不是' in resp.text:
                        return None
                    selector = etree.HTML(resp.text)
                    root = selector.xpath(
                        '//div[@id="relWordTab"]/p[1]/span/a[@class="search-js"]/text()')
                    return root[0]
            except Exception as e:
                pass
                # print('*'*20)
                # print(e)
                # print('*'*20)


if __name__ == '__main__':
    wt = WordToRoot('person')
    r = wt.run()
    print(r)

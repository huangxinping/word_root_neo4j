import requests
import random
from lxml import etree
from lib.constants import user_agent_list


class WordToPhrase(object):
    """
    Get some phrase by a word.
    It's use youdao, baidu and jinshan service.
    """

    def __init__(self, word, max_retry=10):
        super(WordToPhrase, self).__init__()
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
                    # the first part.
                    first_part = self.first_part(selector)
                    # the second part.
                    second_part = self.second_part(selector)
                    # the third part.
                    third_part = self.third_part(selector)

                    first_part.update(second_part)
                    first_part.update(third_part)
                    return first_part
            except Exception as e:
                print(e)

    def first_part(self, selector):
        explains = selector.xpath('//div[@class="dict-inter"]/div[@id="wordGroup2"]/p[@class="wordGroup"]/text()')
        explains = list(map(lambda x: x.strip().replace('\n', '').replace(' ', ''), explains))
        explains = list(filter(lambda x: len(x) > 1, explains))
        phrases = selector.xpath(
            '//div[@class="dict-inter"]/div[@id="wordGroup2"]/p[@class="wordGroup"]/span[@class="contentTitle"]/a[@class="search-js"]/text()')
        phrases = list(map(lambda x: x.strip().replace('\n', ''), phrases))
        phrases = list(filter(lambda x: len(x) > 1, phrases))
        return {phrase: explain for phrase, explain in zip(phrases, explains)}

    def second_part(self, selector):
        explains = selector.xpath('//div[@id="tWebTrans"]/div[@id="webPhrase"]/p/text()')
        explains = list(map(lambda x: x.strip().replace('\n', '').replace(' ', ''), explains))
        explains = list(filter(lambda x: len(x) > 1, explains))
        phrases = selector.xpath('//div[@id="tWebTrans"]/div[@id="webPhrase"]/p/span/a/text()')
        phrases = list(map(lambda x: x.strip().replace('\n', ''), phrases))
        phrases = list(filter(lambda x: len(x) > 1, phrases))
        return {phrase: explain for phrase, explain in zip(phrases, explains)}

    def third_part(self, selector):
        explains = selector.xpath('//div[@id="transformToggle"]/div[@class="trans-container tab-content hide more-collapse"]/p/text()')
        explains = list(map(lambda x: x.strip().replace('\n', '').replace(' ', ''), explains))
        explains = list(filter(lambda x: len(x) > 1, explains))
        phrases = selector.xpath('//div[@id="transformToggle"]/div[@class="trans-container tab-content hide more-collapse"]/p/span/a/text()')
        phrases = list(map(lambda x: x.strip().replace('\n', ''), phrases))
        phrases = list(filter(lambda x: len(x) > 1, phrases))
        return {phrase: explain for phrase, explain in zip(phrases, explains)}


if __name__ == '__main__':
    wt = WordToPhrase('correct')
    r = wt.run()
    print(r)

import requests
import random
from lxml import etree
from lib.constants import user_agent_list, pos


class WordTranslate(object):
    """
    Translate helper, it's use youdao service.
    """

    def __init__(self, word, max_retry=10):
        super(WordTranslate, self).__init__()
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
                    # 音标
                    phonetics = selector.xpath('//span[@class="phonetic"]/text()')
                    phonetics = self.phonetic(phonetics)
                    # 词意
                    explains = selector.xpath('//div[@class="trans-container"]/ul/li/text()')
                    explains = self.explain(explains)
                    return {
                        'phonetics': phonetics,
                        'explains': explains
                    }
            except Exception as e:
                print(e)

    # extract phonetic
    def phonetic(self, phonetics):
        if len(phonetics) >= 2:
            uk = phonetics[0].replace("[", '/').replace("]", '/')
            us = phonetics[1].replace("[", '/').replace("]", '/')
            return {'uk': uk, 'us': us}
        return {'uk': '', 'us': ''}

    # extract explain in Chinese.
    def explain(self, explains):
        result = []
        for explain in explains:
            for part in pos.keys():
                if part in explain:
                    result.append(explain.strip())
                    break
        return result


if __name__ == '__main__':
    wt = WordTranslate('there')
    print(wt.run())

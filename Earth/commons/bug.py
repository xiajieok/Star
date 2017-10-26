import requests, os, sys, re, json
from bs4 import BeautifulSoup as bs

url = 'https://linux.cn/news/'
header = 'user-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

# r = requests.get(url,header)
# print(r.encoding)
# print(r.cookies)

ss = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", 'html'))


def getWebPage(url, fname):
    try:
        obj = requests.get(url)
        html = obj.text
        desc = os.path.join(ss, fname)
        print(desc)
        f = open(desc, 'w')
        f.write(html)
        f.close()

    except IOError:
        print('NO !!!!')


def bs4():
    soup = bs(open('new.txt'), 'lxml')
    # 获取文章URL
    b = soup.select('div.caption > a ')
    for i in b:
        url = i.get('href')
        name = url[25:]
        # print(name)
        # getWebPage(url,name)
        obj = requests.get(url).text
        soup = bs(obj, 'lxml')

        # 处理title
        title = soup.select('#article_title ')
        title = str(title)
        pattern = re.compile('<h1 class="ph" id="article_title">(.*?)</h1>', re.S)
        title = re.search(pattern, title).group(1).strip()
        print(title)

        # 处理summary
        summary = soup.find_all('div', id='article_summary')
        summary = str(summary)
        pattern = re.compile('<div id="article_summary" style="display: none;">(.*?)</div>', re.S)
        summary = re.search(pattern, summary).group(1).strip()
        # print(summary)

        # 文章内容
        article = soup.select('#article_content')
        article = str(article)[1:-1]
        print(type(article))

        # 转载信息
        copyright = soup.select('div#footer_info > p.copyright')
        copyright = str(copyright)[1:-1]
        print(copyright)

        data = {'title': title, 'brief': summary, 'article': article, 'copyright': copyright, 'reprinted': str(url)}

        r = requests.post('http://127.0.0.1:8000/robot/', data=data)


if __name__ == '__main__':
    # getWebPage(url,header)
    bs4()

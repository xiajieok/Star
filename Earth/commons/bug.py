import requests, os, sys, re, json, random
from bs4 import BeautifulSoup as bs

linuxcn = 'https://linux.cn/news/index.php?page=1'
ithome = 'https://www.ithome.com/'

hh = [
    'user-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'user-agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'user-agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'user-agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'user-agent:Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
    'user-agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER',
    'user-agent:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
    'user-agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
    'user-agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'user-agent:Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
]
headers = random.sample(hh, 1)[0]

# r = requests.get(url,header)
# print(r.encoding)
# print(r.cookies)

ss = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", 'html'))


def getWebPage(url, fname):
    try:
        obj = requests.get(url)
        obj.headers = headers
        # coding = obj.apparent_encoding
        # print(coding)
        obj.encoding = 'utf-8'

        html = obj.text

        desc = os.path.join(ss, fname)
        # print(desc)
        f = open(desc, 'w', encoding='utf-8')
        f.write(html)
        f.close()

    except IOError:
        print('NO !!!!')


def getIthome(ithome):
    getWebPage(ithome, 'ithome.html')
    soup = bs(open('./html/ithome.html', 'rb'), 'lxml')
    b = soup.select('div.new-list-1 li.new a  ')
    for i in b:
        url = i.get('href')
        # print(url)
        url = str(url)
        if 'digi' in url or 'live' in url:
            print('跳出!!!')
            continue
        else:
            obj = requests.get(url)
            obj.encoding = 'utf-8'
            soup = bs(obj.text, 'lxml')
            # 处理title
            title = soup.select('h1')
            title = str(title)
            pattern = re.compile('<h1>(.*?)</h1>', re.S)
            title = re.search(pattern, title).group(1).strip()
            print(title)
            # 处理发布时间
            date = soup.select('#pubtime_baidu')
            date = str(date)
            pattern = re.compile('<span id="pubtime_baidu">(.*?)</span>', re.S)
            date = re.search(pattern, date).group(1).strip()[0:18]
            print(date)
            # 文章内容
            article = soup.select('div.post_content')
            article = str(article)[1:-1]
            article = article.replace('data-original', 'src')
            # print(article)
            data = {'title': title, 'brief': title, 'article': article, 'copyright': '', 'date': date,
                    "reprinted": url}

            r = requests.post('http://127.0.0.1:8000/robot/', data=data)
            print('ok')


def getLinuxcn(linuxcn):
    getWebPage(linuxcn, 'linuxcn.html')
    soup = bs(open('./html/linuxcn.html',encoding='utf-8'), 'lxml')
    # 获取文章URL
    b = soup.select('span.title > a')
    for i in b:
        # url = i
        url = i.get('href')
        url = str(url)
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

        # 处理发布时间
        date = soup.select('p.xg1')
        date = str(date)
        pattern = re.compile('<p class="xg1">(.*?)</p>', re.S)
        date = re.search(pattern, date).group(1).strip()[0:16]
        print(date)

        # 处理summary
        summary = soup.find_all('div', id='article_summary')
        summary = str(summary)
        pattern = re.compile('<div id="article_summary" style="display: none;">(.*?)</div>', re.S)
        summary = re.search(pattern, summary).group(1).strip()
        # print(summary)

        # 文章内容
        article = soup.select('#article_content')
        article = str(article)[1:-1]
        # print(type(article))

        # 转载信息
        copyright = soup.select('div#footer_info > p.copyright')
        copyright = str(copyright)[1:-1]
        # print(copyright)

        data = {'title': title, 'brief': summary, 'article': article, 'copyright': copyright, 'date': date,
                "reprinted": url}

        r = requests.post('http://127.0.0.1:8000/robot/', data=data)


if __name__ == '__main__':
    getLinuxcn(linuxcn)
    getIthome(ithome)

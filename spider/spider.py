import requests
from bs4 import BeautifulSoup
import pandas

new1 = []
for i in range(1, 26):
    res = requests.get('https://www.qidian.com/rank/click?style=1&dateType=3&page='+str(i))
# print(res.status_code)
    soup = BeautifulSoup(res.text, 'html.parser')

# print(soup)

    for news in soup.select('.rank-view-list li'):
    # print(news)
    # print(news.select('p')[1].text)     #出不来简介  ？
    # print(news.select('p')[1].text)
    # print(news.select('a')[1].text)    #书名
    # print(news.select('a')[2].text)    #作者
    # print(news.select('a')[3].text)    #分类
    # print(news.select('span')[1].text) #完本or连载
    #print(news.select('p')[1].text)    #理论上应该是简介
    # print(news.select('p')[2].text)    #最新章节
    # print(news.select('a')[0]['href']) #网址
        cc = news.select('a')[0]['href']
        test = requests.get('http://' + cc[2:])
        soup1 = BeautifulSoup(test.text, 'html.parser')
        news1 = soup1.select('.book-intro')
        print(news.select('a')[1].text, news.select('a')[2].text, news.select('a')[3].text, news1[0].text.strip(),
          news.select('span')[1].text, news.select('p')[2].text, news.select('a')[0]['href'])
    '''
    new1.append({'书名': news.select('a')[1].text, '作者': news.select('a')[2].text, '类型': news.select('a')[3].text,
                    '连载状态': news.select('span')[1].text, '简介': news.select('p')[1].text,
                    '最新内容': news.select('p')[2].text, '链接': news.select('a')[0]['href']})
    new2 = pandas.DataFrame(new1)
new2.to_excel('qidian_rank1.xlsx ')
'''

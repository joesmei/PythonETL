import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
import time

# if not os.path.exists('ptt_Car'):
#     os.mkdir('ptt_Car')

client = MongoClient('localhost', 27017)
db = client['ptt_car']
collect = db['pttCar']

useragent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
headers = {'User-Agent':useragent}

ss = requests.session()
notation = ['\\','/',':','*','?','"',"'",'<','>','|']
j = 1

for page in range(4390,5003):
    url = 'https://www.ptt.cc/bbs/car/index{}.html'.format(page)
    res = ss.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    title_list = soup.select('div[class="title"] a')
    # print(title_list)
    for title_soup in title_list:
        try:
            # print(title_soup)
            title = title_soup.text
            # print(title)
            real_title_url = 'https://www.ptt.cc/'+title_soup['href']
            # print(real_title_url)

            for i in notation:  # 換掉所有非法字元
                title = title.replace(i, '_')

            res_article = ss.get(real_title_url, headers = headers)
            soup_article = BeautifulSoup(res_article.text, 'html.parser')
            # print(soup_article)
            article_title = soup_article.select('.article-meta-value')[2].text

            # print(article_title)
            article_content_list = soup_article.select('div[id="main-content"]')[0].text.split('--')[0]
            # print(article_content_list)
            article_content_list = article_content_list.replace('\n','')
            comment_list = soup_article.select('span[class="f3 push-content"]')


            article_comment_list =[c.text.split(':')[1] for c in comment_list]
            if len(article_comment_list) ==0 :
                    article_comment_list.append('none')
            # print(article_comment_list)
            # print(article_comment_list)
            article_time = soup_article.select('.article-meta-value')[3].text
            # print(article_time)
            L = [['title',article_title],['text',article_content_list],['comment',article_comment_list],['time',article_time]]
            c = dict(L)
            # print(c)
            # data = {}
            # k = ['text','comment']
            # v = [article_content_list,article_comment_list]
            # data = {k[i]:v[i] for i in range(len(k))}
            # print(data)
            print('新增'+str(j)+'篇文章')
            j += 1
            # with open('./ptt_Car/%s.txt' % (title), 'w', encoding='utf-8') as f:
            #     f.write(str(c))

            c_id = collect.insert_one(c)
            print(c_id)
            # time.sleep(2)

        except IndexError as e:
            print('=====')
            print(title)
            print('=====')



    # last_page_url = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']
    # print(last_page_url)
    # url = last_page_url


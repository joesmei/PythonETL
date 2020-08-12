import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
ss = requests.session()

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
word = input('請輸入欲查詢關鍵字:')
data = []
k = 1

for page in range(1,5):
    url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}&order=12&asc=0&page={}&mode=s&jobsource=2018indexpoc'.format(word,page)

    res = ss.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")
    # print(soup.prettify())

    mytitle = soup.select('h2[class="b-tit"] a')
    # print(mytitle)
    # n=0
    for a in mytitle:
        # print("==============================================")
        Title = a.text
        article_url = "https://www.104.com.tw/job/ajax/content/"+a["href"].split("//")[1].split("?")[0].split("/")[2]
        # print(Title)
        # print(article_url)

        # get content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
            , 'Referer': article_url}
        a_res = requests.get(article_url, headers=headers)
        # print(a_res.text)
        js = json.loads(a_res.text)
        # print(js) #轉成python中的dic

        job_name = js["data"]["header"]["jobName"] #從字典取職稱
        # print(job_name)
        cust_name = js['data']['header']['custName'] #從字典取公司名稱
        # print(cust_name)
        edu = js['data']["condition"]["edu"] #從字典取學歷要求
        # print(edu)
        workExp = js['data']["condition"]["workExp"] #從字典取工作經驗
        # print(workExp)

        # 技能為多值
        def ski():
            skill = js['data']["condition"]["skill"]

            for d in skill:
                yield d['description']

        skill = "、".join(list(ski())) #list轉string
        sk=list(skill)
        if len(sk) == 0:
            sk.append('不拘')  #轉list才能append
        skill = ''.join(sk) #最後轉string

        # print(skill)

        # 擅長工具為多值
        def spe():
            specialty = js['data']['condition']['specialty']
            n = 0
            for s in specialty:
                n += 1
                yield str(n) + '.' + s['description'] # 給編號
        specialty = ",".join(list(spe())).replace(",", "  ")
        sp=list(specialty)
        if len(sp) == 0:
            sp.append('不拘')
        specialty=''.join(sp)

        l = []
        l.append(job_name)
        l.append(cust_name)
        l.append(edu)
        l.append(workExp)
        l.append(skill)
        l.append(specialty)
        # print(l)

        data.append(l)
        print('新增' + str(k) + '筆資料')
        k += 1

df = pd.DataFrame(data=data,columns = ['職稱','公司名稱','學歷要求','工作經歷','工作技能','擅長工具'])
df.to_csv('./homework.csv',index = 0,encoding = 'utf-8-sig')

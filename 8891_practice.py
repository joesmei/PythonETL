import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('8891_brand'):
    os.mkdir('8891_brand')

ss = requests.session()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
url = 'https://c.8891.com.tw/Models'

res = ss.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup)

group_list = soup.select('ul[class="group-list"] a')
# print(group_list)
for group in group_list:
    # print(group)
    brand = group['href'].split('/')[-1]
    print(brand)

    with open('./8891_brand/car.text', 'a', encoding='utf-8') as f:
        f.write(brand + '\n')
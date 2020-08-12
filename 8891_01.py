from bs4 import BeautifulSoup
import requests
import json
import os

if not os.path.exists('8891_image'):
    os.mkdir('8891_image')

ss = requests.session()
with open('./8891_brand/car.text', 'r', encoding='utf-8') as f:
    car_kind = f.read()
    # print(car_kind)
car_kind_list = car_kind.split('\n')[:-1]
# print(car_kind_list)
count = 0
for car in car_kind_list:
    # print(car)
    keyword = car
    url = 'https://c.8891.com.tw/Models/{}?&page=1'.format(keyword)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    res = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)

    # car_soup = soup.select('ul[class="clearfix"]')[0].select('a')
    # car_list = [car['href'] for car in car_soup]
    # print(car_list)
    # # car_l = []
    # # for i in range(len(car_list)):  # 偶數標籤才是實際要進入的車款url
    # #     if i % 2 == 0:
    # #         car_l.append(car_list[i])
    # # print(car_l)

    car_soup = soup.select('ul[class="clearfix"] a')
    car_list = []
    for i, car_url_list in enumerate(car_soup):
        if i % 2 == 0:
            car_url = car_url_list['href']
            car_list.append(car_url)
    # print(car_list)  #取得每台車的url

    for c in car_list:
        # print(c)
        k = '_'.join(c.split('/')[3:5]) #取車種跟車款EX: honda_crv
        # print(k)
        res_c = ss.get(c, headers=headers)
        soup_c = BeautifulSoup(res_c.text, 'html.parser')
        car_back_list=[]
        # print(soup_c)
        url_outside = soup_c.select('a[alt="外觀"]')
        # print(url_outside)
        if len(url_outside)==0:
            continue
        # print(url_outside) #找到外觀的url
        for u in url_outside:
            true_url = u['href']
            # print(true_url)
            pid = true_url.split('=')[1]
            pic_list = ['%2C' + str(i) for i in range(int(pid) - 15, int(pid) + 15)]
            s = ""
            pic_str = s.join(pic_list)
            car_pic_url = 'https://c.8891.com.tw/photoLibrary-ajaxList.html?pid={}{}'.format(pid, pic_str)
            res_car_outside = requests.get(car_pic_url, headers=headers)
            json_car = json.loads(res_car_outside.text)
            # print(json_car) #是一個dictionary
            for i in json_car['data']: #只有data跟status兩個key
                if i['tid'] == 6:
                    car_back_list.append(i)
            car_back_url = [c['thumbnail'] for c in car_back_list]
            print(car_back_url)

            for img_url in car_back_url:
                res_img = ss.get(img_url, headers=headers)
                img_content = res_img.content
                img_name = './8891_img/' + k
                with open(img_name + '_' + '.png', 'wb') as f:
                    f.write(img_content)
                    count += 1
print(count)






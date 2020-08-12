from pymongo import MongoClient
import re

# 從eight_brands讀取八大款式名字
brands = ['FIT','Fit','fit']
# with open('./eight_brands.csv', 'r', encoding='utf-8') as f:
#     brand = f.read()
#     brands = brands.append(brand)
print(type(brands))
# for brand in brands:
#     print(brand)


# 建立 mongoDB localhost server 特定db之特定collection的連線
client = MongoClient('localhost', 27017)
db = client['ptt_car']
crawler_coll = db['clean_pttcar']
clean_coll = db['clean_Fit']

k = 1
for doc in crawler_coll.find({}, {"_id": 0, "title": 1, "text": 1, "comment":1, "time": 1}): #把mongodb裡的資料讀進來，不含id
    doc['language'] = 'zh-Hant'  # 增加一個欄位，指定語言為繁體中文
    # regex = re.compile(r'（([\u4E00-\u9FA5])*）')
    # print(regex.search(tmp_str))
    # 以下先用python的函數先做一番清洗，split()用作文章分段，切開來後取前半([0])或後半([1])
    # replace() 用來替換一些無用的字
    tmp_str = doc['text']
    # 再用正則表示式挑出（）包住的中文及一些數字符號，例如（示意照，記者劉濱銓翻攝）等等
    reg_str = re.sub(r'（([\u4E00-\u9FA5，：0-9])*）', '', tmp_str)
    doc['text'] = reg_str  # 把'text'改為清洗完成的文字
    brands_shown = []
    # 檢查品牌是否出現在新聞之中
    for brand in brands:                # 60幾個廠牌全部查一遍
        if brand in reg_str:
            brands_shown.append(brand)
            doc['brand'] = brands_shown
    if 'brand' in doc: #若資料裡面有brand欄位(新聞裡抓到有汽車廠牌的內容再放到clean_collection裡面)
        clean_coll.insert_one(doc)
        print('新增'+str(k)+'筆資料')
        k += 1
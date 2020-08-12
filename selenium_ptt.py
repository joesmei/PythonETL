from selenium.webdriver import Chrome

driver = Chrome('./chromedriver')

url = 'https://www.ptt.cc/bbs/index.html'

driver.get(url) #對網址提出請求，便會自動開啟瀏覽器到所指定的網址裡

driver.find_element_by_class_name('board-name').click()
driver.find_element_by_class_name('btn-big').click()

cookie = driver.get_cookies()
for c in cookie:
    print(c) #每一個cookie都是字典


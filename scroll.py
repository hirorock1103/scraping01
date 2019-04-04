from selenium import webdriver # さっきpip install seleniumで入れたseleniumのwebdriverというやつを使う
import time
import datetime
import sqlite3

# connect database
con = sqlite3.connect('sample.db')
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS SampleGetPostList(id integer primary key AUTOINCREMENT, url text, word text)")


driver = webdriver.Chrome(r"C:\Users\user\Desktop\chromedriver/chromedriver.exe")   # さっきDLしたchromedriver.exeを使う
fPath = r"C:\Users\user\Desktop\data"
# https://teratail.com/questions/131027 permission problem
targetWord = "アメリカ"

TOP_URL = "https://www.instagram.com/explore/tags/" + targetWord + "/"

driver.set_page_load_timeout(600)   # ページロード最大600秒
driver.get(TOP_URL)    # chrome起動→ログインページに移動
time.sleep(5)

# infinite scroll
lastUrl = ""
# last urlが変わり続ける限り取得する
getCount = 0
for i in range(0, 5000):

    print("count:" + str(i))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)   # 電波状況悪いと長時間waiting必要
    # tmp = driver.find_elements_by_xpath("//a[@href]")
    tmp = driver.find_elements_by_xpath("//a[contains(@href,'%s')]" % "/p/")
    # thanks https://teratail.com/questions/154740

    if lastUrl != tmp[tmp.__len__()-1].get_attribute("href"):

        # 最後のURLが「最後から」何番目にあるかチェックする
        start = tmp.__len__()-1
        targetNumber = 0
        if i == 0:  # roop 1回目は取得されたURL全てが対象となる
            targetNumber = tmp.__len__()-1
        print("start: last url = " + lastUrl)
        print("# 最後のURLが「最後から」何番目にあるかチェックする")
        print("first tmp value : " + tmp[0].get_attribute("href"))
        for j in range(tmp.__len__()):
            print("■" + str(start-j) + "/" + tmp[start-j].get_attribute("href"))
            if lastUrl == tmp[start-j].get_attribute("href"):
                print("★" + str(j) + "/" + tmp[start - j].get_attribute("href"))
                targetNumber = j
                print("最後から" + str(targetNumber) + "番目の要素にHit")
                print("確認:" + tmp[targetNumber].get_attribute("href"))
        print("「targetNumber」" + str(targetNumber))
        print("「tmp.__len__() - 1」" + str(tmp.__len__() - 1))

        print("first tmp value : " + tmp[0].get_attribute("href"))
        newList = []
        for n in range(targetNumber + 1):
            getCount += 1
            # print(tmp[targetNumber + n].get_attribute("href"))
            print("array set:" + "(" + str(n) + ")" + tmp[tmp.__len__() - 1 - targetNumber + n].get_attribute("href"))
            newList.append(tmp[tmp.__len__() - 1 - targetNumber + n].get_attribute("href"))
            cursor.execute("INSERT INTO SampleGetPostList (url, word) VALUES(?, ?)", (newList[n], targetWord,))

        con.commit()
        path = fPath + "/new_" + targetWord + "_" + str(datetime.date.today()) + ".txt"
        with open(path, mode='a') as f:
            f.write('\n'.join(newList) + '\n')

        # 最後のurlを保存
        lastUrl = tmp[tmp.__len__() - 1].get_attribute("href")
        print("last url update:" + lastUrl)
        print("最後のurlが違ったので処理継続")

    else:
        print("最後のurlが同じだったので処理ストップ")
        break

    # for s in tmp:
    # print(s.get_attribute("href"))

    print("getCount:" + str(getCount))


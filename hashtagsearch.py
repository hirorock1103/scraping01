from selenium import webdriver    # さっきpip install seleniumで入れたseleniumのwebdriverというやつを使う
import time
import sqlite3
from datetime import datetime, date, timedelta

# 投稿LISTに対してuser名とハッシュタグをセットしていく
mode = ""

# connect database
con = sqlite3.connect('sample.db')
cursor = con.cursor()
query = "CREATE TABLE IF NOT EXISTS SampleGetPostList(" \
        "id integer primary key AUTOINCREMENT, " \
        "url text, " \
        "word text, " \
        "post_date text, " \
        "h_tags text, " \
        "post_user_id text, " \
        "converted_post_date text, " \
        "createdate text)"
cursor.execute(query)

TOP_URL = "https://www.instagram.com"
fPath = r"C:\Users\user\Desktop\data"

# targetList = list()
# # get data from file or database
# f = open(fPath + '/new_スタイル抜群_2019-04-05.txt', 'r')
# line = f.readline()
# while line:
#     line = f.readline()
#     # targetList.append(line)
# f.close()

driver = webdriver.Chrome(r"C:\Users\user\Desktop\chromedriver/chromedriver.exe")   # さっきDLしたchromedriver.exeを使う
driver.set_page_load_timeout(600)   # ページロード最大600秒
# driver.get(TOP_URL)    # chrome起動→ログインページに移動
# time.sleep(2)


def convert_str_to_date(str_date):
    print(str_date)
    today = datetime.today()
    ansDate = ""
    # 時間前 / 分前　→　todayとして登録
    if str_date.find("時間前") >= 0 or str_date.find("分前") >= 0:
        print("「時間前、分前」が含まれる")
        targetDate = today
        ansDate = datetime.strftime(targetDate, '%Y-%m-%d')

    # 日前　→　指定日で計算
    elif str_date.find("日前") >= 0:
        count = int(str_date[0:1])
        print("「日前」が含まれる")
        targetDate = today - timedelta(days=count)
        ansDate = datetime.strftime(targetDate, '%Y-%m-%d')

    # 〇年〇月〇日　→　指定年月日
    elif str_date.find("年") >= 0 and str_date.find("月") >= 0 and str_date.find("日") >= 0:
        print("指定年月日" + str_date)
        date_string = str_date
        print("date_string" + date_string)
        targetDate = datetime.strptime(date_string, '%Y年%m月%d日')
        ansDate = datetime.strftime(targetDate, '%Y-%m-%d')

    # 〇月〇日　→ 今年の指定年月日
    elif str_date.find("月") >= 0 and str_date.find("日") >= 0:
        print("今年の指定年月日" + str_date)
        date_string = str(today.year) + "年" + str_date
        print("date_string" + date_string)
        targetDate = datetime.strptime(date_string, '%Y年%m月%d日')
        ansDate = datetime.strftime(targetDate, '%Y-%m-%d')

    return ansDate


# start from database
cursor.execute('SELECT * FROM SampleGetPostList ORDER BY id ASC')

for row in cursor:

    dataId = (row[0])
    url = (row[1])
    title = (row[2])
    dataUserId = (row[5])

    print(dataUserId)
    if dataUserId is not None:
        print("userId is already set")
        continue

    print("\n\n -search start- " + url)
    driver.get(url)

    try:
        errormsg = driver.find_element_by_xpath("/html/body/div/div[1]/div/div/h2")
        print(errormsg.text)
        if errormsg.text == "このページはご利用いただけません。":
            print("ページが存在しないためcontinue")
            time.sleep(1)
            continue
    except:
        print("通常")

    time.sleep(2)
    if mode != "VIEW":

        # User を取得
        userTag = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/h2/a')
        # ハッシュタグを取得
        hashTags = []
        elmDiv = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]')
        elmSpan = elmDiv.find_elements_by_tag_name("span")
        aTags = elmDiv.find_elements_by_tag_name("a")
        timeTags = elmDiv.find_element_by_tag_name("time")
        convertedDate = convert_str_to_date(timeTags.text)
        print("convertedDate:" + convertedDate)

        for link in aTags:
            if "#" in link.text:
                hashTags.append(link.text)

        if hashTags.__len__() > 0:
            # update record
            tags = ",".join(hashTags)
            dataId = dataId
            user = userTag.text
            print("tags:" + tags)
            print("dataId:" + str(dataId))
            print("user:" + user)
            cursor2 = con.cursor()
            query = "update SampleGetPostList SET h_tags = ?, post_user_id = ?, post_date = ?, converted_post_date = ? WHERE id = ?"
            args = (tags, userTag.text, timeTags.text, convertedDate, dataId)
            cursor2.execute(query, args)
            con.commit()


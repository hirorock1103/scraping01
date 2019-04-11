from selenium import webdriver # さっきpip install seleniumで入れたseleniumのwebdriverというやつを使う
import time
import random
import sqlite3


# function log
def log(comment):
    print(comment)
    cursor.execute("INSERT INTO Log (log_title, comment, createdate) VALUES(?, ?, datetime())", (logTitle, comment,))
    con.commit()


# connect database
con = sqlite3.connect('sample.db')
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS SampleGetUserList(id integer primary key AUTOINCREMENT, url text, user text, createdate text)")
cursor.execute("CREATE TABLE IF NOT EXISTS Log(id integer primary key AUTOINCREMENT, log_title text, comment text, createdate text)")

# Url and Path Setting
driver = webdriver.Chrome(r"C:\Users\user\Desktop\chromedriver/chromedriver.exe")   # さっきDLしたchromedriver.exeを使う
TOP_URL = "https://www.instagram.com/accounts/login/?hl=ja&source=auth_switcher"
fPath = r"C:\Users\user\Desktop\data"

# Basic Setting
randIntFrom = 2     # sleep時の時間設定
randIntTo = 4   # sleep時の時間設定
targetUsersFollowersMax = 200     # ユーザーのフォロワー

# getFollower
targetUser = "_m.shun_"      # user id
targetUser = "koji7821"      # user id

# other
logTitle = "getUserList"

# START
driver.set_page_load_timeout(600) # ページロード最大600秒
driver.get(TOP_URL) # chrome起動→ログインページに移動
time.sleep(random.randint(randIntFrom, randIntTo))

# LOGIN
id = driver.find_element_by_name("username")
id.send_keys("mdiz1103@gmail.com")

passwordId = driver.find_element_by_name("password")
passwordId.send_keys("11032189")

time.sleep(random.randint(randIntFrom, randIntTo))

# ログインボタンをクリック
login_button = driver.find_elements_by_tag_name("button")
login_button[1].click()

# 少し待機
time.sleep(random.randint(randIntFrom, randIntTo))

# move to top
driver.get("https://www.instagram.com/?hl=ja")

# if pop up appear
buttons = driver.find_elements_by_tag_name("button")
bt = 0
for i in range(buttons.__len__()):
    if buttons[i].text == "後で":
        bt = i

time.sleep(random.randint(randIntFrom, randIntTo))

if bt > 0:
    buttons[bt].click()

time.sleep(random.randint(randIntFrom, randIntTo))

# move to Users Page
driver.get("https://www.instagram.com/" + targetUser + "/")

commnt = "start get Followers list, targetUser:" + targetUser
log(commnt)

# Users Followers PopUp
word = targetUser + "/followers"
link = driver.find_element_by_xpath("//a[contains(@href,'%s')]" % word)
time.sleep(random.randint(randIntFrom, randIntTo))
link.click()

time.sleep(random.randint(randIntFrom, randIntTo))

# followerNumber
commnt = "follower:" + link.text
log(commnt)

# Manage slide inner pop up
presentation = driver.find_element_by_xpath("/html/body/div[3]")
followerArea = presentation.find_element_by_xpath("/html/body/div[3]/div/div[2]/ul")
followerButtons = followerArea.find_elements_by_tag_name("li")

# direct path to follower number
span = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
resultFollowerCount = 0
spanFollowerCount = str(span.text)

commnt = "文字列「千」が存在するか no : -1  " + str(spanFollowerCount.find("千"))
log(commnt)

if spanFollowerCount.find("千") != -1:
    tmp = spanFollowerCount.replace("千", "")
    tmp = tmp.replace(",", "")
    tmp = tmp.replace(".", "")
    resultFollowerCount = int(tmp) * 1000
else:
    spanFollowerCount = spanFollowerCount.replace(",", "")
    resultFollowerCount = int(spanFollowerCount)

commnt = "convert followers to int : " + str(resultFollowerCount)
log(commnt)

# calc distance by number of followers
RpCount = int(resultFollowerCount / 2)
commnt = "roopCount:" + str(RpCount)
log(commnt)
insertCount = 0
moveDistance = 150
if followerButtons.__len__() > 11:

    sameCount = 0   # 取得件数が同じだった回数
    judgeCount = 0  # 全取得されたと判断するカウント
    previousBtCount = 0   # スクロール後のButton数カウント
    previousList1stVal = ""
    previousListLastVal = ""

    for i in range(RpCount):

        if insertCount >= targetUsersFollowersMax:
            commnt = "-- break because db insert count is over limit"
            log(commnt)
            break

        moveDistance += 125
        time.sleep(0.7)
        script = "document.querySelector('div[role=\"dialog\"]>div[class=\"isgrP\"]').scrollTop=" + str(moveDistance)
        driver.execute_script(script)
        # load image
        followerArea = presentation.find_element_by_xpath("/html/body/div[3]/div/div[2]/ul")
        followerButtons = followerArea.find_elements_by_tag_name("li")

        count = followerButtons.__len__()

        if previousBtCount == count:

            sameCount += 1
            # print(count)
            # print(str(sameCount) + "回同じ要素数")
            # previousBtCount = count

        else:
            sameCount = 0
            # print("要素がloadされた")
            # print("previous count:" + str(previousBtCount))
            # print("li in ul count:" + str(count))
            try:
                # print("last item:" + followerButtons[count-1].find_element_by_tag_name("a").get_attribute("href"))
                # if not error , calc count between current count and previous count
                positionFromLastElement = count - previousBtCount
                commnt = "positionFromLastElement:" + str(positionFromLastElement)
                log(commnt)

                if i > 0 & positionFromLastElement > 12:
                    commnt = "-- roop skip because positionFromLastElement is over 12"
                    log(commnt)
                    continue

                if positionFromLastElement > 0:

                    log("roop count - " + str(i) + "回目")
                    log("data count - " + str(positionFromLastElement) + "個のデータ")

                    dbInsert = 0
                    for j in range(positionFromLastElement):

                        if insertCount >= targetUsersFollowersMax:
                            commnt = "-- skip because db insert count is over limit!"
                            log(commnt)
                            continue

                        pos = count - positionFromLastElement + j
                        url = followerButtons[pos].find_element_by_tag_name("a").get_attribute("href")

                        # set for previous value
                        if j == 0:
                            if previousList1stVal == url:
                                commnt = "-- this first value equals pre first value, roop break"
                                log(commnt)
                                break
                            previousList1stVal = url
                        previousListLastVal = url

                        # print("(" + str(pos) + ")" + url)
                        cursor.execute("INSERT INTO SampleGetUserList (url, user, createdate) VALUES(?, ?, datetime('now', 'localtime'))", (url, targetUser,))
                        insertCount += 1
                        dbInsert += 1

                    con.commit()
                    if dbInsert > 0:
                        commnt = "-- Database Inserted : " + str(dbInsert) + " --"
                        log(commnt)
                        commnt = "insertCount:" + str(insertCount)
                        log(commnt)

                # set follower count as previous count
                previousBtCount = count

            except sqlite3.Error as e:
                commnt = "sqlite3 error occurred:", e.args[0]
                log(commnt)
            except:
                commnt = "Error failed to get last element"
                log(commnt)

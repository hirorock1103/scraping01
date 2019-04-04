from selenium import webdriver # さっきpip install seleniumで入れたseleniumのwebdriverというやつを使う
import time
import random
import sqlite3

# connect database
con = sqlite3.connect('sample.db')
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS SampleGetList(id integer primary key AUTOINCREMENT, url text, user text)")

# Url and Path Setting
driver = webdriver.Chrome(r"C:\Users\user\Desktop\chromedriver/chromedriver.exe") # さっきDLしたchromedriver.exeを使う
TOP_URL = "https://www.instagram.com/accounts/login/?hl=ja&source=auth_switcher"
fPath = r"C:\Users\user\Desktop\data"

# Basic Setting
randIntFrom = 2     # sleep時の時間設定
randIntTo = 4   # sleep時の時間設定
targetUsersFollowersMax = 200     # ユーザーのフォロワー

# getFollower
targetUser = "_m.shun_"      # user id
targetUser = "miraamira1440"      # user id

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

# Users Followers PopUp
word = targetUser + "/followers"
link = driver.find_element_by_xpath("//a[contains(@href,'%s')]" % word)
time.sleep(random.randint(randIntFrom, randIntTo))
link.click()

time.sleep(random.randint(randIntFrom, randIntTo))

# followerNumber
print(link.text)

# Manage slide inner pop up
presentation = driver.find_element_by_xpath("/html/body/div[3]")
followerArea = presentation.find_element_by_xpath("/html/body/div[3]/div/div[2]/ul")
followerButtons = followerArea.find_elements_by_tag_name("li")

# direct path to follower number
span = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
resultFollowerCount = 0
spanFollowerCount = str(span.text)
print(spanFollowerCount.find("千"))
if spanFollowerCount.find("千") != -1:
    tmp = spanFollowerCount.replace("千", "")
    tmp = tmp.replace(",", "")
    tmp = tmp.replace(".", "")
    resultFollowerCount = int(tmp) * 1000
else:
    spanFollowerCount = spanFollowerCount.replace(",", "")
    resultFollowerCount = int(spanFollowerCount)

print(resultFollowerCount)

# calc distance by number of followers
RpCount = int(resultFollowerCount / 10)
insertCount = 0
moveDistance = 150
if followerButtons.__len__() > 11:

    sameCount = 0   # 取得件数が同じだった回数
    judgeCount = 0  # 全取得されたと判断するカウント
    btCountLastScroll = 0   # スクロール後のButton数カウント

    for i in range(RpCount):

        if insertCount > targetUsersFollowersMax:
            break

        moveDistance += 100
        time.sleep(0.5)
        script = "document.querySelector('div[role=\"dialog\"]>div[class=\"isgrP\"]').scrollTop=" + str(moveDistance)
        driver.execute_script(script)
        # load image
        followerArea = presentation.find_element_by_xpath("/html/body/div[3]/div/div[2]/ul")
        followerButtons = followerArea.find_elements_by_tag_name("li")

        count = followerButtons.__len__()

        if btCountLastScroll == count:

            sameCount += 1
            # print(count)
            # print(str(sameCount) + "回同じ要素数")
            btCountLastScroll = count

        else:
            sameCount = 0
            # print("要素がloadされた")
            # print("previous count:" + str(btCountLastScroll))
            # print("li in ul count:" + str(count))
            try:
                # print("last item:" + followerButtons[count-1].find_element_by_tag_name("a").get_attribute("href"))
                # if not error , calc count between current count and previous count
                positionFromLastElement = count - btCountLastScroll
                print("positionFromLastElement:" + str(positionFromLastElement))
                if positionFromLastElement > 0:
                    for j in range(positionFromLastElement):
                        pos = count - positionFromLastElement + j
                        url = followerButtons[pos].find_element_by_tag_name("a").get_attribute("href")
                        print("(" + str(pos) + ")" + url)
                        # print("(" + str(pos) + ")" + followerButtons[pos].find_element_by_tag_name("a").text)

                        if insertCount > targetUsersFollowersMax:
                            continue
                        cursor.execute("INSERT INTO SampleGetList (url, user) VALUES(?, ?)", (url, targetUser,))
                        insertCount += 1

                    con.commit()

                # set follower count as previous count
                btCountLastScroll = count
            except sqlite3.Error as e:
                print("sqlite3 error occurred:", e.args[0])
            except:
                print("Error failed to get last element")








from selenium import webdriver # さっきpip install seleniumで入れたseleniumのwebdriverというやつを使う
import time
import random
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(r"C:\Users\user\Desktop\chromedriver/chromedriver.exe")   # さっきDLしたchromedriver.exeを使う

TOP_URL = "https://www.instagram.com/accounts/login/?hl=ja&source=auth_switcher"
fPath = r"C:\Users\user\Desktop\data"

randIntFrom = 3
randIntTo = 5

userIdList = list()
likeUserIdList = list()
unfollowUserIdList = list()
# get data from file or database
f = open(fPath + '/key_word_all_hash_tag_all_2019-04-11.txt', 'r')
line = f.readline()
while line:
    line = f.readline()
    userIdList.append(line)
f.close()

driver.set_page_load_timeout(600) # ページロード最大600秒
driver.get(TOP_URL) # chrome起動→ログインページに移動
time.sleep(random.randint(randIntFrom, randIntTo))

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

driver.get("https://www.instagram.com/?hl=ja")

# pop up
buttons = driver.find_elements_by_tag_name("button")
bt = 0
for i in range(buttons.__len__()):
    if buttons[i].text == "後で":
        bt = i

time.sleep(random.randint(randIntFrom, randIntTo))

if bt > 0:
    buttons[bt].click()

# 少し待機
time.sleep(random.randint(randIntFrom, randIntTo))

# follow

for item in userIdList:
    print(item + "のフォローを開始")
    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))
    # driver.get("https://www.instagram.com/p/"+item+"/")
    driver.get(item)

    buttons.clear()
    buttons = driver.find_elements_by_tag_name("button")
    bt = -1
    for i in range(buttons.__len__()):
        print("bttext:" + buttons[i].text)
        if buttons[i].text == "フォローする":
            bt = i

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))

    if bt > -1:
        buttons[bt].click()

# unfollow
for item in unfollowUserIdList:
    print(item + "のアンフォローを開始")

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))
    # driver.get("https://www.instagram.com/p/" + item + "/")
    driver.get(item)

    buttons.clear()
    buttons = driver.find_elements_by_tag_name("button")
    bt = -1
    for i in range(buttons.__len__()):
        print("bttext:" + buttons[i].text)
        if buttons[i].text == "フォロー中":
            bt = i

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))

    if bt > -1:
        buttons[bt].click()

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))

    # フォローをやめる
    buttons.clear()
    buttons = driver.find_elements_by_tag_name("button")
    bt = -1
    for i in range(buttons.__len__()):
        print("bttext:" + buttons[i].text)
        if buttons[i].text == "フォローをやめる":
            bt = i

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))

    if bt > -1:
        buttons[bt].click()

# いいね
for item in likeUserIdList:
    print(item + "のlikeを開始")

    # 少し待機
    time.sleep(random.randint(randIntFrom, randIntTo))
    # driver.get("https://www.instagram.com/p/" + item + "/")
    driver.get(item)

    # /html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button
    target = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]/span[1]/button')
    span = driver.find_element_by_class_name("glyphsSpriteHeart__outline__24__grey_9")
    print(span.get_attribute("aria-label"))
    if span.get_attribute("aria-label") == "いいね！":
        target.click()

    time.sleep(random.randint(randIntFrom, randIntTo))
    # target.click()
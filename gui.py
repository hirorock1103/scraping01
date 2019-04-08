import tkinter
import tkinter.ttk as ttk
import sqlite3

# connect database
con = sqlite3.connect('sample.db')
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS SampleGetUserList(id integer primary key AUTOINCREMENT, url text, user text)")
query = "CREATE TABLE IF NOT EXISTS SampleGetPostList(" \
        "id integer primary key AUTOINCREMENT, " \
        "url text, " \
        "word text, " \
        "post_date text, " \
        "h_tags text, " \
        "post_user_id text)"
cursor.execute(query)
cursor.execute("CREATE TABLE IF NOT EXISTS Log(id integer primary key AUTOINCREMENT, log_title text, comment text, createdate text)")

cursor.execute('SELECT count(*) as count FROM SampleGetUserList')
numberOfResult = 0
for row in cursor:
    numberOfResult = (row[0])

cursor.execute('SELECT count(*) as count FROM SampleGetPostList')
postNumberOfResult = 0
for row in cursor:
    postNumberOfResult = (row[0])

cursor.execute('SELECT count(*) as count FROM Log')
logNumberOfResult = 0
for row in cursor:
    logNumberOfResult = (row[0])


def pushed():
    print("pushed")


# Tkクラス生成
frm = tkinter.Tk()
# 画面サイズ
frm.geometry('900x700')
# title
frm.title("ユーザーリスト")

note = ttk.Notebook(frm)

tabWidth = 900
tabHeight = 600

tab_a = tkinter.Frame(note, height=tabHeight, width=tabWidth)
tab_b = tkinter.Frame(note, height=tabHeight, width=tabWidth)
tab_c = tkinter.Frame(note, height=tabHeight, width=tabWidth)

note.add(tab_a, text="ユーザー取得リスト")
note.add(tab_b, text="投稿取得リスト")
note.add(tab_c, text="実行ログ")

note.pack()

# ####TAB 1
label = tkinter.Label(tab_a, text="getList(user取得結果一覧)")
label.pack()

label = tkinter.Label(tab_a, text="【件数】" + str(numberOfResult) + "件")
label.pack()

tree = ttk.Treeview(tab_a)

# 列インデックスの作成
tree["columns"] = (1, 2, 3)
# 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
tree["show"] = "headings"
# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1, width=50)
tree.column(2, width=150)
tree.column(3, width=700)

# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1, text="№")
tree.heading(2, text="User")
tree.heading(3, text="URL")

# Data set
cursor.execute('SELECT * FROM SampleGetUserList')
for row in cursor:
    tree.insert("", "end", values=(row[0], row[2], row[1]))
con.commit()
# ツリービューの配置
tree.pack()

# ####TAB 2
label = tkinter.Label(tab_b, text="getList(投稿POST取得結果一覧)")
label.pack()

label = tkinter.Label(tab_b, text="【件数】" + str(postNumberOfResult) + "件")
label.pack()

tree = ttk.Treeview(tab_b, selectmode='browse')
tree.pack(side='left')


# 列インデックスの作成
tree["columns"] = (1, 2, 3, 4, 5)
# 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
tree["show"] = "headings"
# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1, width=50)
tree.column(2, width=60)
tree.column(3, width=240)
tree.column(4, width=100)
tree.column(5, width=450)

# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1, text="№")
tree.heading(2, text="word")
tree.heading(3, text="URL")
tree.heading(4, text="user")
tree.heading(5, text="tag")

# Data set
cursor.execute('SELECT * FROM SampleGetPostList')
for row in cursor:
    try:
        tree.insert("", "end", values=(row[0], row[2], row[1], row[4], row[3]))
    except:
        print("err")
con.commit()
# ツリービューの配置
tree.pack()

# ####TAB 3
label = tkinter.Label(tab_c, text="getList(log)")
label.pack()

label = tkinter.Label(tab_c, text="【件数】" + str(logNumberOfResult) + "件")
label.pack()

tree = ttk.Treeview(tab_c)

# 列インデックスの作成
tree["columns"] = (1, 2, 3)
# 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
tree["show"] = "headings"
# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1, width=40)
tree.column(2, width=350)
tree.column(3, width=150)

# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1, text="№")
tree.heading(2, text="logComment")
tree.heading(3, text="datetime")

# Data set
cursor.execute('SELECT * FROM Log')
for row in cursor:
    try:
        tree.insert("", "end", values=(row[0], row[2], row[3]))
    except:
        print("err")
con.commit()
# ツリービューの配置
tree.pack()


button = tkinter.Button(frm, text="情報更新", command=pushed)

frm.mainloop()
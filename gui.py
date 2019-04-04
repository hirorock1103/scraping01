import tkinter
import tkinter.ttk as ttk
import sqlite3

# connect database
con = sqlite3.connect('sample.db')
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS SampleGetList(id integer primary key AUTOINCREMENT, url text, user text)")
cursor.execute('SELECT count(*) as count FROM SampleGetList')
numberOfResult = 0
for row in cursor:
    numberOfResult = (row[0])


def pushed():
    print("取得しました")
    cursor.execute('SELECT * FROM SampleGetList')
    for row in cursor:
        print(row[0], row[1])
    con.commit()


# Tkクラス生成
frm = tkinter.Tk()

# 画面サイズ
frm.geometry('600x400')
# title
frm.title("ユーザーリスト")

label = tkinter.Label(frm, text="getList(user取得結果一覧)")
label.pack()

label = tkinter.Label(frm, text="【件数】" + str(numberOfResult) + "件")
label.pack()

tree = ttk.Treeview(frm)

# 列インデックスの作成
tree["columns"] = (1, 2, 3)
# 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
tree["show"] = "headings"
# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1, width=40)
tree.column(2, width=150)
tree.column(3, width=400)

# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1, text="№")
tree.heading(2, text="User")
tree.heading(3, text="URL")


# Data set
cursor.execute('SELECT * FROM SampleGetList')
for row in cursor:
    tree.insert("", "end", values=(row[0], row[2], row[1]))
con.commit()
# ツリービューの配置
tree.pack()

button = tkinter.Button(frm, text="情報更新", command=pushed)
button.pack()

frm.mainloop()


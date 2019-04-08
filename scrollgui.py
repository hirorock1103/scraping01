from tkinter import ttk
from tkinter import *
import tkinter as tk
import sqlite3

# connect database
con = sqlite3.connect('sample.db')
cursor = con.cursor()
query = "CREATE TABLE IF NOT EXISTS SampleGetPostList(" \
        "id integer primary key AUTOINCREMENT, " \
        "url text, " \
        "word text, " \
        "post_date text, " \
        "h_tags text, " \
        "post_user_id text)"
cursor.execute(query)

cursor.execute('SELECT count(*) FROM SampleGetPostList')
postNumberOfResult = 0
for row in cursor:
    postNumberOfResult = (row[0])

win = tk.Tk()
win.geometry('1000x500')
win.resizable(width=0, height=0)

title = "投稿リスト 取得件数(" + str(postNumberOfResult) + ")"
label = tk.Label(win, text=title)

label.pack(padx=5, pady=5, anchor=tk.W)

title = "keyword"
label = tk.Label(win, text=title)
label.pack(padx=5, pady=0, anchor=tk.W)

form1 = StringVar()
entry = Entry(win, textvariable=form1).pack(padx=8, pady=5, anchor=tk.W)

title = "#hashtag"
label = tk.Label(win, text=title)
label.pack(padx=5, pady=0, anchor=tk.W)

form2 = StringVar()
entry = Entry(win, textvariable=form2).pack(padx=8, pady=5, anchor=tk.W)


# Button 1
def button1_clicked():
    print(form1.get())
    print(form2.get())
    win.mainloop()


button1 = tk.Button(
    win,
    text='検索',
    command=button1_clicked)

button1.pack(padx=5, pady=5, anchor=tk.W)


# #####  MAKE TABLE  #####
tree = ttk.Treeview(win, selectmode='browse')
tree.pack(side='left')

vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')

tree.configure(yscrollcommand=vsb.set)

tree["columns"] = (1, 2, 3, 4, 5, 6)
tree['show'] = 'headings'

# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1, width=50)
tree.column(2, width=60)
tree.column(3, width=60)
tree.column(4, width=60)
tree.column(5, width=560)
tree.column(6, width=150)


# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1, text="№")
tree.heading(2, text="url")
tree.heading(3, text="word")
tree.heading(4, text="post")
tree.heading(5, text="#hash")
tree.heading(6, text="user")

# Data set
cursor.execute('SELECT * FROM SampleGetPostList')
for row in cursor:
    try:

        dataId = row[0]
        word = row[1]
        postDate = row[2]
        url = row[3]
        user = row[4]
        tag = row[5]

        tree.insert("", "end", values=(dataId, word, postDate, url, user, tag))
    except:
        print("err")
con.commit()

win.mainloop()
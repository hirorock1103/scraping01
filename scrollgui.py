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
        "h_tags text, " \
        "post_user_id text)"
cursor.execute(query)

cursor.execute('SELECT count(*) FROM SampleGetPostList')
postNumberOfResult = 0
for row in cursor:
    postNumberOfResult = (row[0])

print(postNumberOfResult)

win = tk.Tk()
win.resizable(width=0, height=0)

title = str(postNumberOfResult)
label = tk.Label(win, text=title)

label.pack(padx=5, pady=5, anchor=tk.W)

ment = StringVar()
entry = Entry(win, textvariable=ment).pack(padx=5, pady=5, anchor=tk.W)

# #####  MAKE TABLE  #####
tree = ttk.Treeview(win, selectmode='browse')
tree.pack(side='left')

vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')

tree.configure(yscrollcommand=vsb.set)

tree["columns"] = (1, 2, 3, 4, 5)
tree['show'] = 'headings'

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

win.mainloop()
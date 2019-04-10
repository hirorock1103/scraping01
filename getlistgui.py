
from tkinter import ttk
from tkinter import *
import tkinter as tk
import sqlite3
import webbrowser


# connect database
con = sqlite3.connect('sample.db')
cursor = con.cursor()
query = "CREATE TABLE IF NOT EXISTS SampleGetUserList(id integer primary key AUTOINCREMENT, url text, user text)"
cursor.execute(query)


# ****** SQL *******
cursor.execute('SELECT count(*) FROM SampleGetUserList')
postNumberOfResult = 0
for row in cursor:
    postNumberOfResult = (row[0])


# ****** root *******
win = tk.Tk()
win.geometry('1200x500')
win.resizable(width=0, height=0)

# ****** FRAME ******
topFrame = Frame(win)
bottomFrame = Frame(win)
topFrame.pack(anchor=tk.W)
bottomFrame.pack(padx=10, side=LEFT)

# ****** widget *******
titleBuff = StringVar()
titleBuff.set("USERリスト 取得件数(" + str(postNumberOfResult) + "件)")
label0 = tk.Label(topFrame, textvariable=titleBuff)

label0.pack(padx=5, pady=5, anchor=tk.W)

title = "user"
label1 = tk.Label(topFrame, text=title)
label1.pack(padx=5, pady=0, anchor=tk.W, side=LEFT)

form1 = StringVar()
entry = Entry(topFrame, textvariable=form1).pack(padx=8, pady=5, anchor=tk.W, side=LEFT)

title = "url"
label2 = tk.Label(topFrame, text=title)
label2.pack(padx=5, pady=0, anchor=tk.W, side=LEFT)

form2 = StringVar()
entry = Entry(topFrame, textvariable=form2).pack(padx=8, pady=5, anchor=tk.W, side=LEFT)


# Button 1
def button1_clicked():

    formWordUser = form1.get()
    formWordFollower = form2.get()

    query = ""
    query2 = ""
    args = ""
    if formWordUser == "" and formWordFollower == "":
        query = "SELECT count(*) FROM SampleGetUserList"
        query2 = "SELECT * FROM SampleGetUserList ORDER BY id ASC"
        cursor.execute(query)

    elif formWordUser != "" and formWordFollower == "":
        query = "SELECT count(*) FROM SampleGetUserList" + " WHERE user like ?"
        query2 = "SELECT * FROM SampleGetUserList" + " WHERE user like ?  ORDER BY id ASC"
        args = ("%" + formWordUser + "%",)
        cursor.execute(query, args)

    elif formWordUser == "" and formWordFollower != "":
        query = "SELECT count(*) FROM SampleGetUserList" + " WHERE url like ?"
        query2 = "SELECT * FROM SampleGetUserList" + " WHERE url like ?  ORDER BY id ASC"
        args = ("%" + formWordFollower + "%",)
        cursor.execute(query, args)

    else:
        query = "SELECT count(*) FROM SampleGetUserList" + " WHERE user like ? AND url like ?"
        query2 = "SELECT * FROM SampleGetUserList" + " WHERE user like ? AND url like ?  ORDER BY id ASC"
        args = ("%" + formWordUser + "%", "%" + formWordFollower + "%",)
        cursor.execute(query, args)

    for row in cursor:
        number = (row[0])
    titleBuff.set("投稿リスト 取得件数(" + str(number) + "件)")

    if args != "":
        cursor.execute(query2, args)
    else:
        cursor.execute(query2)

    # table reflesh
    for i in tree.get_children():
        tree.delete(i)

    for row in cursor:
        try:
            dataId = row[0]
            userId = row[2]
            follower = row[1]

            tree.insert("", "end", values=(dataId, userId, follower))
        except:
            print("err")

    con.commit()


button1 = tk.Button(
    topFrame,
    text='検索',
    command=button1_clicked)

button1.pack(padx=5, pady=5, anchor=tk.W)


# ****** TABLE *******
tree = ttk.Treeview(bottomFrame, selectmode='browse')
vsb = ttk.Scrollbar(bottomFrame, orient="vertical", command=tree.yview)
tree.pack(side='left')
vsb.pack(side='right', fill='y')

tree.configure(yscrollcommand=vsb.set)


# 列インデックスの作成
tree["columns"] = (1, 2, 3)
tree['show'] = 'headings'

# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1, width=50)
tree.column(2, width=150)
tree.column(3, width=700)

# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1, text="№")
tree.heading(2, text="User")
tree.heading(3, text="URL")


def callback(event):
    url = ""
    for i in tree.selection():
        print(tree.item(i))
        print(tree.item(i)['values'][2])
        url = tree.item(i)['values'][2]
        webbrowser.open_new(url)

tree.bind("<Double-1>", callback)

# Data set
cursor.execute('SELECT * FROM SampleGetUserList ORDER BY id ASC')
for row in cursor:
    try:
        dataId = row[0]
        userId = row[2]
        follower = row[1]

        tree.insert("", "end", values=(dataId, userId, follower))
    except:
        print("err")

con.commit()

win.mainloop()

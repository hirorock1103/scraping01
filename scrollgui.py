
from tkinter import ttk
from tkinter import *
import tkinter as tk
import sqlite3
import webbrowser


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


# ****** SQL *******
cursor.execute('SELECT count(*) FROM SampleGetPostList')
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
titleBuff.set("投稿リスト 取得件数(" + str(postNumberOfResult) + "件)")
label0 = tk.Label(topFrame, textvariable=titleBuff)

label0.pack(padx=5, pady=5, anchor=tk.W)

title = "keyword"
label1 = tk.Label(topFrame, text=title)
label1.pack(padx=5, pady=0, anchor=tk.W, side=LEFT)

form1 = StringVar()
entry = Entry(topFrame, textvariable=form1).pack(padx=8, pady=5, anchor=tk.W, side=LEFT)

title = "#hashtag"
label2 = tk.Label(topFrame, text=title)
label2.pack(padx=5, pady=0, anchor=tk.W, side=LEFT)

form2 = StringVar()
entry = Entry(topFrame, textvariable=form2).pack(padx=8, pady=5, anchor=tk.W, side=LEFT)


# Button 1
def button1_clicked():

    formWordKeyWord = form1.get()
    formWordHashTag = form2.get()

    query = ""
    query2 = ""
    args = ""
    if formWordKeyWord == "" and formWordHashTag == "":
        query = "SELECT count(*) FROM SampleGetPostList"
        query2 = "SELECT * FROM SampleGetPostList ORDER BY id ASC"
        cursor.execute(query)

    elif formWordKeyWord != "" and formWordHashTag == "":
        query = "SELECT count(*) FROM SampleGetPostList" + " WHERE word like ?"
        query2 = "SELECT * FROM SampleGetPostList" + " WHERE word like ?  ORDER BY id ASC"
        args = ("%" + formWordKeyWord + "%",)
        cursor.execute(query, args)

    elif formWordKeyWord == "" and formWordHashTag != "":
        query = "SELECT count(*) FROM SampleGetPostList" + " WHERE h_tags like ?"
        query2 = "SELECT * FROM SampleGetPostList" + " WHERE h_tags like ?  ORDER BY id ASC"
        args = ("%" + formWordHashTag + "%",)
        cursor.execute(query, args)

    else:
        query = "SELECT count(*) FROM SampleGetPostList" + " WHERE word like ? AND h_tags like ?"
        query2 = "SELECT * FROM SampleGetPostList" + " WHERE word like ? AND h_tags like ?  ORDER BY id ASC"
        args = ("%" + formWordKeyWord + "%", "%" + formWordHashTag + "%",)
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
            word = row[1]
            postDate = row[2]
            url = row[3]
            user = row[4]
            tag = row[5]
            create = row[7]
            converted_post_date = row[6]

            tree.insert("", "end", values=(dataId, word, postDate, url, user, tag, create, converted_post_date))
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

tree["columns"] = (1, 2, 3, 4, 5, 6, 7, 8)
tree['show'] = 'headings'

# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1, width=40)
tree.column(2, width=60)
tree.column(3, width=60)
tree.column(4, width=80)
tree.column(5, width=520)
tree.column(6, width=150)
tree.column(7, width=120)
tree.column(8, width=120)

# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1, text="№")
tree.heading(2, text="url")
tree.heading(3, text="word")
tree.heading(4, text="post")
tree.heading(5, text="#hash")
tree.heading(6, text="user")
tree.heading(7, text="Date")
tree.heading(8, text="post")


def callback(event):
    url = ""
    for i in tree.selection():
        print(tree.item(i)['values'][1])
        url = tree.item(i)['values'][1]
        webbrowser.open_new(url)


tree.bind("<Double-1>", callback)

# Data set
cursor.execute('SELECT * FROM SampleGetPostList  ORDER BY id ASC')
for row in cursor:
    try:
        dataId = row[0]
        word = row[1]
        postDate = row[2]
        url = row[3]
        user = row[4]
        tag = row[5]
        create = row[7]
        converted_post_date = row[6]

        tree.insert("", "end", values=(dataId, word, postDate, url, user, tag, create, converted_post_date))
    except:
        print("err")

con.commit()

win.mainloop()

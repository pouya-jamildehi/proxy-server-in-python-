import socket
import sqlite3 as db
import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#x=db.connect('database.db')
#x.close()
def admin():
    root = Tk()
    root.resizable(width=False, height=False)
    root.title('Main Page')
    lable = Label(root, text="MAIN PAGE")
    lable.grid(row=0, column=1)
    lable.config(font='Times 22', fg='green')
    button1 = Button(root, text=' start  ', command=main_a)
    button2 = Button(root, text='database', command=g_db)
    button3 = Button(root, text='quit', command=quit)
    button4 = Button(root, text='filter', command=g_filter)
    button2.grid(row=3, column=1, padx=220, sticky=W, pady=6)
    button1.grid(row=3, column=1, sticky=W, padx=50, pady=6)
    button3.grid(row=3, column=1, sticky=W, padx=280, pady=6)
    button4.grid(row=3, column=1, sticky=W, padx=180, pady=6)
    root.mainloop()

def login_a():
    global username,password,entry1,entry2
    username="admin"
    password="admin"
    def login():
        value1 = entry1.get()
        value2 = entry2.get()
        if value1 == username and value2 == password:
            messagebox.showinfo("Success", "You log in !")
            gui1.quit()
        else:
            messagebox.showinfo("Error", "Wrong password or username")

    gui1 = Tk()
    gui1.resizable(width=False, height=False)
    gui1.title('proxy server')
    lable = Label(gui1, text="PROXY SERVER")
    lable.grid(row=0, column=1)
    lable.config(font='Times 22', fg='red')
    entry1 = Entry(gui1, width=30)
    entry2 = Entry(gui1, width=30)
    entry2.config(show='*')
    lblentry1 = ttk.Label(text="Your Username : ")
    lblentry2 = ttk.Label(text="Your Password : ")
    lblentry1.grid(row=1, column=0, sticky='W', pady=10)
    lblentry2.grid(row=2, column=0, sticky='W')
    entry1.grid(row=1, column=1, sticky=W)
    entry2.grid(row=2, column=1, sticky=W)
    button1 = Button(gui1, text='Login', command=login)
    button1.grid(row=3, column=1, sticky=W, padx=50, pady=6)
    gui1.mainloop()
def g_db():
    gui=Tk()
    x = show()
    gui.title('Data Base')
    lable = Label(gui, text="DATA BASE")
    lable.grid(row=0, column=1)
    lable.config(font='Times 22', fg='blue')
    Descrip = Text(gui, width=70, height=15, font=(("Arial"), 10), wrap=WORD)
    Descrip.insert(INSERT,x)
    Descrip.grid(row=1, column=1, pady=5, sticky=W)
    # button1=Button(gui,text=' change username/password  ')
    #button2 = Button(gui, text='main page',command=mainpage)
    button3 = Button(gui, text='quit', command=gui.quit)
    #button2.grid(row=3, column=1, padx=20, sticky=W, pady=6)
    # button1.grid(row=3,column=1,sticky=W,padx=50,pady=6)
    button3.grid(row=3, column=1, sticky=W, padx=120, pady=6)
    gui.mainloop()
def g_filter():
    gui = Tk()
    x = show_filter()
    gui.title('filter')
    lable = Label(gui, text="Filter")
    lable.grid(row=0, column=1)
    lable.config(font='Times 22', fg='brown')
    Descrip = Text(gui, width=70, height=15, font=(("Arial"), 10), wrap=WORD)
    Descrip.insert(INSERT, x)
    Descrip.grid(row=1, column=1, pady=5, sticky=W)
    button3 = Button(gui, text='quit', command=gui.quit)
    button3.grid(row=3, column=1, sticky=W, padx=120, pady=6)
    gui.mainloop()
def main_a():
    global data, a, browser, webserver, temp, client, spec, buffer, counter, flag_filter,username, password, entry1, entry2
    flag_filter = 0
    counter = 0
    buffer = 1000000
    #create_table_filter()
    #create_table()
    a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    a.bind(("127.0.0.1", 8078))
    a.listen(1)
    client, spec = a.accept()

    while True:
        try:
            data = client.recv(buffer)
            threading.Thread(target=position()).start()
        except Exception as e:
            print(e)

#POSITION
def position():
    try:

        first_line=data.decode("ANSI").split("\n")[0]

        url = first_line.split(" ")[1]

        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        temp = url[(http_pos + 3):]#url site

        port_pos = temp.find(":")

        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos + 1):][:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        se(webserver, port, client, data, spec,temp)
    except Exception as e:
        print(e)

def se(webserver,port,clinet,data,spec,temp):
    try:
        check_filter(temp)
        if flag_filter == 0:
            b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            b.connect((webserver, port))
            b.send(data)
            insert(spec[0], webserver)#insert to database
            while 1:
                reply = b.recv(10000)
                if len(reply) > 0:
                    client.sendall(reply)
                else:
                    break
            b.close()
    except Exception as e:
        print(e)

def check_filter(url):
    try:
        x=db.connect('database.db')
        cur=x.cursor()
        cur.execute("select * from filter")
        filter_table=cur.fetchall()
        for i in range(0,len(filter_table)):
            if filter_table[i] == url:
                flag_filter=1
                return print("Page is Filter")
    except Exception as e:
        print(e)

###############################################################
#DATABASE

def create_table():
    x = db.connect('database.db')
    cur = x.cursor()
    cur.execute("create table a1 (id integer primary key autoincrement,ip text  , adress text ,)")
    x.close()

def create_table_filter():
    x=db.connect('database.db')
    cur=x.cursor()
    cur.execute("create table filter (url text PRIMARY KEY )")
    x.close()

def insert(ip1,adress1):
    x = db.connect('database.db')
    cur = x.cursor()
    adress=adress1
    ip=ip1
    ips = x.cursor()
    if check(ip,adress) == 0:
        cur.execute("insert into a1(ip, adress) values ('{}', '{}')".format(ip, adress))
        x.commit()
    x.close()

def insert_filter():
    x=db.connect('database.db')
    cur = x.cursor()
    url=input("import url filter:")
    cur.execute("insert into filter(url) values ('{}')".format(url))
    x.commit()
    x.close()

def show():
    x = db.connect('database.db')
    cur = x.cursor()
    cur.execute("select * from a1")
    ips = cur.fetchall()
    x.close()
    return ips
    #print(ips)

def show_filter():
    x=db.connect('database.db')
    cur=x.cursor()
    cur.execute("select * from filter")
    y=cur.fetchall()
    x.close()
    return y
    #print(y)

def check(a,b):
    flag=0
    x=db.connect('database.db')
    cur=x.cursor()
    cur.execute("select * from a1")
    check_table=cur.fetchall()
    if len(check_table)!=0:
        for i in range(0, len(check_table)):
            if (check_table[i][1]) == str(a):
                if check_table[i][2] == b:
                    flag=1
                    return flag
    return flag
    x.close()

def delete_contact():
    x = db.connect('database.db')
    cur = x.cursor()
    c_id = int(input("Enter an id for edit contact: "))
    cur.execute("delete from a1 where ip = {}".format(c_id))
    x.commit()
    x.close()

#################################################################



login_a()

while True:
    admin()

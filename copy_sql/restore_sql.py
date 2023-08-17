"""
This program is the second phase of "copy_sql" module.
It restores the databases and it's structures using the text and csv files created by "copy_sql.py".
It uses os, mysql connector, tkinter(for GUI), user built module(easy_sql, oopen).
"""
import os
root_dir = os.getcwd()
req_mods = {"easy_sql" : "sql_functions", "oopen" : "openeasy"}
req_mods_lnk = {"sql_functions" : "https://github.com/karthikvvk/make-life-easy-python-packages-easy_sql/blob/main/make-life-easy-python-packages-easy_sql/sql_functions.py", "oopen" : "https://github.com/karthikvvk/make-life-easy-python-packages-oopen/blob/main/make-life-easy-python-packages-oopen/openeasy.py"}
for hi in req_mods:
    if os.path.exists(hi):
        pass
    else:
        os.mkdir(hi)
    open(f"{root_dir}\\{hi}\\{req_mods[hi]}.py", 'w').close()
    open(f"{root_dir}\\{hi}\\__init__.py", 'w').close()
    os.system(f"curl -o {root_dir}\\{hi}\\{req_mods[hi]}.py {req_mods_lnk[hi]}")
import mysql.connector as c
from tkinter import *
import oopen.openeasy as op


root = Tk()
root.geometry('500x300')
root.title('copy_sql')

user_name_tv = StringVar()
host_name_tv = StringVar()
password_tv = StringVar()

passwd = ''
host = ''
user = ''

def submit():
    global passwd, host, user
    passwd = password_tv.get()
    host = host_name_tv.get()
    user = user_name_tv.get()
    root.destroy()



Entry(root, textvariable=password_tv).grid(row=0, column=1)
Label(root, text='enter your mysql password:', justify='left').grid(row=0, column=0)

Entry(root, textvariable=host_name_tv).grid(row=1, column=1)
Label(root, text='enter your mysql host name:', justify='left').grid(row=1, column=0)

Entry(root, textvariable=user_name_tv).grid(row=2, column=1)
Label(root, text='enter your mysql user name:', justify='left').grid(row=2, column=0)

Button(root, text='submit', command=submit).grid(row=3, column=0)
root.mainloop()

dir = os.listdir()
pat = os.getcwd()
for i in dir:
    if '.' in i:
        dir.remove(i)

db = c.connect(user=user, host=host, passwd=passwd)
cr = db.cursor()

for j in dir:
    cr.execute(f'create database if not exists {j}')

    mydb = c.connect(user='root', host='localhost', passwd='vk07092005', database=j)
    mycr = mydb.cursor()

    tables = os.listdir(pat + '\\' + j)
    tables.sort()
    n = 0
    nn = n + 1
    for t in range(int(len(tables) / 2)):

        cs_v = op.o_read(pat + '\\' + j + '\\' + tables[n]).split('\n')
        cs_v.remove('')
        txt = op.o_read(pat + '\\' + j + '\\' + tables[nn]).replace("'", '').split('\n')
        txt.remove('')

        namcsv = tables[n].rstrip('.csv')
        namtxt = tables[nn].rstrip('.txt')
        st = f'create table if not exists {namcsv} ('
        sp = cs_v

        no = 0

        for i in sp:
            lis = i.split(',')

            if 'YES' in lis[2]:
                null = 'null'
            else:
                null = ''

            if 'PRI' in lis[3]:
                primary = 'primary key'

            if 'None' in lis[4]:
                default = ''
            else:
                default = lis[4]

            if len(lis[5]) > 0:
                extra = lis[5]
            else:
                extra = ''


            qr = lis[0] + ' ' + lis[1].lstrip("b'").rstrip("'") + ' '
            if null:
                qr += null + ' '
            if default:
                qr += default.lstrip("b") + ' '
            if extra:
                qr += extra + ')'
            st += qr + ','

            if no == len(sp) - 1:
                st = st.rstrip(',') + ')'
                break
            no += 1
        n += 2
        nn += 2
        mycr.execute(st)

        tup = tuple(txt)
        for u in txt:
            mycr.execute(f'insert into {namcsv} values({u})')
            mydb.commit()


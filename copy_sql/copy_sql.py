"""
This program is the first phase of "copy_sql" module.
It copies the databases and it's structures in the text and csv files created by "copy_sql.py" in such a way it can be read and restored by "restore_sql.py".
It uses os, csv, runpy, mysql connector, tkinter(for GUI), user built module(easy_sql, oopen).
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
import easy_sql.sql_functions as es
import runpy

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
if len(passwd) > 0:
    pass
else:
    runpy.run_path('copy_sql.py')

try:
    db = c.connect(user=user, host=host, passwd=passwd)
except:
    Label(root, text='wrong password or user name', justify='left').grid(row=3, column=2)

mc = db.cursor()
databases = es.show_db(mc)
for i in ['information_schema', 'mysql', 'performance_schema', 'sys', 'world', 'sakila']:
    if i in databases:
        databases.remove(i)
columns = []

for i in databases:
    cr_dir = os.getcwd()
    os.mkdir(i)
    os.chdir(os.getcwd() + fr'\{i}')
    data = c.connect(user=user, host=host, passwd=passwd, database=i)
    cursors = data.cursor()

    tables = es.show_tables(cursors)
    for j in tables:

        cursors.execute(f'desc {j}')
        s = cursors.fetchall()
        lt = []
        for k in s:
            op.o_write(j+'.csv', str(k).rstrip(')').lstrip('(').replace("'", "").replace(" ", ""), newline=True)
        cursors.execute(f'select * from {j}')
        dta = cursors.fetchall()
        for h in dta:
            op.o_write(j+'.txt', [str(h).rstrip(')').lstrip('(')], newline=True)
    os.chdir(cr_dir)

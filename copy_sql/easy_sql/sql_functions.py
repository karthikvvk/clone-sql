"""
This is a module made using python to make the MYSQL-python interaction easier.
It uses MYSQL connector's functions to accomplish the task.
It also uses os module to operatee over the files.
"""
import mysql.connector as c

def show_db(cursor):
    cursor.execute('show databases')
    r = cursor.fetchall()
    lis = []
    for k in range(len(r)):
        t = str(r[k]).rstrip("'),")
        gm = t.lstrip("('")
        lis.append(gm)
    return lis


def search_database(cursor, database):
    cursor.execute('show databases')
    r = cursor.fetchall()
    for k in range(len(r)):
        t = str(r[k]).rstrip("'),")
        gm = t.lstrip("('")
        if gm == database:
            return True


def show_tables(cursor):
    cursor.execute('show tables')
    r = cursor.fetchall()
    lis = []
    for k in range(len(r)):
        t = str(r[k]).rstrip("'),")
        gm = t.lstrip("('")
        lis.append(gm)
    return lis


def search_table(cursor, table):
    cursor.execute('show databases')
    r = cursor.fetchall()

    for k in range(len(r)):
        t = str(r[k]).rstrip("'),")
        gm = t.lstrip("('")
        if gm == table:
            return True

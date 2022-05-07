import os.path
from types import TracebackType
import mysql.connector

def mainmenu():
    Dropdown = input(print("""
    What system do you want:
    1: Make a new DB
    2: Make the Table to store hash files
    """))
    if Dropdown == 1:
        MakeDB()
    if Dropdown == 2:
        MakeTable()

def MakeDB():
    session = mysql.connector.connect(
        host='127.0.0.1',
        user='pythonuser',
        port='3306',
        password='PythonSQLPass',
        
    )
    cursor = session.cursor()
    db_cursor = session.cursor()
    db_cursor.execute("CREATE DATABASE MasterHash")
    for db in db_cursor:
        print(db)

def MakeTable():
    session = mysql.connector.connect(
        host='127.0.0.1',
        user='pythonuser',
        port='3306',
        database ='MasterHash',
        password='PythonSQLPass',
    )
    cursor = session.cursor()
    db_cursor = session.cursor()
    try:
        print("Trying to Make Table Now")
        db_cursor.execute("CREATE TABLE systemhash (FileName VARCHAR(255), MD5 VARCHAR(255))")
        for db in db_cursor:
            print(db)
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

mainmenu()
"""
The following code was made for the point was to build a basic anti-virus

Author is Graham Gibney
Student Number B00119513

API = "Please use your on company API key here as none will be provided"

"""
import datetime
import glob
import hashlib
import os.path
import time
from os import listdir, name, system, walk
from os.path import isfile, join
from types import TracebackType
import HashingSystem
import SQLSettings

import mysql.connector

from NoneMain.Hashfile import getmd5

utc = datetime.datetime.now().time()
session = mysql.connector.connect(
    host='192.168.10.1',
    user='pythonuser',
    database ='hashsystem',
    port='3306',
    password='PythonSQLPass',
)
cursor = session.cursor()

def mainmenu():
    print("This code was wrote by Cyber_Gman / Graham Gibney Student number B00119513 please do not abuse this system")
    print("----------------------------------------------------------------------------------------------------------")
    print("The Current Time is:")
    print(utc)
    print("You are currently connected to ", session)
    print("""Please chose from the following 
    1: Scan File System and Hashfile
    2: Check MD5 Hash agisnt DB
    """)
    answer = input("Enter your choice here using number value: ")
    if answer == "1":
        Hashingsystem()
    elif answer == "2":
        databaselookup()
    elif answer != " ":
        checkNull()

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

    
def checkNull():
    print("Please enter a valid number from the list")
    time.sleep(7)
    clear()
    time.sleep(5)
    mainmenu()

def Hashingsystem():
    print("To scan a drive please follow the following guidelines")
    print("""
    [1] Use the Name of the Drive in the following format 
    [2] Then use the following  This will scan the whole drive
    [3] Then hit enter and make sure everything runs
    """)
    hashing101 = glob.iglob(input("Enter Drive Name:\n"), recursive=True)
    HashingSystem.md5(hashing101)
    HashingSystem.DBInput(hashing101)

def databaselookup():
    MD5 = input("What hash are you looking to find:n\
        ")
    cursor.execute("Select MD5 FROM systemhashs WHERE MD5=%s", (MD5,))
    data = cursor.fetchall()
    if data:
        print("MD5 Found In DB")
    else:
        print("No MD5 Hash found")
mainmenu()

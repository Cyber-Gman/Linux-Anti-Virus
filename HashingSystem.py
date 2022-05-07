import hashlib
import glob
from logging import exception
import os.path
import csv
from types import TracebackType
import mysql.connector
import ntpath
import time
from LAV.sql import sqlconcur
from alive_progress import alive_bar

session,cursor = sqlconcur()


def hashinginput():
    print("You are currently connected to ", session)


def md5(fname1):
    try:
        if os.path.isfile(fname1):
            hash_md5 = hashlib.md5()
            for fname in fname1:
                try:
                    print(fname)
                    with open(fname, "rb") as f:
                        for chunk in iter(lambda: f.read(2 ** 20), b""):
                            hash_md5.update(chunk)
                            return hash_md5.hexdigest()
                except Exception as E:
                    print("File Not accessable at this time moving on")
                    print(E)
    except exception as e:
        print(f"starting md5 crash\n{e}\nending md5 crash fin")
        exit()

path = '/home/gman/AntiVirus Tool/test.txt'

viruslist = open(path,'rt')
virusinside = [l.rstrip() for l in viruslist]
virus="detected"
novirus="clear"


import os
def DBInput(fname):
    with alive_bar(1000, force_tty=True) as bar:
        for filename in fname:
            try:
                if os.path.isfile(filename):
                    time.sleep(0.02)
                    newmd5 = md5(fname)
                    print(filename)
                    bar()

                    print(newmd5)
                    if newmd5 in virusinside:
                        print(virus)
                        time.sleep(5)
                        basicname = ntpath.basename(filename)
                        time.sleep(5)
                        cursor.execute(f"insert into virushash (FileName, MD5) values ('{basicname}', '{newmd5}')") 
                        time.sleep(5)

                    else:
                        try:
                            cursor.execute(f"insert into systemhashs (FileName, MD5) values ('{filename}', '{newmd5}')") 
                            session.commit()
                            print("Files Added")
                        except mysql.connector.Error as error:
                            print("Failed to insert into MySQL table {}".format(error))
            except exception as e:
                print(f"starting DBInput crash\n{e}\nfinishing DBInput crash")
                exit()
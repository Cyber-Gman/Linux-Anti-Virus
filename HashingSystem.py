from ast import pattern
import hashlib
import glob
from logging import exception
import os.path
import csv
from types import TracebackType
from click import style
import mysql.connector
import ntpath
import time
from LAV.sql import sqlconcur,elementexists,getdetails
from alive_progress import alive_bar
import os



def hashinginput():
    print("You are currently connected to ", session)


def md5(fname1):
    try:
        hash_md5 = hashlib.md5()
        for fname in fname1:
            if os.path.isfile(fname) and os.access(fname, os.R_OK):
                try:
                    with open(fname, "rb") as f:
                        for chunk in iter(lambda: f.read(2 ** 20), b""):
                            hash_md5.update(chunk)
                            return hash_md5.hexdigest()
                except Exception as e:
                    print("File Not accessable at this time moving on")
                    print(e)
    except Exception as e:
        print(f"starting md5 crash\n{e}\nending md5 crash fin")
        exit()





def DBInput(fname,clear):
    clear()
    path = input('Malware Hash file location eg /home/user/hashes.txt:\nOr leave blank if hashes.txt is in current directory\n')
    if path == "" or path is None:
        path = "./hashes.txt"
    session,cursor = sqlconcur()
    time.sleep(2)
    clear()
    viruslist = open(path,'rt')
    virusinside = [l.rstrip() for l in viruslist]
    virus="detected"
    novirus="clear"
    with alive_bar(force_tty=True,theme="smooth") as bar:
        id = getdetails()[0]
        for filename in fname:
            if os.path.isfile(filename) and os.access(filename, os.R_OK):
                try:
                    time.sleep(0.02)
                    newmd5 = md5(fname)
                    bar()

                    print(f"FileName: {filename}\nMD5: {newmd5}")
                    if newmd5 in virusinside:
                        print(f"Virus detected: {virus}")
                        time.sleep(5)
                        basicname = ntpath.basename(filename)
                        time.sleep(5)
                        if not elementexists(cursor, id,filename):
                            cursor.execute(f"insert into {id} (FileName, MD5) values ('{basicname}', '{newmd5}')") 
                        time.sleep(5)

                    else:
                        try:
                            if not elementexists(cursor, id,filename):
                                cursor.execute(f"insert into {id} (FileName, MD5) values ('{filename}', '{newmd5}')") 
                                session.commit()
                                print("Files Added")
                        except mysql.connector.Error as error:
                            print("Failed to insert into MySQL table {}".format(error))
                except Exception as e:
                    print(f"starting DBInput crash\n{e}\nfinishing DBInput crash")
                    exit()

# This code provides the the functions necessary with communicating with the mysql database
# @author  TallPanda
# @version 1.03 10th of January 2022
# @platform   Python 3.10.1
from mysql import connector
import json,os
import uuid,getpass
import time

from progressbar.bar import ProgressBar

def getdetails(config:str=None):# gets the details of from the login.json file
    if config == None:
        config = "config/mysql/secure/login.json"
    if not os.path.isfile(config):
        raise(f"Config does not exist at {config}")
    
    with open(config, "r") as details:
        details = json.loads(details.read())
        host = details["host"]
        passw = details["password"]
        user = details["user"]
        database = details["database"]
        port = details["port"]
    id = f"{getpass.getuser()}_{uuid.getnode()}"
    return id,host,passw,user,database,port

def sqlconcur(config:str=None):# returns the console and cursor object for the mysql package
    host,passw,user,database,port = getdetails(config)[1:]

    try:
        con =connector.connect(host=host,user=user,password=passw,database=database,port=port)
        print(f"""
        Connected to {con.server_host} as User '{con.user}' on Port: {con.server_port}    
        Server Version: {con.get_server_info().replace('-0ubuntu0.',',Ubuntu-').strip(str.join(".",[str(_) for _ in con.get_server_version()])+"-").replace("-",":").split(",")}
        Connection ID: {con.connection_id}
        """)
        cur = con.cursor(buffered=True)
        return con,cur
    except Exception as e:
        if "Can't connect to MySQL server on" in str(e):
            print(f"Connection Issues on {host}:{port}")
            print("Retrying in 2 minutes\nPlease contact the devloper if the issue cannot be resolved")
            time.sleep(120)
            return sqlconcur(config)
        else:
            print(e)
            raise "Please contact the devloper if the issue cannot be resolved"


def tablexists(cur,table):# checks is table exists
    cur.execute("show tables;")
    for x in cur:
        if table in x:
            return True
    return False

def makeusertable(cur,id):# makes a table for the users data
    if not tablexists(cur,id):
        cur.execute(f"create Table {id}(SHA1 VARCHAR(255) UNIQUE not null, vtstatus int not null default 0, fname  VARCHAR(255), primary key (SHA1));")
        print(f"Table {id} created.")
    else:
        inp = input(f"Table: {id} already exists\nDo you want to recreate the table?(Y/N)\n")
        while not inp.lower() in ["y","n"]:
            inp = input(f"Table: {id} already exists\nDo you want to recreate the table?(Y/N)\n")

        match inp.lower():
            case "y":
                cur.execute(f"drop Table {id};")
                cur.execute(f"create Table {id}(SHA1 VARCHAR(255) UNIQUE not null, vtstatus int not null default 0, fname  VARCHAR(255), primary key (SHA1));")
                print(f"Table {id} created.")
            case "n":
                print(f"Skipping table {id}")


def elementexists(cur,id,key,element=None):# checks if sha1 already exists
    if element == None:
        element = "SHA1"
    cur.execute(f"select * from {id} where {element}='{key}'")
    for message in cur:
        if key in message:
            return True
    return False

def uploadata(cur,id,userdata):# Uploads the sha1 hash along with the vt status 0 by default meaning not uploaded
    n = len(userdata.keys())
    i = 0
    with ProgressBar(max_value=n) as pb:
        for key,value in userdata.items():
            pb.update(i)
            value,fname = list(value)
            if not elementexists(cur,id,key):
                cur.execute(f"insert into {id} (SHA1, vtstatus, fname) values ('{key}',{value},'{fname}')")
            i+=1

def notfounds(cur,id,element=None):# retuns hashes not found in thedatabase
    if element == None:
        element = "SHA1"
    cur.execute(f"select * from {id} where (not vtstatus=2 or not vtstatus=3) and {element} not in (select {element} from uniq);")
    nfs = {}
    try:
        for i in cur:
            key,value,fname =i
            nfs[key] = [value,fname]
        return nfs
    except:
        return nfs


def sql(userdata,config:str=None):
    id = getdetails(config)[0]
    con, cur = sqlconcur()
    with con as con:
        with cur as cur:
            makeusertable(cur,id)
            uploadata(cur,id,userdata)
            return(notfounds(cur,id))

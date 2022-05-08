# This code provides the the functions necessary with communicating with the mysql database
# @author  TallPanda
# @version 1.03 10th of January 2022
# @platform   Python 3.10.1
from mysql import connector
import json,os
import uuid
import time

# from progressbar.bar import ProgressBar

def getdetails(config:str=None,database:str=None):# gets the details of from the login.json file
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
    id = f"systemhashes_{uuid.getnode()}"
    
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

def sqlconcurnodb(config:str=None):
    host,passw,user,database,port = getdetails(config)[1:]
    try:
        con =connector.connect(host=host,user=user,password=passw,port=port)
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
        cur.execute(f"create Table {id}(MD5 VARCHAR(255),FileName VARCHAR(255) UNIQUE not null, primary key (FileName));")
        print(f"Table {id} created.")
    else:
        inp = input(f"Table: {id} already exists\nDo you want to recreate the table?(Y/N)\n")
        while not inp.lower() in ["y","n"]:
            inp = input(f"Table: {id} already exists\nDo you want to recreate the table?(Y/N)\n")

        match inp.lower():
            case "y":
                cur.execute(f"drop Table {id};")
                cur.execute(f"create Table {id}(MD5 VARCHAR(255),FileName VARCHAR(255) UNIQUE not null, primary key (FileName));")
                print(f"Table {id} created.")
            case "n":
                print(f"Skipping table {id}")

def makeuserdb(cur):# makes a db for the users data
    try:
        cur.execute(f"CREATE DATABASE MasterHash;")
        print(f"DB MasterHash created.")
    except Exception as e:
        print(e)
        
def elementexists(cur, id, key, element=None):# checks if MD5 already exists
    if element == None:
        element = "FileName"
    cur.execute(f"select * from {id} where {element}='{key}'")
    for message in cur:
        if key in message:
            return True
    return False
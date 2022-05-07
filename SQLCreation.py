import os.path
from types import TracebackType
import mysql.connector
from LAV.sql import sqlconcur,makeusertable,makeuserdb,getdetails
def mainmenu():
    session,cur = sqlconcur()
    id = getdetails()[0]
    with cur as cur:
        Dropdown = input("""
        What system do you want:
        1: Make a new DB
        2: Make the Table to store hash files
        3: Exit
        """)
        if Dropdown == "1":
                makeuserdb(cur)
        elif Dropdown == "2":
            makeusertable(cur,id)
        elif Dropdown == "3":
            print("exiting")
            exit()
        mainmenu()
if __name__ == "__main__":
    mainmenu()
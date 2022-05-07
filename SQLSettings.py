import mysql.connector
from LAV.sql import sqlconcur
value = 0

def ConnectDB():
    session,cursor = sqlconcur()
    cursor.execute("SELECT * FROM systemhashes LIMIT 50;")
    result = cursor.fetchall
    while value >= 50:
        value ++1
        print(result)

ConnectDB()
import mysql.connector
value = 0

def ConnectDB():
    session,cursor = sqlconcur()
    cursor.execute("SELECT * FROM systemhashs LIMIT 50;")
    result = cursor.fetchall
    while value >= 50:
        value ++1
        print(result)

ConnectDB()
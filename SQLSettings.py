import mysql.connector
value = 0

def ConnectDB():
    session = mysql.connector.connect(
        host='192.168.10.1',
        user='pythonuser',
        port='3306',
        database ='hashsystem',
        password='PythonSQLPass',   
    )
    cursor = session.cursor()
    cursor.execute("SELECT * FROM systemhashs LIMIT 50;")
    result = cursor.fetchall
    while value >= 50:
        value ++1
        print(result)

ConnectDB()
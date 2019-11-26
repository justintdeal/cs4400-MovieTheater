from theater import app
import mysql.connector
import os

#db connection info
user = "team50"
password = "Columns1!"
host = "127.0.0.1"

def connect():
    connection = mysql.connector.connect(user=user, password=password, host=host)
    return connection

def runSqlFile(path):
    connection = connect()
    cursor = connection.cursor()
    
    temp = open(path, 'r')
    sql = temp.read()
    temp.close()
    
    commands = sql.split(';')
    
    for command in commands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except IOError:
            print("skipped")
            
    cursor.close()
    connection.close()

def initDB(schema, data, procedures):
    runSqlFile(schema)
    os.system('mysql -u {} -p{} team50 < {}'.format(user, password, procedures))
    runSqlFile(data)
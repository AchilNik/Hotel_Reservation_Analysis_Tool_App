import mysql.connector

def db_connection():
    try:
        my_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='',
            database='Project2023'
        )
    except mysql.connector.Error as err:
        print(f'Failed connecting to MySQL database: {err}\n')
        exit('Program terminated unexpectedly\n')

    return my_connection
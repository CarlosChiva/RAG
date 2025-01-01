import mysql.connector
def db_connect():
    db = mysql.connector.connect(
    
        host='localhost',  # Host is the service name from Docker Compose
        user='app_user',
        password='app_password',
        port=3306,
        database='app_db'

    )
    return db
def checker_users(user_name:str,password:str):
    print("User:",user_name)
    print("Password:",password)
    db= db_connect()
    mysql_cursor = db.cursor()
    mysql_cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (user_name, password))
    mysql_cursor.fetchall()
    if mysql_cursor.rowcount == 0:
        mysql_cursor.close()
        db.close()
        return False
    db.close()
    return True
def registrer_users(user_name:str,password:str):
    db= db_connect()
    print("User:",user_name)
    print("Password:",password)
    mysql_cursor = db.cursor()
    mysql_cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (user_name, password))
    mysql_cursor.close()
    db.commit()
    db.close()

    return True
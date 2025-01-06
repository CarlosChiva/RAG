import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os
async def db_connect():
    db = mysql.connector.connect(
    
        host=os.getenv("DB_HOST"),  # Host is the service name from Docker Compose
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=3306,
        database=os.getenv("DB_DATABASE")

    )
    return db
async def checker_users(user_name:str,password:str):

    db= await db_connect()
    mysql_cursor = db.cursor()
    mysql_cursor.execute("SELECT username,password_hash FROM users WHERE username = %s AND password_hash = %s", (user_name, password))
    mysql_cursor.fetchall()
    if mysql_cursor.rowcount == 0:
        mysql_cursor.close()
        db.close()
        return False
    db.close()
    return True
async def registrer_users(user_name:str,password:str):
    db= await db_connect()

    mysql_cursor = db.cursor()
    mysql_cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (user_name, password))
    mysql_cursor.close()
    db.commit()
    db.close()

    return True

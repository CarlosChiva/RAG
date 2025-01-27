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

async def check_user_by_credential(credential:str):

    db= await db_connect()
    mysql_cursor = db.cursor()
    mysql_cursor.execute("SELECT id_user FROM users WHERE password_hash = %s", ( credential))
    mysql_cursor.fetchall()
    if mysql_cursor.rowcount == 0:
        mysql_cursor.close()
        db.close()
        return ""
    else:
        user_id = mysql_cursor.fetchone()[0]
        mysql_cursor.close()
        db.close()
        return user_id

async def get_user_services(id_user:str):

    db= await db_connect()
    mysql_cursor = db.cursor()
    mysql_cursor.execute("SELECT * FROM services WHERE user_id = %s", (id_user))
    mysql_cursor.fetchall()
    if mysql_cursor.rowcount == 0:
        mysql_cursor.close()
        db.close()
        return ""
    else:
        user_id = mysql_cursor.fetchone()[0]
        mysql_cursor.close()
        db.close()
        return user_id
async def add_user_services(service:str,id_user:str):
    db= await db_connect()
    mysql_cursor = db.cursor()
    mysql_cursor.execute(" UPDATE services SET %s = TRUE WHERE user_id = %s", (service, id_user))
    mysql_cursor.close()
    db.commit()
    db.close()

    return f"{service} Updated successfully"
async def remove_user_services(service:str,id_user:str):
    db= await db_connect()
    mysql_cursor = db.cursor()
    mysql_cursor.execute(" UPDATE services SET %s = FALSE WHERE user_id = %s", (service, id_user))
    mysql_cursor.close()
    db.commit()
    db.close()

    return f"{service} Updated successfully"
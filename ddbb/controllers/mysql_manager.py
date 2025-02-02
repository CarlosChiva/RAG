import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os
async def db_connect():
    db = mysql.connector.connect(
    
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=3306,
        database=os.getenv("DB_DATABASE")

    )
    return db
async def checker_users(user_name:str,password:str):

    db= await db_connect()
    mysql_cursor = db.cursor()
    mysql_cursor.execute("SELECT username,password_hash FROM users WHERE username = %s AND password_hash = %s ;", (user_name, password))
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
    mysql_cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)  ;", (user_name, password))
    id_user = mysql_cursor.lastrowid
    mysql_cursor.execute("INSERT INTO services (user_id) VALUES (%s);", (id_user,))
    mysql_cursor.close()
    db.commit()
    db.close()

    return id_user
async def registrer_token(user_name:str,token:str): 
    db= await db_connect()

    mysql_cursor = db.cursor()
    mysql_cursor.execute("UPDATE users SET jwt_token = %s  WHERE username = %s ;", (token,user_name))
    mysql_cursor.close()
    db.commit()
    db.close()

    return "Token update successfully"
async def check_user_by_credential(credential:str):
    print(credential)
    # credential = credential.sub
    db= await db_connect()
    mysql_cursor = db.cursor()
    mysql_cursor.execute("SELECT id_user FROM users WHERE jwt_token = %s ;", (credential,))
    result=mysql_cursor.fetchone()
    if result:
        mysql_cursor.close()
        db.close()
        return str(result[0])
    
    else:
        mysql_cursor.close()
        db.close()
        return None

async def get_user_services(id_user:str):
    try:
        # Connect to database
        db = await db_connect()
        mysql_cursor = db.cursor()
        
        # Execute the query
        mysql_cursor.execute("SELECT chat, pdf, multimedia, excel FROM services WHERE user_id = %s", (id_user,))
        
        # Fetch all results
        services = mysql_cursor.fetchall()
        print("services....",services)
        if not services:
            # No services found, return empty string
            mysql_cursor.close()
            db.close()
            return []
        else:
            chat, pdf, multimedia, excel = services[0]
            services_result=[("chat",chat),("pdf",pdf),("multimedia",multimedia),("excel",excel)] 
            mysql_cursor.close()
            db.close()
            result=[]
            for service,enable in services_result:
                if enable:
                    result.append(service)
            if len(result)==0:
                return None        
            return result                
    except Exception as e:
        # Log the error (you might want to add logging here)
        print(f"Error fetching services: {e}")
        return None

async def get_user_services_available(id_user:str):
    try:
        # Connect to database
        db = await db_connect()
        mysql_cursor = db.cursor()
        
        # Execute the query
        mysql_cursor.execute("SELECT chat, pdf, multimedia, excel FROM services WHERE user_id = %s", (id_user,))
        
        # Fetch all results
        services = mysql_cursor.fetchall()
        print("services....",services)
        if not services:
            # No services found, return empty string
            mysql_cursor.close()
            db.close()
            return []
        else:
            chat, pdf, multimedia, excel = services[0]
            services_result=[("chat",chat),("pdf",pdf),("multimedia",multimedia),("excel",excel)] 
            mysql_cursor.close()
            db.close()
            result=[]
            for service,enable in services_result:
                if not enable:
                    result.append(service)
            if len(result)==0:
                return None        
            return result                
    except Exception as e:
        # Log the error (you might want to add logging here)
        print(f"Error fetching services: {e}")
        return None
async def add_user_services(service:str,id_user:str):
    db= await db_connect()
    mysql_cursor = db.cursor()
    query = "UPDATE services SET {} = TRUE WHERE user_id = {} ;".format(service, id_user)
    # values = (service, int(id_user))
    try:
        mysql_cursor.execute(query)#, values)
    except Exception as e:
        mysql_cursor.close()
        db.commit()
        db.close()
        print(f"Error adding service: {e}")
        return f"Error adding service: {e}"
    mysql_cursor.close()
    db.commit()
    db.close()

    return f"{service} Updated successfully"
async def remove_user_services(service:str,id_user:str):
    db= await db_connect()
    mysql_cursor = db.cursor()
    query = " UPDATE services SET {} = FALSE WHERE user_id = {} ;".format(service, id_user)

    mysql_cursor.execute(query)
    mysql_cursor.close()
    db.commit()
    db.close()

    return f"{service} Updated successfully"
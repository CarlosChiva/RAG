from .mysql_manager import checker_users, registrer_users
import os
async def check_user(user_name:str,password:str):
    return await checker_users(user_name=user_name,password=password)

async def registrer(user_name:str,password:str):

    return await registrer_users(user_name=user_name,password=password)
    

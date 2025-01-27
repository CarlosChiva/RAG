from .mysql_manager import checker_users, registrer_users, check_user_by_credential, get_user_services,add_user_services,remove_user_services
import os
async def check_user(user_name:str,password:str):
    return await checker_users(user_name=user_name,password=password)

async def registrer(user_name:str,password:str):

    return await registrer_users(user_name=user_name,password=password)
    
async def get_services(credential:str):
    id_user= await check_user_by_credential(credential=credential)
    services= await get_user_services(id_user=id_user)
    return services

async def add_services(credential:str,service:str):
    id_user= await check_user_by_credential(credential=credential)
    return await add_user_services(service=service,id_user=id_user)
    
async def remove_services(credential:str,service:str):
    id_user= await check_user_by_credential(credential=credential)
    return await remove_user_services(service=service,id_user=id_user)
    

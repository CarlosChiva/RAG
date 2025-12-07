from typing import Dict
from models.user import UserSession
from fastapi import  WebSocket

class ExcelAgent: # Change to querier who collect user_sessions
    """Clase singleton para gestionar el agente de Excel."""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.user_session:Dict[str,UserSession]={}
        
    async def query(self, question:str,
              file_path:str,
              credentials:str,
              websocket:WebSocket):
        """Realiza una consulta al agente."""
        
        if not credentials in self.user_session.keys():
            self.user_session[credentials]=UserSession(filename=file_path,
                                                       user_id=credentials
                                                       )
        self.user_session[credentials].query_agent(websocket=websocket,query=question)
        


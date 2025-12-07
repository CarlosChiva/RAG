from models.agent import Agent
import logging 
logging.basicConfig(level=logging.INFO)
class UserSession: # who create a agent specictly with file and agent
    _instance = None
    _initialized = False
    
    def __new__(cls, filename=None, user_id=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, filename=None, user_id=None):
        if not self._initialized:
            self.filename = filename
            self.user_id = user_id
            self.personal_agent = Agent(file_path=filename)
            self._initialized = True
            logging.info(f"Inizialize User session  {self.filename}")

    async def query_agent(self, websocket, query):
        config={"configurable":{"thread_id":self.user_id}}

        async for result in  self.personal_agent.agent.astream({"messages": query},config,stream_mode="values"):
            logging.info(f"result  {result["messages"]}")
            await websocket.send_json(result["messages"][-1].content)

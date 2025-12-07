from models.agent import Agent
class UserSession: # who create a agent specictly with file and agent
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, filename=None, user_id=None):
        if not self._initialized:
            if filename is not None and user_id is not None:
                self.filename = filename
                self.user_id = user_id
                self.personal_agent = Agent(file_path=filename)
                self._initialized = True
    
    async def query_agent(self, websocket, query):
        config={"configurable":{"thread_id":self.user_id}}

        async for result in  self.personal_agent.astream({"messages": query},config,stream_mode="values"):
            websocket.send_text(result[-1].content)

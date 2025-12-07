from agent import Agent
class UserSession: # who create a agent specictly with file and agent
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self,filename,user_id):
        if not self._initialized:
            filename=filename
            self.user_id=user_id
            self.personal_agent=Agent(file_path=filename)
    
    async def query_agent(self,websocket,query):
        config={"configurable":{"thread_id":self.user_id}}

        async for result in  self.personal_agent.astream({"messages": query},config,stream_mode="values"):
            websocket.send_text(result[-1].content)
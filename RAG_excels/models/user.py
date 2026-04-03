from models.agent import Agent
import logging 
logging.basicConfig(level=logging.INFO)
class UserSession: # who create a agent specictly with file and agent
    _instance = None
    _initialized = False
    thinking=False

    def __new__(cls, filename=None, user_id=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    async def send_message(self,websocket, msg_chunk):  

        if hasattr(msg_chunk, "tool_calls") and msg_chunk.tool_calls:
            logging.info(f"aaaaaaaaaaaaaa: {msg_chunk}")

            logging.info(f"🔧 Tool Call: {msg_chunk.tool_calls}")
            await websocket.send_json({
                "event": f"Using Tool {msg_chunk.tool_calls[0]['name']}",
            }) 

            
        reasoning_content = msg_chunk.additional_kwargs.get('reasoning_content')

        # if msg_chunk.additional_kwargs.reasoning_content:
        #     self.thinking=True
        #     return
            
            
        # elif not msg_chunk.additional_kwargs.reasoning_content:
        #     self.thinking=False
        #     return
        if reasoning_content:
            logging.info(f"{msg_chunk}")

            await websocket.send_json({
                "event": "response",
                "step":"thinking",
                "token": msg_chunk.content,                
            })
        if hasattr(msg_chunk, 'content') and msg_chunk.content:

                try:
                    await websocket.send_json({
                        "event": "response",
                        "step":"response",
                        "response":msg_chunk.content                                
                    })
                except Exception as e:
                    logging.error(f"Error sending websocket message: {e}")

    def __init__(self, filename=None, user_id=None):
        if not self._initialized:
            self.filename = filename
            self.user_id = user_id
            self.personal_agent = Agent(file_path=filename)
            self._initialized = True
            logging.info(f"Inizialize User session  {self.filename}")

    async def query_agent(self, websocket, query):
        config={"configurable":{"thread_id":self.user_id}}

        async for result,metadata in  self.personal_agent.agent.astream({"messages": query},config,stream_mode="messages"):
            logging.info(f"result  {result}")
           # logging.info(f"result  {result.content}")
            await self.send_message(websocket=websocket,
                                    msg_chunk=result
                                    )
        await websocket.send_json({"end":"__END__"})

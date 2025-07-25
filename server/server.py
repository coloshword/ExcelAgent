from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

#ChatMessage: Object Model for a chat message. A ChatMessage can be either an attachment (base64 str) or message (str)
class ChatMessage(BaseModel):
    message: str | None
    attachment: str | None

origins = [
    "*"
]    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


'''
Endpoint for chatting with the LLM in the backend 
'''
@app.post("/chat")
async def add_message(msg: ChatMessage):
    return {"received_message": msg.message, "received_attachment": msg.attachment}
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import auth

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

'''
Endpoint for logging in and getting a 
'''

## following a quick auth guide 
@app.get("/")
async def root():
    return {"message": "FASTAPI Auth demo"}

# this should be a protected endpoint 
@app.get("/protected")
async def protected_route(current_user: str = Depends(auth.authenticate_user)):
    return {"message": f"Hello {current_user}, this is a protected route!"}
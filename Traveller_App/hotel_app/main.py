# api.py
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union

from service import provide_stay_plan

app = FastAPI()

# --- JSON-RPC data models ---
class TextPart(BaseModel):
    type: str
    text: str

class Message(BaseModel):
    role: str
    parts: List[TextPart]

class Params(BaseModel):
    id: str
    message: Message

class JsonRPCRequest(BaseModel):
    jsonrpc: str
    id: Union[str, int]
    method: str
    params: Params

# --- Agent descriptor endpoint ---
@app.get("/.well-known/agent.json")
async def agent_info():
    return {
        "name": "Stay Advisor",
        "description": "Provide advise to users for choosing hotel stay",
        "capabilities": {
            "streaming": False, 
            "pushNotifications": False},
        "url": "http://localhost:9001",
        "skills": [
            {
                "id": "hotels", 
                "description": "Helps to identify suitable hotel stay"}
        ],
    }

# --- JSON-RPC handler ---
@app.post("/")
async def handle_rpc(payload: JsonRPCRequest):
    resp = {"jsonrpc": "2.0", "id": payload.id}

    if payload.method != "tasks/send":
        resp["error"] = {"code": -32601, "message": "Method not found"}
        return resp

    # Extract the user’s text
    user_text = "".join(
        p.text for p in payload.params.message.parts if p.type == "text"
    )

    # Call into the service layer
    messages = await provide_stay_plan(user_text)

    artifact = {
        "parts": [{"type": "data", "data": {"messages": messages}}],
        "index": 0
    }
    task_result = {
        "id": payload.params.id,
        "status": {
            "state": "completed",
            "timestamp": datetime.datetime.utcnow().isoformat()
        },
        "artifacts": [artifact],
        "history": []
    }
    resp["result"] = task_result
    return resp

# --- Standalone run ---
if __name__ == "__main__":
    import uvicorn
    #uvicorn.run("api:app", host="127.0.0.1", port=9001, reload=True)

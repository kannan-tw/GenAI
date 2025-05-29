# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union
import datetime
import json

from service import provide_flights_info

app = FastAPI()

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


@app.get("/.well-known/agent.json")
async def agent_info():
    return {
        "name": "Flight Advisor",
        "description": "Provide advise to user for flights selection",
        "capabilities": {
            "streaming": False, 
            "pushNotifications": False},
        "url": "http://localhost:9002",
        "skills": [
            {
                "id": "flights", 
                "name": "flights", 
                "description": "helps to identify suitable flight"}]
    }


@app.post("/")
async def handle_rpc(payload: JsonRPCRequest):
    response = {"jsonrpc": "2.0", "id": payload.id}

    if payload.method == "tasks/send":
        user_text = "".join([p.text for p in payload.params.message.parts if p.type == "text"])
        flights = await provide_flights_info(user_text)
        artifact = {
            "parts": [{"type": "data", "data": {"flights": flights}}],
            "index": 0
        }
        task_result = {
            "id": payload.params.id,
            "status": {"state": "completed", "timestamp": datetime.datetime.utcnow().isoformat()},
            "artifacts": [artifact],
            "history": []
        }
        response["result"] = task_result
        print(response)
        return response
    else:
        response["error"] = {"code": -32601, "message": "Method not found"}
        return response


if __name__ == "__main__":
    import uvicorn
    #uvicorn.run("main:app", host="127.0.0.1", port=9002, reload=True)

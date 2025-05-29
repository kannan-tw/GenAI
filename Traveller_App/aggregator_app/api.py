# api.py
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union

from service import provide_plan  # your async LangGraph runner

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
    """
    Agent Card for A2A discovery.
    """
    return {
        "name": "TravelPlanAgent",
        "description": "Generates travel itineraries using LangGraph",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False
        },
        "url": "http://localhost:8000",  # base URL of this agent
        "skills": [
            {
                "id": "generate_travel_plan",
                "description": "Produce a full travel plan from user prompt"
            }
        ],
    }

# --- JSON-RPC handler ---
@app.post("/")
async def handle_rpc(payload: JsonRPCRequest):
    resp = {"jsonrpc": "2.0", "id": payload.id}

    # Only support tasks/send
    if payload.method != "tasks/send":
        resp["error"] = {"code": -32601, "message": "Method not found"}
        return resp

    # Extract user text from parts
    user_text = "".join(
        p.text for p in payload.params.message.parts if p.type == "text"
    )

    # Call the service layer (LangGraph workflow)
    # Note: include checkpoint fields so MemorySaver won’t error
    result_state = await provide_plan(  # returns the final state dict
        prompt=user_text
    )

    # Package the result_state under artifacts
    artifact = {
        "parts": [
            {
                "type": "data",
                "data": result_state
            }
        ],
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
    #uvicorn.run("api:app", host="127.0.0.0", port=8001, reload=True)

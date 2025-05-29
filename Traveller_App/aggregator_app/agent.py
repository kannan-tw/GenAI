from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage, BaseMessage
import httpx
import json
from langgraph.checkpoint.memory import MemorySaver

from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from typing import Annotated

model_name = "gpt-4o-mini" 


User_Prompt =  """
You are a smart travel planning assistant.

**Step 1: Understand Intent**
Determine whether the user wants:
- Flight options only
- Hotel options only
- A complete travel plan (flights + stay + itinerary)

Ask this clearly at the start if the intent is not obvious.

---

**Step 2: Collect Required Info Based on Intent**

🔹 **For Flights:**
- Origin
- Destination
- Travel start date (and return date, if round-trip)
- Class or airline preference (optional)

🔹 **For Hotels:**
- Destination
- Check-in and check-out dates
- Hotel preference (type, budget, etc.) — optional

🔹 **For Full Travel Plan:**
- Origin
- Destination
- Travel start and end dates
- Flight preference (optional)
- Hotel preference (optional)
- Budget (optional)

---

**Smart Behavior:**
- Infer return date if duration is mentioned (e.g., "one week trip")
- For multi-day trips, assume accommodation may be needed
- Use distance and geography to infer if flights are likely needed
- Only ask for missing or unclear fields
- Avoid repeating previously answered questions
- Summarize all gathered information and ask for confirmation
- Proceed only after the user confirms all details

---

**Interaction Flow:**
1. Ask what kind of travel help the user needs (if not already clear)
2. Collect required inputs based on that intent
3. Confirm collected data with a summary
4. Proceed to show flight/hotel options or generate full travel plan

Be concise, friendly, and avoid unnecessary questions.
"""


def get_user_info(messages):
    if not isinstance(messages, list):
        messages = [messages]
    return [SystemMessage(content=User_Prompt)] + messages

class TravelInfo(BaseModel):
    """Instructions on how to prompt the LLM."""
    origin: str
    destination: str
    travel_date: str
    travel_end: str
    budget: str

#llm = ChatOpenAI(model=model_name, temperature=0, max_retries=1)

def travel_agent(state):
    print("travel_agent")
    messages = get_user_info(state["messages"])
    print("travel_agent 1 \n", messages)
    print("travel_agent -1 \n", messages[-1])
    print("travel_agent 0 \n", messages[0]) 
    llm = ChatOpenAI(model=model_name, temperature=0, max_retries=1)
    try:
        print("travel_agent 2")
        llm_with_tool = llm.bind_tools([TravelInfo])
        print("travel_agent 3")
        response = llm_with_tool.invoke(messages)
        print("travel_agent : ", response)
        return {
        "messages": [response]
        }
    except Exception as e:
        print(f"{e}")
        return e


def conclude_conversation(state):
    response = {
        "messages": [
            ToolMessage(
                content="Clarified and proceeding further",
                tool_call_id=state["messages"][-1].tool_calls[0]["id"],
            )
        ]
    }
    print("conclude_conversation : ", response)
    return response

def is_clarified(state):
    messages = state["messages"] 
    if isinstance(messages[-1], AIMessage) and messages[-1].tool_calls:

        return "yes" #"conclude_conversation"
    else:
        return "no" #"continue_conversation"
    

    
Intent_Prompt = "Generate user intent based on {reqs}"

def get_user_messages(messages: list):
    tool_call = None
    other_msgs = []
    
    for m in messages:
        if isinstance(m, AIMessage) and m.tool_calls:
            tool_call = m.tool_calls[0]["args"]
            if hasattr(m, 'tool_calls'):
                delattr(m, 'tool_calls')
        elif isinstance(m, ToolMessage):
            continue
        elif tool_call is not None:
            other_msgs.append(m)
   
    return[
        SystemMessage(content=Intent_Prompt.format(reqs=tool_call)),
        
        ] + other_msgs  

def generate_user_intent(state):
    messages = get_user_messages(state["messages"])
    llm = ChatOpenAI(model=model_name, temperature=0, max_retries=1)
    response = llm.invoke(messages)
    print("generate_user_intent : ", response)
    return {
        "user_intent": response
    }

def agent_cards():
    urls = [
        "http://localhost:9001/.well-known/agent.json",
        "http://localhost:9002/.well-known/agent.json"
    ]
    
    responses = []

    for url in urls:
        try:
            resp = httpx.get(url, timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                responses.append(data)
            else:
                print(f"Failed to fetch from {url}, status code: {resp.status_code}")
        except Exception as e:
            print(f"Error calling {url}: {e}")
    
    #print("All responses:", responses)
    return responses

Classify_Prompt = """Help to choose right agent from {agent_list} for given user query. 
- Repond with Flights agent array from agent list if user is enquiring about flight relation information
- Repond with <Hotels agent array> from agent list if user is enquiring about stay/hotels related information
- Repond with <Flights and Hotel agents array> from agent list if user is enquiring about travel or flight and stay related
Respond json object only.
Don't make wild guess"""

def get_agent_info(messages):
    agents = agent_cards()
    return [SystemMessage(content=Classify_Prompt.format(agent_list=agents))] + messages

def discovery_agent(state):
    print("discovery_agent")
    messages = get_agent_info(state["user_intent"])
    print("discovery_agent :", messages)
    print("discovery_agent - user_intent:", state["user_intent"])
    llm = ChatOpenAI(model=model_name, temperature=0, max_retries=1)
    response = llm.invoke(messages)
    print("discovery_agent : ", response)
    return {"agent_card": response}


async def call_remote_agent(agent, user_query):
    payload = {
        "jsonrpc": "2.0",
        "id": "101",
        "method": "tasks/send",
        "params": {
            "id": "1011",
            "message": {
                "role": "user",
                "parts": [
                    {
                        "type": "text",
                        "text": user_query
                    }
                ]
            }
        }
    }

    async with httpx.AsyncClient(timeout=120) as client:
        try:
            response = await client.post(agent, json=payload)
            
            print("Agent response :", response.json())
            return response.json()
            
        except Exception as e:
            print(e)
            return e
            
async def collection_agent(state):
    print("collection_agent")
    agent_card = state['agent_card'][-1].content
    user_query = state['user_intent'][-1].content
    print("collection_agent - agent card : ", agent_card)
    print("collection_agent - user_query : ", user_query)
    
    if not agent_card.strip():
        print("Error: agent_card is empty.")
        return
    else:
        print(agent_card)
    
    content = agent_card.strip()

    # Remove triple backtick formatting if present
    if content.startswith("```json"):
        content = content[7:]  # remove ```json
    if content.endswith("```"):
        content = content[:-3]  # remove `
    agents = json.loads(content)
    print("Agents :", agents)
    # Access elements
    print("\n*** Discovered Agents ***\n")
    agent_responses = []
    for agent in agents:
        '''print("Name:", agent["name"])
        print("Description:", agent["description"])
        print("URL:", agent["url"])
        print("Skills:")
        for skill in agent["skills"]:
            print(f"  - {skill['id']}: {skill['description']}")
        print("\n")'''
        
        print("URL:", agent["url"])
        print("User Intent   :", user_query)
        agent_response = await call_remote_agent (agent["url"], user_query)
        agent_responses.append ({
                "name" : agent["name"],
                "response" : agent_response
        })


    print("agent_responses: ", agent_responses)
    return {
        "messages": [
            {
                "role": "assistant",
                "content": f"{json.dumps(agent_responses, indent=2)}"
            }
        ]
    }


Aggregate_Prompt = "Generate Travel Plan for provided {details}"
def get_aggregate_info(messages):
    return [SystemMessage(content=Aggregate_Prompt.format(details=messages))]


def aggregate_agent(state):
    agent_responses = state['messages'][-1].content
    messages = get_aggregate_info(agent_responses)
    llm = ChatOpenAI(model=model_name, temperature=0, max_retries=1)
    response = llm.invoke(messages)
    print("Final Plan :", response)

    return {"messages": response}




class State(TypedDict):
    messages: Annotated[list, add_messages]
    initial_query: Annotated[list, add_messages]
    user_intent: Annotated[list, add_messages]
    agent_card: Annotated[list, add_messages]
    max_iteration: int
    iteration: int
    

def build_aggregator():
    memory = MemorySaver()
    workflow = StateGraph(State)
    

    workflow.add_edge(START, "Planner")
    workflow.add_node("Planner", travel_agent)
    workflow.add_node("generate_user_intent", generate_user_intent)
    workflow.add_node("Discoverer", discovery_agent)
    workflow.add_node("Collector", collection_agent)
    workflow.add_node("Aggregator", aggregate_agent)
    workflow.add_node("conclude_conversation", conclude_conversation)

    workflow.add_conditional_edges(
    "Planner", 
    is_clarified, 
    {"yes": "conclude_conversation",  "no": END})
    workflow.add_edge("conclude_conversation", "generate_user_intent")
    workflow.add_edge("generate_user_intent", "Discoverer")
    workflow.add_edge("Discoverer", "Collector")
    workflow.add_edge("Collector", "Aggregator")
    workflow.add_edge("Aggregator", END)

    graph = workflow.compile(checkpointer=memory) 
    return graph

'''graph = build_aggregator()
print(graph)'''
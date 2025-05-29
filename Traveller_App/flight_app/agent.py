
import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")


'''def external_approval_tool(content):
    print("**** waiting for approval *****", content)
    return "rejected"'''

def flight_advisor_agent():

    #approval_tool = FunctionTool(func=external_approval_tool)

    # Agent that prepares the request
    """validate_agent = LlmAgent(
        name="validate_agent",
        model=LiteLlm("openai/gpt-4o-mini"),
        description="Help to validate whether user provided all information",
        instruction='''Ask user if either origin or destination is missing''',
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
        output_key="validate",
    )"""

    extract_agent = LlmAgent(
        name="extract_agent",
        model=LiteLlm("openai/gpt-4o-mini"),
        description="Help to infer origin, destination and class from user query",
        instruction='''Infer origin, destination and class details from user query.
        Return the response as a JSON object formatted like this:
        {
            origin: <where flight departure>
            destination: <where flight arrive>
            class: <default with economy unless user prefer business class>
        }''',
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
        output_key="request",
    )

    search_agent = LlmAgent(
        name="search_agent",
        model=LiteLlm("openai/gpt-4o-mini"),
        description="Help users find best flight deals",
        instruction='''Read state ['request'] and generate Best 3 search results for given resutls.
        Return the response as a JSON object formatted like this:
        {{
            {{"flights": [
                {
                "flight_number":"Unique identifier for the flight, like BA123, AA31, etc."),
                "departure": {{
                    "city_name": "Name of the departure city",
                    "timestamp": ("ISO 8601 departure date and time"),
                }},
                "arrival": {{
                    "city_name":"Name of the arrival city",
                    "timestamp": "ISO 8601 arrival date and time",
                }},
                "airlines": [
                    "Airline names, e.g., American Airlines, Emirates"
                ],
                "price_in_usd": "Integer - Flight price in US dollars",
                "number_of_stops": "Integer - indicating the number of stops during the flight",
                }
            ]}}
        }}''',
        disallow_transfer_to_parent=True,
        disallow_transfer_to_peers=True,
        output_key="flight",
    )

    flight_agent = Agent(
        model=LiteLlm("openai/gpt-4o-mini"),
        description="""Helps users with flight details""",
        name="flight_agent",
        
        instruction='''Choose the one of the BEST flight option from state ['flight'] 
                and "provide flights info" to user. 
                Note:Don't send all options to user.''',
        tools=[
            #AgentTool(agent=validate_agent),
            AgentTool(agent=extract_agent),
            AgentTool(agent=search_agent),
        ],
    )

    return flight_agent
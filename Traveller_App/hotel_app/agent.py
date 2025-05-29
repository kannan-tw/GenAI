# agents.py
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# ensure your OPENAI_API_KEY is set in the environment
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

def stay_advisor_agent():
    """
    Instantiate and return the list of AssistantAgents
    in the order they should speak.
    """
    client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    validation_agent = AssistantAgent(
        "validation_agent",
        model_client=client,
        description="Validate incoming request",
        system_message='''You are tasked to validate user request
        to ensure whether user have provided desination details, 
        Otherwise you must say "TERMINATE" with reason of termination. '''
    )

    extract_agent = AssistantAgent(
        "extract_agent",
        model_client=client,
        description="Help to infer destination from user query",
        system_message='''Infer destination from user query.
        Return the response as a JSON object formatted like this:
        {
            destination: <city name>
        }
        Don't make assumption'''
    )

    search_agent = AssistantAgent(
        "search_agent",
        model_client=client,
        description="Help users find best hotel at destination",
        system_message='''Generate TOP 3 hotel stay details only.
        Return the response as a JSON object formatted like this:
        {{
            {{"hotels": [
                {
                "hotel": "hotel names, "
                "price_in_usd": "US dollars",
                "address": "location of the hotel",
                }
            ]}}
        }}'''
    )

    stay_summary_agent = AssistantAgent(
        "stay_summary_agent",
        model_client=client,
        description="Compile final stay plan",
        system_message=(
            "You are an assistant that aggregates all advice into a final plan. "
            "When done, TERMINATE it. Don't respond terminate wording at end"
        )
    )

    return [extract_agent, search_agent, stay_summary_agent]

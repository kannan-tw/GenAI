# service.py
import datetime
import asyncio
from typing import List, Dict

from agent import stay_advisor_agent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination

async def provide_stay_plan(prompt: str, max_messages: int = 5) -> List[Dict]:
    """
    Run the round-robin group chat on the user prompt,
    collect up to `max_messages` messages, then return them.
    """
    agents = stay_advisor_agent()
    msg_termination = MaxMessageTermination(max_messages=max_messages)
    text_termination = TextMentionTermination("TERMINATE")
    combined_termination = msg_termination | text_termination
    group_chat = RoundRobinGroupChat(agents, termination_condition=combined_termination)

    messages = []
    import re
    async for msg in group_chat.run_stream(task=prompt):
        # Each msg is a dict: {"role": ..., "content": ...}
        #print(msg.source + ":" + msg.content)
        
        print("\n\n")
        if hasattr(msg, 'source'):
            print("history :", msg.content)
        else:
            final_msg = msg.messages[-1]
            print("final message : ", final_msg)
            messages.append(final_msg)

    # Clean up the underlying model client
    # All agents share the same client instance under the hood
    #await agents[0].model_client.close()

    return messages

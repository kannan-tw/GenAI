# service.py
import asyncio
from agent import build_aggregator

_graph = build_aggregator()
config = {"configurable": {"thread_id": 19}}
async def provide_plan(prompt: str) -> str:
    """
    Runs the LangGraph StateGraph for the given prompt
    and returns the final 'plan' text.
    """
    # Initialize state
    
    initial_state = {
        "messages": prompt, 
        #"thread_id": 11 
        }
    # Execute the graph (sync or async)
    result_state = await _graph.ainvoke(initial_state, config=config)  # :contentReference[oaicite:3]{index=3}
    print("Response from LangGraph :", result_state)
    return result_state

'''if __name__ == "__main__":
    result = asyncio.run(provide_plan("how are you doing?"))
    print(result)'''
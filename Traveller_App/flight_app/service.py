# services/classification_service.py
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.adk.memory import InMemoryMemoryService
from google.genai import types
from agent import flight_advisor_agent
import json
#from google.adk.sessions import Message 

session_service = InMemorySessionService()
memory_service = InMemoryMemoryService() 
agent = flight_advisor_agent()
USER_ID = "user_classify"
SESSION_ID = "session_classify"
APP_NAME = "flight_app"

runner = Runner(
    agent=agent, 
    app_name=APP_NAME, 
    session_service=session_service,
    memory_service=memory_service
    )

session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
async def provide_flights_info(text: str):
    
    #print(f"Initial state: {session.state}")
    content = types.Content(role="user", parts=[types.Part(text=text)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            
            try:
                
                parsed = event.content.parts[0].text.strip()#json.loads(event.content.parts[0].text.strip())
                '''print("result :", parsed)
                updated_session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
                print("state :", updated_session.state)
                print("last_update_time :", updated_session.last_update_time)
                print("user_id :", updated_session.user_id)'''
                
                return parsed #.get("content", "Unknown")
            
            except Exception:
                return event.content.parts[0].text.strip()


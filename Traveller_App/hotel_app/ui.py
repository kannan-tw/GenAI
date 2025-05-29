# ui/app.py
import streamlit as st
import requests
import uuid
import os

# —————— Streamlit page setup ——————
st.set_page_config(page_title="🧳 Accomodation Assistant")
st.title("🧳 Accomodation Assistant")

# —————— Session state ——————
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# —————— Helper to call JSON-RPC API ——————
API_URL = os.getenv("STAY_ADVISOR_API_URL", "http://localhost:9002/")

def send_to_backend(user_text: str):
    """Send the user's prompt to the FastAPI JSON-RPC endpoint and return the list of messages."""
    rpc_payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tasks/send",
        "params": {
            "id": str(uuid.uuid4()),
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": user_text}]
            }
        }
    }
    try:
        resp = requests.post(API_URL, json=rpc_payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # Extract the sequence of messages from the artifact
        return data["result"]["artifacts"][0]["parts"][0]["data"]["messages"]
    except Exception as e:
        st.error(f"API request failed: {e}")
        return []

# —————— User input ——————
user_input = st.chat_input("Ask me...")

if user_input:
    # show user message immediately
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        # call the backend
        with st.spinner("Thinking…"): 
        # Call the backend and retrieve the agent’s messages
            agent_messages = send_to_backend(user_input)
        
        '''if isinstance(agent_messages, list):
            final_msg = agent_messages[-2] if agent_messages else {}
        elif isinstance(agent_messages, dict):
            final_msg = agent_messages
        else:
            final_msg = {}'''

        
        #content = final_msg.get("content", "😕 Sorry, no content received.")
        st.session_state.chat_history.append({"role": "user", "text": user_input})

        st.session_state.chat_history.append({"role": "system", "text": agent_messages})

        

# —————— Render chat ——————
for entry in st.session_state.chat_history:
    print(entry)
    with st.chat_message(entry["role"]):
            st.markdown(entry["text"])

# ui/app.py
import streamlit as st
import requests
import uuid
import os

# —————— Streamlit page setup ——————
st.set_page_config(page_title="🧳 Travel Advisor Chatbot")
st.title("🧳 Traveller Guide")

# —————— Session state ——————
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# —————— Helper to call JSON-RPC API ——————
API_URL = os.getenv("STAY_ADVISOR_API_URL", "http://localhost:9003/")

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
        resp = requests.post(API_URL, json=rpc_payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        # Safely navigate into artifacts → parts → data → messages
        return (
            data
            .get("result", {})
            .get("artifacts", [{}])[0]
            .get("parts", [{}])[0]
            .get("data", {})
            .get("messages", [])
        )
    except Exception as e:
        st.error(f"API request failed: {e}")
        return []
    
# —————— Render existing chat history ——————
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["text"])

# —————— Handle new user input ——————
#if not st.session_state.is_loading:
user_input = st.chat_input("Ask me to plan your trip…")
#else:
#    user_input = None

if user_input:
    # Show and store the user message
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.spinner("Thinking…"): 
    # Call the backend and retrieve the agent’s messages
        agent_messages = send_to_backend(user_input)
    print("actual response: ", agent_messages)

    if isinstance(agent_messages, list):
        final_msg = agent_messages[-1] if agent_messages else {}
    elif isinstance(agent_messages, dict):
        final_msg = agent_messages
    else:
        final_msg = {}

    # Now safely extract content
    content = final_msg.get("content", "😕 Sorry, no content received.")
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    st.session_state.chat_history.append({"role": "system", "text": content})


# —————— Render chat ——————
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["text"])

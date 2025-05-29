# ui/app.py
import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Flight Assistant")
st.title("🤖 Flight Assistant")

# Initialize session state for messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box for user message
user_input = st.chat_input("Type your helpdesk question here...")

# Handle user input
if user_input:
    # Display user message
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Prepare JSON-RPC payload
    rpc_payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tasks/send",
        "params": {
            "id": str(uuid.uuid4()),
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": user_input}]
            }
        }
    }

    try:
        # Make POST request to FastAPI
        response = requests.post("http://localhost:9001/", json=rpc_payload)
        if response.status_code == 200:
            data = response.json()
            flights = data["result"]["artifacts"][0]["parts"][0]["data"]["flights"]
            bot_reply = f"🗂️ ** {flights} **"
        else:
            bot_reply = f"❌ {response}. Please try again."
    except Exception as e:
        bot_reply = f"❌ Request failed: {e}"

    # Append bot response to history
    st.session_state.chat_history.append({"role": "bot", "text": bot_reply})

# Display full chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

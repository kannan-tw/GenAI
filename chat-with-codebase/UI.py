import streamlit as st
import requests

# Set up Streamlit layout



#st.set_page_config(layout="wide")
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"  # Options: "auto", "expanded", "collapsed"
)
st.header("AskCode")
st.markdown("**A simple interface to chat with code**")

# Initialize session state for chat history and settings
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_settings" not in st.session_state:
    st.session_state.api_settings = {
        "code_dir": "",
        "allowed_extn": "",
        "code_summary": "",
        "file_location":""
    }

# Sidebar for another API invocation settings
with st.sidebar:
    st.header("API Coniguration")
    st.subheader("Configuration for Code Parsing")
    st.session_state.api_settings["code_dir"] = st.text_input(
        "Code Directory", value=st.session_state.api_settings["code_dir"], placeholder="e.g., /path/to/code"
    )
    st.session_state.api_settings["allowed_extn"] = st.text_input(
        "Allowed Extensions", value=st.session_state.api_settings["allowed_extn"], placeholder="e.g., .py, .js"
    )
    st.session_state.api_settings["code_summary"] = st.text_input(
        "Code Summary", value=st.session_state.api_settings["code_summary"], placeholder="Summary of the code"
    )

    # Button to invoke the API
    if st.button("Parse"):
        # API URL for the invocation
        API_URL = "http://127.0.0.1:8000/code_parser_with_summary"

        # Prepare payload for the API
        payload = {
            "code_dir": st.session_state.api_settings["code_dir"],
            "allowed_extn": st.session_state.api_settings["allowed_extn"],
            "code_summary": st.session_state.api_settings["code_summary"],
        }

        try:
            # Make API request
            with st.spinner("Parsing..."):
                response = requests.post(API_URL, json=payload, timeout=60)
            
                if response.status_code == 200:
                    st.success("Success\n" + response.text)
                    
                    #st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}. Could not complete the request.")
                    st.write(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")
    
    # Section for API 2
    st.subheader("Configuration for ingesting data")

    st.session_state.api_settings["file_location"] = st.text_input(
        "File Location", value=st.session_state.api_settings["file_location"], placeholder="e.g., file name"
    )

    if st.button("Ingest Data"):
        API_URL_2 = "http://127.0.0.1:8000/ingest_data"
        payload = {
           "file_location":  st.session_state.api_settings["file_location"]
        }
        
        try:
            with st.spinner("Loading..."):
                
                response = requests.post(API_URL_2, json=payload, timeout=60)
                print(response.text)
                if response.status_code == 200:
                    st.success("Success! " + response.text)
                    #st.json(response.json())
                else:
                    st.error(f"Error: {response.status_code}. Could not complete the request.")
                    st.write(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")

# Chat interface below


# Function to send query to backend
def send_query_to_api(query):
    ASK_URL = "http://127.0.0.1:8000/ask_code"
    try:
        response = requests.post(ASK_URL, json={"USER_INPUT": query}, ) #timeout=10
        
        # Handle non-JSON responses gracefully
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            return f"Error: {response.status_code}. Could not retrieve a valid response."
    
    except ValueError:
        return f"Non-JSON response: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to backend: {e}"


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input with `st.chat_input`
if user_input := st.chat_input("Ask me something"):
    # Display user message in chat message container
    st.chat_message("user").markdown(user_input)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display a spinner while waiting for the response
    with st.spinner("Thinking..."):
        bot_response = send_query_to_api(user_input)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

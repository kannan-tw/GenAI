import streamlit as st
import requests

API_URL = "http://localhost:8001/tasks"

def fetch_tasks():
    response = requests.get(API_URL)
    return response.json()

def add_task(title, description=""):
    response = requests.post(API_URL, params={"title": title, "description": description})
    return response.json()

def update_task(task_id, title, description=""):
    response = requests.put(f"{API_URL}/{task_id}", params={"title": title, "description": description})
    return response.json()

st.title("Daily Tasks App")

# Add new task
with st.form("add_task_form"):
    new_title = st.text_input("Task Title")
    new_description = st.text_area("Task Description")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        if new_title:
            add_task(new_title, new_description)
            st.success("Task added!")
            st.rerun()
        else:
            st.error("Please enter a task title.")


st.subheader("Task List")
tasks = fetch_tasks()
if not tasks:
    st.info("No tasks found.")
else:
    for t in tasks:
        with st.expander(f"Task: {t['title']} (ID: {t['id']})"):
            st.markdown(f"**Task ID:** `{t['id']}`")
            edit_title = st.text_input(f"Edit Title {t['id']}", value=t['title'], key=f"title_{t['id']}")
            edit_description = st.text_area(f"Edit Description {t['id']}", value=t.get('description', ''), key=f"desc_{t['id']}")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.text("ID (not editable):")
            with col2:
                st.code(str(t['id']), language="text")
            if st.button("Update", key=f"update_{t['id']}"):
                update_task(t['id'], edit_title, edit_description)
                st.success("Task updated!")
                st.experimental_rerun()
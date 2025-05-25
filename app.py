import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="OpenRouter Chatbot", page_icon="🤖")
st.title("🤖 Chat with OpenRouter GPT")
st.markdown("##### Made with ❤️ by **Areeb Malik**")

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = os.getenv("OPENROUTER_API_KEY")

def get_openrouter_response(message):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "google/gemini-2.5-flash-preview-05-20",
        "messages": [{"role": "user", "content": message}],
    }

    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    res_json = res.json()

    print(res_json)  # Debug: Show response in terminal

    if "choices" in res_json:
        return res_json["choices"][0]["message"]["content"]
    else:
        return "❌ Error from OpenRouter: " + str(res_json)

# Chat UI
for chat in st.session_state.messages:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        reply = get_openrouter_response(user_input)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

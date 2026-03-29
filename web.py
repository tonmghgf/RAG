import streamlit as st
import requests

backend_url = "http://127.0.0.1:6066/chat"
st.set_page_config(page_title="ChatBot", page_icon="🤖", layout="centered")
st.title("🤖 聊天机器人")

def clear_chat_history():
    st.session_state.history = []

with st.sidebar:
    st.title("设置")
    sys_prompt = st.text_input("系统提示词", value="你是一个有用的助手")
    history_len = st.slider("历史轮数", 1, 10, 1)
    temperature = st.slider("temperature", 0.01, 2.0, 0.7)
    top_p = st.slider("top_p", 0.01, 1.0, 0.8)
    max_tokens = st.slider("max_tokens", 256, 4096, 1024)
    stream = st.checkbox("流式输出", value=True)
    st.button("清空历史", on_click=clear_chat_history)

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("来聊天吧~"):
    with st.chat_message("user"):
        st.markdown(prompt)

    data = {
        "query": prompt,
        "sys_prompt": sys_prompt,
        "history": st.session_state.history,
        "history_len": history_len,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }

    response = requests.post(backend_url, json=data, stream=True)
    if response.status_code == 200:
        chunks = ""
        assistant = st.chat_message("assistant")
        placeholder = assistant.empty()

        for chunk in response.iter_content(decode_unicode=True):
            chunks += chunk
            placeholder.markdown(chunks)

        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": chunks})
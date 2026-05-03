import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    base_url="https://api.deepseek.com/v1",
)

st.set_page_config(page_title="我的智能客服", page_icon="🤖")
st.title("🤖 智能客服机器人")
st.caption("我可以回答产品相关问题，试试问我吧！")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一位专业、友好的智能客服助手，回答要简洁准确。"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("请输入您的问题..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages,
            stream=True,
            temperature=0.7
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.header("设置")
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = [
            {"role": "system", "content": "你是一位专业、友好的智能客服助手，回答要简洁准确。"}
        ]
        st.rerun()
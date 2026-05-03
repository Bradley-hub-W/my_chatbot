import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    base_url="https://api.deepseek.com/v1",
    timeout=30,
    max_retries=3,
)

st.set_page_config(page_title="我的智能客服",page_icon="🤖")
st.title("🤖 智能客服机器人")
st.caption("我可以回答产品相关问题，试试问我吧！")

if "conversations" not in st.session_state:
    st.session_state.cnversations = []
if "current_conv_id" not in st.session_state:
    st.session_state.current_conv_id = None

current_conv = get_current_conversation()
chat_messages = current_conv["messages"] 

for msg in chat_messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("请输入您的问题..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    chat_messages.append({"role":"user","content":prompt})

    if len(chat_messages) == 2:
        current_conv["title"] = prompt[:20]  + ("..." if len(prompt) > 20 else "")

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages,
            stream=True,
            temperature=0.2,       # 客服专用：稳定、准确
            max_tokens=1024,      # 不长不短
            frequency_penalty=0.2,# 减少重复
            presence_penalty=0.1, # 更自然
            stop=["。"],          # 遇到句号可自动停（可选）
        )
        response = st.write_stream(stream)
    chat_messages.append({"role":"assistant","content":response})



def create_new_conversation():
    new_id = len(st.session_state.conversations)
    new_conv = {
        "id": new_id,
        "title": "新对话",
        messages: [
            {"role":"system", "content":"你是一位专业、友好的智能客服助手，回答要简洁准确。"}
        ]
    }
    st.session_state.conversations.append(new_conv)
    st.session_state.current_conv_id = new_id
    st.rerun()

def get_current_conversation():
    if st.session_state.current_conv_id is None:
        return create_new_conversation()
    return next(
        conv for conv in st.session_state.conversations 
        if conv["id"] == st.session_state.current_conv_id)

with st.sidebar:
    st.header("设置")
    if st.button("+ 新对话"):
        create_new_conversation()

    st.subheader("历史对话")
    for conv in st.session_state.conversations:
        title = conv["title"]
        if st.button(f"{title[:20]}", use_container_width=True):
            st.session_state.current_conv_id = conv["id"]
            st.session_state.messages = conv["messages"]
            st.rerun()

    if st.button("🗑️ 清空所有对话"):
        st.session_state.conversations = []
        st.session_state.current_conv_id = None
        st.session_state.messages = [
            {"role":"system", "content":"你是一位专业、友好的智能客服助手，回答要简洁准确。"}
        ]
        st.rerun()
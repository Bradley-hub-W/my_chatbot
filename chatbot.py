import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 初始化 OpenAI 客户端（支持自定义 base_url）
client = OpenAI(
    api_key=os.getenv("sk-b4920569d21a43729abc82b4e6682fa1"),
    base_url=os.getenv("https://api.deepseek.com/v1"), 
)

# 页面标题和图标
st.set_page_config(page_title="我的智能客服", page_icon="🤖")
st.title("🤖 智能客服机器人")
st.caption("我可以回答产品相关问题，试试问我吧！")

# 初始化聊天记录（存入 session_state）
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一位专业、友好的智能客服助手，回答要简洁准确。"}
    ]

# 显示历史消息
for msg in st.session_state.messages:
    if msg["role"] != "system":  # 不显示系统提示
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 接收用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用大模型 API
    with st.chat_message("assistant"):
        # 使用流式输出（打字机效果）
        stream = client.chat.completions.create(
            # model=os.getenv("MODEL_NAME", "gpt-3.5-turbo"),  # 或 deepseek-chat
            model="deepseek-chat",
            messages=st.session_state.messages,
            stream=True,
            temperature=0.7
        )
        # 收集完整回复
        response = st.write_stream(stream)  # Streamlit 内置支持流式
    st.session_state.messages.append({"role": "assistant", "content": response})

# 侧边栏：清空对话按钮
with st.sidebar:
    st.header("设置")
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = [
            {"role": "system", "content": "你是一位专业、友好的智能客服助手，回答要简洁准确。"}
        ]
        st.rerun()
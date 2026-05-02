from openai import OpenAI

client = OpenAI(
    api_key="sk-b4920569d21a43729abc82b4e6682fa1",
    base_url="https://api.deepseek.com/v1",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}],
    stream=False,
)

print(response.choices[0].message.content)
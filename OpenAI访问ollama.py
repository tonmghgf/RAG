# 先安装：pip install openai==1.71.0
from openai import OpenAI

# 连接本地 Ollama 服务
client = OpenAI(
    api_key="ollama",  # 随便填，本地不需要真实key
    base_url="http://localhost:11434/v1"  # 固定地址
)

# 流式请求本地模型
response = client.chat.completions.create(
    model="qwen2.5:0.5b",
    messages=[
        {"role": "system", "content": "你是一个乐于助人的助手。"},
        {"role": "user", "content": "你好"}
    ],
    max_tokens=512,
    temperature=0.7,
    stream=True  # 流式输出
)

# 逐字打印结果（干净不换行）
for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
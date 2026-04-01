import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1. 连接本地 Ollama 模型
chat_model = ChatOpenAI(
    openai_api_key="ollama",
    base_url="http://localhost:11434/v1",
    model="qwen2.5:0.5b"
)

# 2. 提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个乐于助人的助手"),
    ("human", "{user_question}")
])

# 3. 组装链（LCEL 写法，官方推荐）
chain = prompt | chat_model

# 4. 运行
response = chain.invoke({"user_question": "你好"})
print(response.content)
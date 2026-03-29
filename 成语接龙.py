from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 1. 连接本地 Ollama 模型
llm = ChatOpenAI(
    openai_api_key="ollama",
    base_url="http://localhost:11434/v1",
    model="qwen2.5:0.5b"
)

# 2. 成语接龙提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个成语接龙高手。只回复成语，不要多余解释。根据用户给出的成语，用最后一个字接下一个成语。"),
    ("user", "{input_idiom}")
])

# 3. 构建 LCEL 链
chain = prompt | llm | StrOutputParser()

# 4. 成语接龙循环
print("=== 成语接龙游戏 ===")
print("输入“退出”结束游戏\n")

current = input("请输入第一个成语：")

while True:
    if current in ["退出", "exit", "结束"]:
        print("游戏结束！")
        break

    # AI 接成语
    ai_idiom = chain.invoke({"input_idiom": current})
    print("AI：", ai_idiom)

    # 用户继续接
    current = input("请接成语：")
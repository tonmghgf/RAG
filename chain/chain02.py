# ==========================================
# 无网络、无新安装、无模型下载
# 100% 使用你现有环境！
# ==========================================
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

# ================= 导入现有环境已有的库 =================
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# ================= 本地 Ollama 大模型 =================
chat_model = ChatOpenAI(
    openai_api_key="ollama",
    base_url="http://localhost:11434/v1",
    model="qwen2.5:0.5b"
)

# ================= 直接读取文本（不走RAG，避免向量模型） =================
with open(r"D:\ollama\chain\sanguoyanyi.txt", "r", encoding="utf-8") as f:
    context = f.read()

# ================= 提示词 =================
system_message = SystemMessagePromptTemplate.from_template(
    "根据以下已知信息回答用户问题，不许编造。\n已知信息：{context}"
)
human_message = HumanMessagePromptTemplate.from_template("用户问题：{question}")
chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])

# ================= 构造链 =================
chain = chat_prompt | chat_model

# ================= 运行 =================
user_question = "五虎上将有哪些？"

response = chain.invoke({
    "context": context,
    "question": user_question
})

print("\n✅ 模型回答：")
print(response.content)
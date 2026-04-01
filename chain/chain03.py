import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1",
    model="qwen2.5:0.5b"
)

prompt = ChatPromptTemplate.from_template("说出一句包含 {topic} 的诗句")
parser = StrOutputParser()

chain = prompt | model | parser
print(chain.invoke({"topic": "花"}))
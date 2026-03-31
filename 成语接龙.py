from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent
IDIOM_DICT_PATH = BASE_DIR / "常用成语词典大全2021.txt"
EMBEDDING_MODEL_PATH = BASE_DIR / "models" / "bge-large-zh-v1.5"

# ====================== 这里改成 gemma3 ======================
OLLAMA_MODEL = "gemma3"
# =============================================================


def load_all_idioms(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return [line.strip() for line in lines if len(line.strip()) == 4]


def format_docs(docs) -> str:
    return "\n".join(d.page_content.strip() for d in docs)


def clean_idiom(text: str) -> str:
    return "".join(c for c in text if "\u4e00" <= c <= "\u9fff")[:4]


def find_local_idiom(idioms: list[str], first_char: str) -> None:
    for idiom in idioms:
        if idiom.startswith(first_char):
            return idiom
    return None


if not IDIOM_DICT_PATH.exists():
    raise FileNotFoundError(
        f"未找到成语词典文件：{IDIOM_DICT_PATH}\n"
        "请确认词典文件和脚本放在同一目录下。"
    )

idiom_list = load_all_idioms(IDIOM_DICT_PATH)

chat_model = ChatOpenAI(
    openai_api_key="ollama",
    base_url="http://localhost:11434/v1",
    model=OLLAMA_MODEL,  # 这里会自动用 gemma3
    temperature=0.01,
    max_tokens=16,
)

prompt = ChatPromptTemplate.from_template(
    """
规则：
1. 只许输出一个四字成语，不要任何多余文字
2. 用上一个成语最后一个字开头
3. 只能使用提供的成语列表

可用成语列表：
{context}

上一个成语：{question}
你接：
""".strip()
)

rag_chain = None
if EMBEDDING_MODEL_PATH.exists():
    try:
        loader = TextLoader(str(IDIOM_DICT_PATH), encoding="utf-8")
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        chunks = text_splitter.split_documents(docs)

        embedding = HuggingFaceEmbeddings(
            model_name=str(EMBEDDING_MODEL_PATH),
            model_kwargs={"device": "cpu"}
        )
        vs = FAISS.from_documents(chunks, embedding)
        retriever = vs.as_retriever(search_kwargs={"k": 20})
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | chat_model
            | StrOutputParser()
        )
        print("✅ RAG 向量库加载成功")
    except Exception as e:
        print(f"⚠️ RAG 加载失败：{e}，将使用本地词典模式")
else:
    print(f"提示：未找到向量模型目录 {EMBEDDING_MODEL_PATH}")
    print("将跳过 RAG，直接使用本地成语词典兜底接龙。")

print(f"\n=== 成语接龙（模型：{OLLAMA_MODEL}）===")
print("输入 q 退出游戏\n")

while True:
    user_idiom = input("你出：").strip()
    if user_idiom.lower() in {"q", "quit", "exit"}:
        print("游戏结束。")
        break

    if len(user_idiom) != 4:
        print("❌ 请输入四字成语！")
        continue

    if user_idiom not in idiom_list:
        print("❌ 该成语不在本地词典中，请换一个！")
        continue

    last_char = user_idiom[-1]
    ai_idiom = ""

    if rag_chain is not None:
        try:
            raw_ans = rag_chain.invoke(user_idiom).strip()
            ai_idiom = clean_idiom(raw_ans)
            print(f"🤖 模型原始输出：{raw_ans}")
        except Exception as exc:
            print(f"⚠️ 模型调用失败，改用本地词典：{exc}")

    valid = False
    if len(ai_idiom) == 4 and ai_idiom.startswith(last_char) and ai_idiom in idiom_list:
        print("✅ AI：", ai_idiom)
        valid = True

    if valid:
        continue

    print("🔍 使用本地词典兜底...")
    fallback_idiom = find_local_idiom(idiom_list, last_char)
    if fallback_idiom:
        print("✅ AI：", fallback_idiom)
    else:
        print("🏆 AI：我接不上了，你赢了！")
        break
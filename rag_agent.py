from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ドキュメントを準備
docs = [
    "エンジンECUは燃料噴射量と点火タイミングを制御し、燃費と出力を最適化する。",
    "ボディECUはドアロックやウィンドウ、ライトなどの車体系装備を制御する。",
    "ABS-ECUはブレーキ時の車輪ロックを防止し、制動距離を短縮する。",
    "CAN通信は車内の複数ECU間でデータをやり取りするための通信プロトコルである。",
    "機能安全はISO26262で規定されており、自動車の電子システムの安全性を確保する規格である。",
]

# ベクターストアを作成
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_texts(docs, embeddings)

# 検索ツールを定義
@tool
def search_ecu_docs(query: str) -> str:
    """ECUや車載システムに関するドキュメントを検索する"""
    results = vectorstore.similarity_search(query, k=2)
    return "\n".join([r.page_content for r in results])

# エージェントを作成
model = ChatAnthropic(model="claude-opus-4-6")
agent = create_react_agent(
    model, 
    [search_ecu_docs],
    prompt="ドキュメントに書いてある情報だけを使って答えてください。"
)

# 実行
response = agent.invoke({
    "messages": [{"role": "user", "content": "機能安全とCAN通信について教えて"}]
})

print(response["messages"][-1].content)
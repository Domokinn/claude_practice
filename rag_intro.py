from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

# ドキュメントを用意
docs = [
    "トヨタのプリウスは世界初の量産ハイブリッド車で1997年に発売された。",
    "ホンダのインサイトは北米市場向けのハイブリッド車で1999年に発売された。",
    "日産のリーフは2010年に発売された世界初の量産電気自動車の一つ。",
    "テスラのモデルSは2012年に発売された高級電気自動車でEV普及に大きく貢献した。",
]

# ベクターストアに保存
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_texts(docs, embeddings)

# 質問
query = "ハイブリッド車の歴史を教えて"

# 関連ドキュメントを検索
results = vectorstore.similarity_search(query, k=2)
context = "\n".join([r.page_content for r in results])

# Claudeに渡して回答させる
model = ChatAnthropic(model="claude-opus-4-6")
prompt = ChatPromptTemplate.from_messages([
    ("system", "以下の情報をもとに質問に答えてください。\n\n{context}"),
    ("human", "{question}")
])

chain = prompt | model
response = chain.invoke({"context": context, "question": query})

print("=== 参照したドキュメント ===")
print(context)
print("\n=== Claudeの回答 ===")
print(response.content)
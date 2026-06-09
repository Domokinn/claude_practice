from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

# テキストファイルを読み込む
with open("sample.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 行ごとに分割してドキュメントにする
docs = [line.strip() for line in text.split("\n") if line.strip()]

# ベクターストアに保存
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_texts(docs, embeddings)

# 質問
query = "ボディECUは何を制御しますか？"

# 関連ドキュメントを検索
results = vectorstore.similarity_search(query, k=2)
context = "\n".join([r.page_content for r in results])

# Claudeに渡して回答させる
model = ChatAnthropic(model="claude-opus-4-6")
prompt = ChatPromptTemplate.from_messages([
    ("system", "以下の情報をもとに質問に答えてください。情報に書いていないことは答えないでください。\n\n{context}"),
    ("human", "{question}")
])

chain = prompt | model
response = chain.invoke({"context": context, "question": query})

print("=== 参照したドキュメント ===")
print(context)
print("\n=== Claudeの回答 ===")
print(response.content)
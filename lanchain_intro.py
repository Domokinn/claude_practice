from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

model = ChatAnthropic(model="claude-opus-4-6")

# 1段階目：要約
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "与えられたテキストを3行で要約してください。"),
    ("human", "{text}")
])

# 2段階目：一言でまとめる
oneliner_prompt = ChatPromptTemplate.from_messages([
    ("system", "与えられたテキストを一言でまとめてください。"),
    ("human", "{summary}")
])

# 2段階のチェーン
chain = summary_prompt | model

summary = chain.invoke({"text": "Pythonは1991年にグイド・ヴァンロッサムが開発したプログラミング言語で、シンプルな文法と豊富なライブラリが特徴。Web開発、データ分析、AI開発など幅広い分野で使われており、世界で最も人気のある言語の一つとなっている。"})

chain2 = oneliner_prompt | model

final = chain2.invoke({"summary": summary.content})

print("=== 要約 ===")
print(summary.content)
print("=== 一言 ===")
print(final.content)
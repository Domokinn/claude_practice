from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

model = ChatAnthropic(model="claude-opus-4-6")

# 調査エージェント
@tool
def search_info(query: str) -> str:
    """ECU関連情報を調査する"""
    db = {
        "CAN": "CANはController Area Networkの略で車内ECU間通信プロトコル。最大1Mbps。",
        "ISO26262": "ISO26262は自動車機能安全規格。ASILはA〜Dの4段階。",
        "エンジンECU": "エンジンECUは燃料噴射と点火タイミングを制御する。",
    }
    for key in db:
        if key in query:
            return db[key]
    return "情報が見つかりませんでした"

research_agent = create_react_agent(
    model,
    [search_info],
    prompt="あなたは調査担当です。必要な情報を検索して事実のみを返してください。"
)

# 執筆エージェント
writer_agent = create_react_agent(
    model,
    [],
    prompt="あなたは技術ライターです。与えられた情報をわかりやすくまとめてください。"
)

# パイプライン実行
query = "CAN通信とISO26262について説明して"

# Step1: 調査
research_result = research_agent.invoke({
    "messages": [HumanMessage(content=query)]
})
research_output = research_result["messages"][-1].content

print("=== 調査結果 ===")
print(research_output)

# Step2: 執筆
write_result = writer_agent.invoke({
    "messages": [HumanMessage(content=f"以下の情報をもとに説明文を書いて：\n{research_output}")]
})

print("\n=== 最終回答 ===")
print(write_result["messages"][-1].content)
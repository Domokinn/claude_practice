from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ツールを定義
@tool
def get_ecu_info(ecu_type: str) -> str:
    """ECUの種類に応じて情報を返す"""
    ecu_db = {
        "エンジンECU": "燃料噴射量と点火タイミングを制御する",
        "ボディECU": "ドアロックやウィンドウ、ライトを制御する",
        "ABSECU": "ブレーキ時の車輪ロックを防止する",
    }
    return ecu_db.get(ecu_type, "該当するECUが見つかりません")

@tool
def calculate(expression: str) -> str:
    """簡単な数式を計算する"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "計算できませんでした"

# エージェントを作成
model = ChatAnthropic(model="claude-opus-4-6")
agent = create_react_agent(model, [get_ecu_info, calculate])

# 実行
response = agent.invoke({
    "messages": [{"role": "user", "content": "エンジンECUとボディECUの役割を教えて、あと12345×678の計算もして"}]
})

print(response["messages"][-1].content)
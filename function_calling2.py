from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

model = ChatAnthropic(model="claude-opus-4-6")

# ツール1：ECU情報を取得
@tool
def get_ecu_spec(ecu_name: str) -> str:
    """ECUの仕様情報を取得する"""
    specs = {
        "エンジンECU": "CPU: 32bit, RAM: 512KB, 通信: CAN/LIN, ASIL: D",
        "ボディECU": "CPU: 16bit, RAM: 128KB, 通信: CAN/LIN, ASIL: B",
        "ABS-ECU": "CPU: 32bit, RAM: 256KB, 通信: CAN, ASIL: C",
    }
    return specs.get(ecu_name, "仕様が見つかりません")

# ツール2：ASIL等級を評価
@tool
def evaluate_asil(asil_level: str) -> str:
    """ASIL等級の意味と要件を返す"""
    asil_info = {
        "A": "最も低い安全要件。軽微な怪我のリスク。",
        "B": "中程度の安全要件。重傷のリスク。",
        "C": "高い安全要件。生命に関わるリスク。",
        "D": "最高の安全要件。致命的なリスク。冗長設計が必要。",
    }
    return asil_info.get(asil_level, "不明なASIL等級")

# ツール3：互換性チェック
@tool
def check_compatibility(ecu1: str, ecu2: str) -> str:
    """2つのECU間の通信互換性をチェックする"""
    compatible_pairs = [
        ("エンジンECU", "ABS-ECU"),
        ("ボディECU", "エンジンECU"),
    ]
    if (ecu1, ecu2) in compatible_pairs or (ecu2, ecu1) in compatible_pairs:
        return f"{ecu1}と{ecu2}はCAN通信で互換性あり"
    return f"{ecu1}と{ecu2}の互換性は未確認"

# エージェント作成
agent = create_react_agent(model, [get_ecu_spec, evaluate_asil, check_compatibility])

# 実行
response = agent.invoke({
    "messages": [HumanMessage(content="エンジンECUとABS-ECUの仕様を調べて、それぞれのASIL等級の意味も教えて。あと2つの互換性も確認して。")]
})

for msg in response["messages"]:
    print(f"--- {msg.type} ---")
    print(msg.content)
    print()
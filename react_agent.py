from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

model = ChatAnthropic(model="claude-opus-4-6")

# ツール1：ECUドキュメント検索
@tool
def search_ecu_document(query: str) -> str:
    """ECU仕様書からキーワードに関連する情報を検索する"""
    documents = {
        "CAN": "CAN通信速度：500kbps、フレーム形式：標準フレーム11bit ID、エラー検出：CRC/ACK",
        "ASIL": "ASIL-D要件：冗長設計必須、診断カバレッジ99%以上、FMEA実施必須",
        "エンジンECU": "CPU：32bit 200MHz、フラッシュ：2MB、RAM：512KB、動作温度：-40〜125℃",
        "ボディECU": "CPU：16bit 40MHz、フラッシュ：256KB、RAM：32KB、動作温度：-40〜85℃",
    }
    for key in documents:
        if key in query:
            return documents[key]
    return "該当する仕様が見つかりません"

# ツール2：FMEA計算
@tool
def calculate_risk(severity: int, occurrence: int, detection: int) -> str:
    """FMEAのRPN（リスク優先数）を計算する。各引数は1〜10の整数"""
    rpn = severity * occurrence * detection
    if rpn >= 200:
        risk = "高リスク：即時対策必要"
    elif rpn >= 100:
        risk = "中リスク：対策検討必要"
    else:
        risk = "低リスク：監視継続"
    return f"RPN={rpn}、判定：{risk}"

# ツール3：互換性チェック
@tool
def check_can_compatibility(node1: str, node2: str) -> str:
    """2つのECUノード間のCAN通信互換性を確認する"""
    compatible = [
        ("エンジンECU", "ABS-ECU"),
        ("エンジンECU", "ボディECU"),
        ("ABS-ECU", "ボディECU"),
    ]
    if (node1, node2) in compatible or (node2, node1) in compatible:
        return f"{node1}と{node2}：CAN通信互換性あり、同一バス接続可能"
    return f"{node1}と{node2}：互換性未確認、要検証"

# エージェント作成
agent = create_react_agent(
    model,
    [search_ecu_document, calculate_risk, check_can_compatibility],
    prompt="あなたは車載システムの技術専門家です。ツールを使って正確な情報を提供してください。"
)

# 実行
response = agent.invoke({
    "messages": [HumanMessage(content="""
以下のタスクをすべて実行して：
1. エンジンECUとボディECUの仕様を調べる
2. エンジンECUのCAN通信仕様を調べる
3. 深刻度8、発生頻度3、検出度4でFMEAのRPNを計算する
4. エンジンECUとABS-ECUの互換性を確認する
""")]
})

print(response["messages"][-1].content)
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

model = ChatAnthropic(model="claude-opus-4-6")

class State(TypedDict):
    messages: List
    research: str
    final_answer: str
    needs_retry: bool

# ノード1：調査
def research_node(state: State) -> State:
    question = state["messages"][0].content
    response = model.invoke([
        HumanMessage(content=f"以下の質問に関する事実だけを箇条書きで3点答えて：{question}")
    ])
    research = response.content
    # 情報が少なすぎたら再試行フラグを立てる
    needs_retry = len(research) < 100
    return {"research": research, "needs_retry": needs_retry}

# ノード2：再調査
def retry_node(state: State) -> State:
    question = state["messages"][0].content
    response = model.invoke([
        HumanMessage(content=f"もっと詳しく教えて：{question}")
    ])
    return {"research": response.content, "needs_retry": False}

# ノード3：執筆
def writer_node(state: State) -> State:
    response = model.invoke([
        HumanMessage(content=f"以下の情報をわかりやすい説明文にして：\n{state['research']}")
    ])
    return {"final_answer": response.content}

# 条件分岐
def check_research(state: State) -> str:
    if state["needs_retry"]:
        print("→ 情報が少ないので再調査します")
        return "retry"
    return "writer"

# グラフを構築
graph = StateGraph(State)
graph.add_node("research", research_node)
graph.add_node("retry", retry_node)
graph.add_node("writer", writer_node)

graph.set_entry_point("research")
graph.add_conditional_edges("research", check_research, {
    "retry": "retry",
    "writer": "writer"
})
graph.add_edge("retry", "writer")
graph.add_edge("writer", END)

app = graph.compile()

# 実行
result = app.invoke({
    "messages": [HumanMessage(content="CAN通信とは何か教えて")],
    "research": "",
    "final_answer": "",
    "needs_retry": False
})

print("=== 調査結果 ===")
print(result["research"])
print("\n=== 最終回答 ===")
print(result["final_answer"])
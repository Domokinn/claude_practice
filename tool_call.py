import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "指定した都市の天気を返す",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "都市名"
                }
            },
            "required": ["city"]
        }
    }
]

# 1回目：Claudeがツールを呼ぶ判断をする
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "名古屋の天気を教えて"}]
)

# 2回目：ツールの結果を返してClaudeに最終回答させる
tool_use = response.content[0]

final_response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "名古屋の天気を教えて"},
        {"role": "assistant", "content": response.content},
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": "晴れ、気温28度"  # ダミーの天気データ
                }
            ]
        }
    ]
)

print(final_response.content[0].text)
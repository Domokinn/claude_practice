import anthropic

client = anthropic.Anthropic()

print("=== ストリーミング出力 ===")

with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "CAN通信について200文字程度で説明して"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print("\n=== 完了 ===")
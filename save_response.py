import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Pythonの仮想環境とは何か、3行で説明して"}]
)

response_text = message.content[0].text

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(response_text)

print("保存完了！")
print(response_text)
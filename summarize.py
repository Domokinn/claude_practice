import anthropic
import argparse

parser = argparse.ArgumentParser(description="テキストをClaudeが要約するツール")
parser.add_argument("text", help="要約したいテキスト")
args = parser.parse_args()

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"以下のテキストを3行で要約して：\n\n{args.text}"}]
)

print(message.content[0].text)
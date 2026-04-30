from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic

agent = ChatAnthropic(model="claude-opus-4-6")
history = []

print("Chatbot ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit"):
        break

    history.append({"role": "user", "content": user_input})
    result = agent.invoke(history)
    text = result.content if isinstance(result.content, str) else "\n".join(b["text"] for b in result.content if b.get("type") == "text")
    history.append({"role": "assistant", "content": text})
    print(f"Claude: {text}\n")

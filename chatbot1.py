from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic

agent = ChatAnthropic(model="claude-opus-4-6")

print("Chatbot ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit"):
        break

    result = agent.invoke(user_input)
    print(f"Claude: {result.content}\n")

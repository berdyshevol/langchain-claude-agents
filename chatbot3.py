from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# LLM with tools
llm = ChatAnthropic(model="claude-sonnet-4-20250514")
search = DuckDuckGoSearchRun()
tools = [search]
tools_by_name = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)

# Conversation history with system prompt
history = [
    SystemMessage(content=(
        "You are a helpful assistant. Answer concisely. "
        "You have access to a web search tool — use it when the user asks about "
        "current events, recent news, or anything you're unsure about."
    ))
]


def extract_text(content):
    """Extract text from response content (handles both str and list formats)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b["text"] for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return str(content)


print("Chatbot ready (with search & memory). Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit"):
        break

    history.append(HumanMessage(content=user_input))

    # Agent loop: keep going until no more tool calls
    while True:
        response = llm_with_tools.invoke(history)
        history.append(response)

        # If no tool calls, print and done
        if not response.tool_calls:
            print(f"Claude: {extract_text(response.content)}\n")
            break

        # Execute tool calls
        for tool_call in response.tool_calls:
            tool_fn = tools_by_name[tool_call["name"]]
            print(f"[Searching: {tool_call['args'].get('query', '')}...]", flush=True)
            result = tool_fn.invoke(tool_call["args"])
            history.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))

    # Trim history if it gets too long (keep system + last 20 messages)
    if len(history) > 22:
        history = [history[0]] + history[-20:]

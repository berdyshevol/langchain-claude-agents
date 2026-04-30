# LangChain + Claude — Chatbot to Agent Progression

Three small Python scripts that step from a stateless chatbot to a tool-using AI agent, using [LangChain](https://www.langchain.com/) and Anthropic's Claude API.

Built as a Master of Science in Information Systems (MSIS) coursework project at Baylor University.

## What's inside

| File | What it demonstrates |
| --- | --- |
| `chatbot1.py` | **Stateless chatbot.** Single-turn — every prompt is independent, no memory. |
| `chatbot2.py` | **Multi-turn chatbot.** Adds conversation history so the model can refer back to earlier turns. |
| `chatbot3.py` | **AI agent with tool use.** Adds a DuckDuckGo web-search tool and a full agent loop. |

### chatbot3.py — the agent loop

The third script is the most interesting one. It implements the canonical "reason → act → observe → repeat" pattern:

1. The user sends a message.
2. The script invokes Claude with the full message history.
3. If Claude decides to call the search tool, the script runs the search and feeds the result back as a `ToolMessage`.
4. The loop continues until Claude returns a normal text response (no more tool calls).
5. History is trimmed with a sliding window (system prompt + last 20 messages) so the context window stays bounded.

Key concepts shown:

- `llm.bind_tools()` — letting the LLM decide when to call a tool.
- `HumanMessage` / `AIMessage` / `ToolMessage` — the three message roles needed for tool use.
- Handling Claude's two response formats (plain string vs. structured content blocks).
- Sliding-window memory management.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# then put your Anthropic API key in .env
```

## Run

```bash
python chatbot1.py    # stateless
python chatbot2.py    # multi-turn
python chatbot3.py    # agent with web search
```

Type `quit` to exit any of them.

## Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

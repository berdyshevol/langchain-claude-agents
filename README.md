# Chatbot → Agent

Three short Python scripts that show, at the code level, what changes when a **chatbot** becomes an **agent**.

Built as MSIS coursework at Baylor University using [LangChain](https://www.langchain.com/) and Anthropic's Claude API.

---

## Why this exists

"Chatbot" and "AI agent" get used interchangeably — but they're different things. Pinpointing the difference is awkward in conversation; in code it's obvious.

Each file removes one of the answers to the question *"what makes an agent an agent?"*:

| | `chatbot1.py` | `chatbot2.py` | `chatbot3.py` |
|---|---|---|---|
| Memory across turns | ❌ | ✅ | ✅ |
| Tool use | ❌ | ❌ | ✅ |
| Agent loop (reason → act → observe → repeat) | ❌ | ❌ | ✅ |
| **Verdict** | stateless chatbot | multi-turn chatbot | tool-using agent |

The chatbot/agent boundary is between files 2 and 3.

---

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # then put your Anthropic API key in .env
```

Run any of:

```bash
python chatbot1.py    # stateless
python chatbot2.py    # multi-turn
python chatbot3.py    # agent with web search
```

Type `quit` to exit.

Requires Python 3.10+ and an [Anthropic API key](https://console.anthropic.com/).

---

## The three scripts

### `chatbot1.py` — stateless chatbot

Every prompt is independent. The model has no memory of earlier turns.

```
You: My name is Oleg.
Claude: Nice to meet you, Oleg!
You: What's my name?
Claude: I don't have access to that information. What's your name?
```

Implementation: 18 lines. Single `agent.invoke(user_input)` call per turn.

### `chatbot2.py` — multi-turn chatbot

Adds a `history` list and passes it on every call so the model can refer back to earlier turns.

```
You: My name is Oleg.
Claude: Nice to meet you, Oleg!
You: What's my name?
Claude: Your name is Oleg.
```

Same 18 lines + `history.append(...)` on both sides of the loop.

### `chatbot3.py` — tool-using agent

Adds a DuckDuckGo web-search tool and a real **agent loop**:

1. Send the message.
2. Invoke Claude with the full history.
3. If Claude returns tool calls, execute them and append the results as `ToolMessage`s.
4. Loop until Claude returns a plain text response (no more tool calls).
5. Trim history with a sliding window (system prompt + last 20 messages) to bound the context.

```
You: What's the latest news about Anthropic?
[Searching: latest news Anthropic 2026...]
Claude: Anthropic recently announced ...
You: Summarize that in one sentence.
Claude: <answers from memory, no search needed>
```

Concepts shown:

- `llm.bind_tools()` — let the LLM decide when to call a tool.
- The three message roles for tool use: `HumanMessage`, `AIMessage`, `ToolMessage`.
- Handling Claude's two response formats (plain string vs. list of content blocks).
- Sliding-window memory management.

---

## Files

| File | Purpose |
|---|---|
| `chatbot1.py` | Stateless single-turn chatbot |
| `chatbot2.py` | Multi-turn chatbot with history |
| `chatbot3.py` | Tool-using agent with DuckDuckGo + sliding-window memory |
| `requirements.txt` | `langchain-anthropic`, `langchain-community`, `langchain-core`, `duckduckgo-search`, `python-dotenv` |
| `.env.example` | Template for `ANTHROPIC_API_KEY` |

# The Council — Multi-Agent Debate Engine

A genuinely agentic debate system where three AI personas argue a question in real time, you can jump in anytime, and a Judge delivers a final verdict.

Built with [Groq](https://console.groq.com) (LLaMA 3.3 70B) and Gradio.

---

## What makes it actually agentic

Most "multi-agent" demos are just sequential LLM calls with different system prompts. The Council is different:

- **Each agent decides its own action** before speaking - `SPEAK`, `PASS`, `CHALLENGE <name>`, or `CONCEDE`. Agents go silent when they have nothing new to add.
- **A Moderator agent** reads the debate state after each round and decides whether to continue or call for a verdict - the debate length is not fixed.
- **You are a live participant** - jump in anytime via the chat input. Agents read your messages and can call you out directly.
- **The Judge only activates** when the Moderator signals resolution, not on a timer.

---

## The Cast

| Agent | Role |
|---|---|
| 🔴 **Skeptic** | Challenges assumptions, demands evidence, attacks weak claims |
| 🔵 **Visionary** | Argues for bold, long-term thinking and transformative upside |
| 🟢 **Pragmatist** | Cuts through theory to ask what actually works right now |
| ⚪ **Moderator** | Watches for consensus or circular debate, calls for verdict |
| 🟡 **Judge** | Delivers WINNER / FATAL FLAW / VERDICT at the end |
| 🟣 **You** | Jump in anytime — agents will respond to what you say |

---

## Project Structure

```
the_council/
├── main.py           # Entry point
├── config.py         # Agent definitions, avatars, model config
├── debate_state.py   # Thread-safe shared state and message bus
├── agents.py         # All LLM calls (decide, speak, moderate, judge)
├── debate_runner.py  # Background debate loop thread
├── ui.py             # Gradio UI, CSS, render logic, event handlers
└── requirements.txt
```

Each file has a single responsibility. Swap the LLM provider → edit `agents.py` only. Change personas → edit `config.py` only. Redesign the UI → edit `ui.py` only.

---

## Quickstart

### 1. Clone and install

```bash
git clone https://github.com/your-username/the-council.git
cd the-council
pip install -r requirements.txt
```

### 2. Get a Groq API key

Create an API key.

### 3. Run

```bash
python main.py
```

Open `http://localhost:7860` in your browser. Paste your Groq API key into the UI, enter a question, hit **Convene**.

> Pass `share=True` in `main.py` → `app.launch(share=True)` to get a public Gradio link.

---

## Example Questions to Try

- *Should AGI development be paused?*
- *Is remote work net positive or negative for society?*
- *Should AI systems be allowed to make medical decisions autonomously?*
- *Is open-source AI more dangerous than closed-source AI?*
- *Will large language models ever truly reason?*

---

## How the Debate Works

```
Moderator opens the question
        │
        ▼
┌─── Round loop ──────────────────────────────────┐
│                                                  │
│  For each agent:                                 │
│    1. Decision step  →  SPEAK / PASS /           │
│                         CHALLENGE / CONCEDE      │
│    2. If SPEAK or CHALLENGE → generate response  │
│    3. Response added to shared history           │
│                                                  │
│  You can inject a message at any point           │
│                                                  │
│  After each round (min 2):                       │
│    Moderator decides → CONTINUE or VERDICT       │
└──────────────────────────────────────────────────┘
        │
        ▼
   Judge delivers verdict
   WINNER · FATAL FLAW · VERDICT
```

---

## Configuration

All tunable constants live in `config.py`:

| Variable | Default | Description |
|---|---|---|
| `MODEL` | `llama-3.3-70b-versatile` | Groq model to use |
| `MAX_ROUNDS` | `8` | Hard ceiling on debate rounds |
| `AGENT_DELAY` | `1.0` | Seconds between agent turns |

To add a new agent, add an entry to the `AGENTS` list in `config.py` with `name`, `color`, `bg`, `avatar` (SVG string), and `persona`.

---

## Dependencies

```
groq
gradio
```

That's it. No LangChain, no vector DB, no external APIs beyond Groq.

---

## License

MIT

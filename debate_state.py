import threading

# ── Shared debate state ───────────────────────────────────────────────────────
# All agent threads and the UI read/write through this single object.
# The lock must be held when mutating messages or history_text.

state = {
    "messages": [],        # list of dicts: {name, color, bg, avatar, text}
    "history_text": "",    # plain-text transcript fed to LLMs
    "running": False,      # True while the debate thread is alive
    "question": "",        # current debate question
    "lock": threading.Lock(),
}


def reset():
    """Clear state for a fresh debate."""
    with state["lock"]:
        state["messages"] = []
        state["history_text"] = ""
        state["running"] = False
        state["question"] = ""


def add_message(name: str, color: str, bg: str, avatar: str, text: str):
    """Append a message to the shared log and plain-text transcript."""
    with state["lock"]:
        state["messages"].append({
            "name": name,
            "color": color,
            "bg": bg,
            "avatar": avatar,
            "text": text,
        })
        state["history_text"] += f"\n[{name}]: {text}"


def get_messages():
    with state["lock"]:
        return list(state["messages"])


def get_history():
    with state["lock"]:
        return state["history_text"]


def is_running():
    return state["running"]


def stop():
    state["running"] = False

import json
from groq import Groq
from config import MODEL


# ── Decision step ─────────────────────────────────────────────────────────────

def decide_action(client: Groq, agent: dict, history: str, question: str) -> dict:
    """
    Ask the agent what it wants to do this turn.
    Returns one of:
      {"action": "SPEAK"}
      {"action": "PASS"}
      {"action": "CHALLENGE", "target": "<AgentName>"}
      {"action": "CONCEDE"}
    """
    prompt = (
        f'Debate question: "{question}"\n\n'
        f"Recent debate:\n{history[-2000:]}\n\n"
        f"You are {agent['name']}. Decide your next action.\n"
        f"Reply with ONLY a JSON object — no extra text:\n"
        f'  {{"action": "SPEAK"}}          — you have something new to add\n'
        f'  {{"action": "PASS"}}           — your point was already made\n'
        f'  {{"action": "CHALLENGE", "target": "Name"}} — call someone out directly\n'
        f'  {{"action": "CONCEDE"}}        — you genuinely agree now\n'
        f"PASS if you are repeating yourself. CONCEDE only if truly convinced."
    )
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": agent["persona"]},
                {"role": "user",   "content": prompt},
            ],
            max_tokens=60,
            temperature=0.4,
        )
        raw = resp.choices[0].message.content.strip()
        start, end = raw.find("{"), raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except Exception:
        pass
    return {"action": "SPEAK"}


# ── Speech step ───────────────────────────────────────────────────────────────

def agent_speak(
    client: Groq,
    agent: dict,
    history: str,
    question: str,
    context_note: str = "",
) -> str:
    """Generate the agent's actual message (max 2 sentences)."""
    prompt = (
        f'Debate question: "{question}"\n\n'
        f"Recent debate:\n{history[-2500:]}\n\n"
        f"{context_note}"
        f"Respond as {agent['name']}. Max 2 punchy sentences. No filler."
    )
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": agent["persona"]},
                {"role": "user",   "content": prompt},
            ],
            max_tokens=120,
            temperature=0.8,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[error: {e}]"


# ── Moderator ─────────────────────────────────────────────────────────────────

def moderator_decision(
    client: Groq,
    history: str,
    question: str,
    round_num: int,
) -> dict:
    """
    Decide whether the debate should CONTINUE or move to VERDICT.
    Returns:
      {"decision": "CONTINUE"}
      {"decision": "VERDICT", "reason": "..."}
    """
    prompt = (
        f'Debate question: "{question}"\n\n'
        f"Debate so far (round {round_num}):\n{history[-3000:]}\n\n"
        f"Should the debate CONTINUE or move to VERDICT?\n"
        f'Reply ONLY with JSON: {{"decision": "CONTINUE"}} or {{"decision": "VERDICT", "reason": "brief reason"}}\n'
        f"Rules: minimum 2 rounds. Call VERDICT if consensus emerged, debate is circular, or round > 5. "
        f"If going in circles, nudge but don't end too early."
    )
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a sharp debate moderator. Be decisive."},
                {"role": "user",   "content": prompt},
            ],
            max_tokens=80,
            temperature=0.3,
        )
        raw = resp.choices[0].message.content.strip()
        start, end = raw.find("{"), raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except Exception:
        pass
    return {"decision": "CONTINUE"}


# ── Judge ─────────────────────────────────────────────────────────────────────

def run_judge(client: Groq, history: str, question: str) -> str:
    """Deliver a final structured verdict."""
    prompt = (
        f'Debate question: "{question}"\n\nFull debate:\n{history}\n\n'
        f"Deliver a verdict in exactly 3 parts:\n"
        f"WINNER: [who made the strongest case, one sentence]\n"
        f"FATAL FLAW: [the weakest argument in the debate, one sentence]\n"
        f"VERDICT: [your own conclusion on the question, 2 sentences max]"
    )
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a ruthless, fair debate judge. Be concise and definitive."},
                {"role": "user",   "content": prompt},
            ],
            max_tokens=200,
            temperature=0.5,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[Judge error: {e}]"

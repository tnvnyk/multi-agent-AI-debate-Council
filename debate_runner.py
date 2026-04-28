import time
import threading
from groq import Groq

import debate_state as ds
from agents import decide_action, agent_speak, moderator_decision, run_judge
from config import AGENTS, MODERATOR, JUDGE, AGENT_DELAY, MAX_ROUNDS


def _debate_loop(client: Groq, question: str):
    """Main debate logic — runs in a background thread."""
    ds.state["running"] = True

    ds.add_message(
        MODERATOR["name"], MODERATOR["color"], MODERATOR["bg"], MODERATOR["avatar"],
        f'The question: "{question}" — Council, begin.',
    )
    time.sleep(AGENT_DELAY)

    for round_num in range(1, MAX_ROUNDS + 1):
        if not ds.is_running():
            break

        spoke_count = 0

        for agent in AGENTS:
            if not ds.is_running():
                break

            history  = ds.get_history()
            decision = decide_action(client, agent, history, question)
            action   = decision.get("action", "SPEAK")

            if action == "PASS":
                # Agent stays silent this turn
                pass

            elif action == "CONCEDE":
                ds.add_message(
                    agent["name"], agent["color"], agent["bg"], agent["avatar"],
                    "I'll concede that point.",
                )
                spoke_count += 1

            elif action == "CHALLENGE":
                target = decision.get("target", "")
                note   = f"You are directly challenging {target}. " if target else ""
                text   = agent_speak(client, agent, ds.get_history(), question, note)
                ds.add_message(agent["name"], agent["color"], agent["bg"], agent["avatar"], text)
                spoke_count += 1

            else:  # SPEAK
                text = agent_speak(client, agent, ds.get_history(), question)
                ds.add_message(agent["name"], agent["color"], agent["bg"], agent["avatar"], text)
                spoke_count += 1

            time.sleep(AGENT_DELAY)

        if not ds.is_running():
            break

        # After each round (min 2) let the moderator decide
        if round_num >= 2:
            mod = moderator_decision(client, ds.get_history(), question, round_num)
            if mod.get("decision") == "VERDICT":
                reason = mod.get("reason", "")
                ds.add_message(
                    MODERATOR["name"], MODERATOR["color"], MODERATOR["bg"], MODERATOR["avatar"],
                    f"Calling it. {reason}",
                )
                time.sleep(AGENT_DELAY)
                break

        if spoke_count == 0:
            ds.add_message(
                MODERATOR["name"], MODERATOR["color"], MODERATOR["bg"], MODERATOR["avatar"],
                "Nobody has more to say. Moving to verdict.",
            )
            break

    # Final verdict
    verdict = run_judge(client, ds.get_history(), question)
    ds.add_message(JUDGE["name"], JUDGE["color"], JUDGE["bg"], JUDGE["avatar"], verdict)
    ds.state["running"] = False


def start_debate_thread(client: Groq, question: str) -> threading.Thread:
    """Spawn and return the debate background thread."""
    t = threading.Thread(target=_debate_loop, args=(client, question), daemon=True)
    t.start()
    return t

import gradio as gr
from groq import Groq

import debate_state as ds
from debate_runner import start_debate_thread
from config import HUMAN

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body, .gradio-container {
    background: #0d0d0d !important;
    font-family: 'DM Mono', monospace !important;
    color: #ccc !important;
}

.app-wrap {
    max-width: 860px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
}

.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid #222;
    padding-bottom: 0.8rem;
}

.app-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.3rem;
    color: #fff;
    letter-spacing: -0.02em;
}
.app-title span { color: #c9a84c; }

/* inputs */
input[type=password], textarea {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
    color: #ccc !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 0.7rem !important;
    transition: border-color 0.15s !important;
}
input:focus, textarea:focus {
    border-color: #c9a84c !important;
    outline: none !important;
}

/* chat window */
.chat-window {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 10px;
    height: 480px;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
    scroll-behavior: smooth;
}
.chat-window::-webkit-scrollbar { width: 4px; }
.chat-window::-webkit-scrollbar-track { background: transparent; }
.chat-window::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 4px; }

/* messages */
.msg-row {
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
    animation: fadeUp 0.25s ease;
}
.msg-row.human { flex-direction: row-reverse; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0);   }
}

.avatar-wrap {
    flex-shrink: 0;
    width: 36px; height: 36px;
    border-radius: 50%;
    overflow: hidden;
}

.bubble {
    max-width: 72%;
    border-radius: 10px;
    padding: 0.5rem 0.75rem;
    font-size: 0.83rem;
    line-height: 1.55;
}
.msg-row.human .bubble {
    background: #1e1a2a;
    border: 1px solid #a084e833;
    color: #d4c8f0;
    text-align: right;
}

.sender {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-bottom: 0.2rem;
    text-transform: uppercase;
}

/* human input row */
.human-input-row textarea {
    flex: 1;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 0.8rem !important;
    resize: none !important;
}
.human-input-row textarea:focus {
    border-color: #a084e8 !important;
}

/* buttons */
button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 7px !important;
    border: none !important;
    cursor: pointer !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.15s !important;
}
.start-btn {
    background: #c9a84c !important;
    color: #0d0d0d !important;
    padding: 0.55rem 1.2rem !important;
}
.start-btn:hover {
    background: #d4b85c !important;
    box-shadow: 0 0 12px rgba(201,168,76,0.35) !important;
}
.send-btn {
    background: #a084e8 !important;
    color: #fff !important;
    padding: 0.55rem 1rem !important;
    white-space: nowrap !important;
}
.send-btn:hover { background: #b090f0 !important; }
.stop-btn {
    background: #333 !important;
    color: #aaa !important;
    padding: 0.55rem 0.9rem !important;
}

footer { display: none !important; }
.label-wrap { display: none !important; }
"""


# ── Render ────────────────────────────────────────────────────────────────────

def render_chat(messages: list) -> str:
    if not messages:
        return (
            "<div class='chat-window' id='chat-window'>"
            "<div style='color:#333;font-size:0.8rem;text-align:center;margin-top:2rem;'>"
            "Waiting for the council to convene..."
            "</div></div>"
        )

    html = "<div class='chat-window' id='chat-window'>"
    for m in messages:
        is_human     = m["name"] == "You"
        row_class    = "msg-row human" if is_human else "msg-row"
        sender_color = "#a084e8" if is_human else m["color"]

        html += f"<div class='{row_class}'>"
        html += f"<div class='avatar-wrap'>{m['avatar']}</div>"
        html += (
            f"<div class='bubble' style='background:{m['bg']};border:1px solid {m['color']}22;'>"
            f"<div class='sender' style='color:{sender_color};'>{m['name']}</div>"
            f"<div>{m['text']}</div>"
            f"</div>"
        )
        html += "</div>"

    html += "</div>"
    # auto-scroll
    html += "<script>var c=document.getElementById('chat-window');if(c)c.scrollTop=c.scrollHeight;</script>"
    return html


# ── Event handlers ────────────────────────────────────────────────────────────

def handle_start(api_key: str, question: str):
    if not api_key.strip():
        return "<div class='chat-window'><div style='color:#e05c5c;padding:1rem;'>Enter your Groq API key.</div></div>", "idle"
    if not question.strip():
        return "<div class='chat-window'><div style='color:#e05c5c;padding:1rem;'>Enter a debate question.</div></div>", "idle"
    if ds.is_running():
        return render_chat(ds.get_messages()), "running"

    ds.reset()
    ds.state["question"] = question.strip()

    client = Groq(api_key=api_key.strip())
    start_debate_thread(client, question.strip())

    return render_chat(ds.get_messages()), "running"


def handle_stop():
    ds.stop()
    return render_chat(ds.get_messages()), "idle"


def handle_human_message(text: str):
    if text.strip():
        ds.add_message(
            HUMAN["name"], HUMAN["color"], HUMAN["bg"], HUMAN["avatar"],
            text.strip(),
        )
    return render_chat(ds.get_messages()), ""


def handle_refresh():
    status = "running" if ds.is_running() else "idle"
    return render_chat(ds.get_messages()), status


# ── Layout ────────────────────────────────────────────────────────────────────

def build_ui() -> gr.Blocks:
    with gr.Blocks(css=CSS, title="The Council") as app:

        gr.HTML("""
        <div class="app-wrap">
          <div class="top-bar">
            <div class="app-title">THE <span>COUNCIL</span></div>
            <div style="font-size:0.72rem;color:#444;letter-spacing:0.05em;">MULTI-AGENT DEBATE</div>
          </div>
        </div>
        """)

        with gr.Row(elem_classes=["app-wrap"]):
            api_key = gr.Textbox(
                placeholder="Groq API key  (gsk_...)",
                type="password",
                show_label=False,
                scale=2,
            )
            question = gr.Textbox(
                placeholder="Debate question...",
                show_label=False,
                scale=5,
            )
            start_btn = gr.Button("Convene", elem_classes=["start-btn"], scale=1)
            stop_btn  = gr.Button("Stop",    elem_classes=["stop-btn"],  scale=1)

        status_state = gr.State("idle")
        chat_html    = gr.HTML(render_chat([]))

        with gr.Row():
            human_input = gr.Textbox(
                placeholder="Jump in anytime... (Enter or Send)",
                show_label=False,
                scale=6,
                lines=1,
                elem_classes=["human-input-row"],
            )
            send_btn = gr.Button("Send", elem_classes=["send-btn"], scale=1)

        # auto-refresh every 1.5 s while debate runs
        timer = gr.Timer(value=1.5)
        timer.tick(fn=handle_refresh, outputs=[chat_html, status_state])

        start_btn.click(fn=handle_start,         inputs=[api_key, question],  outputs=[chat_html, status_state])
        stop_btn.click( fn=handle_stop,                                        outputs=[chat_html, status_state])
        send_btn.click( fn=handle_human_message, inputs=[human_input],         outputs=[chat_html, human_input])
        human_input.submit(fn=handle_human_message, inputs=[human_input],      outputs=[chat_html, human_input])

    return app

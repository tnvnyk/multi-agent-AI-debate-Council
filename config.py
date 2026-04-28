# ── Model ─────────────────────────────────────────────────────────────────────
MODEL = "llama-3.3-70b-versatile"
MAX_ROUNDS = 8
AGENT_DELAY = 1.0  # seconds between agent turns

# ── Avatars ───────────────────────────────────────────────────────────────────
AVATAR_SKEPTIC = """<svg viewBox="0 0 48 48" width="36" height="36" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="22" fill="#2a1515" stroke="#e05c5c" stroke-width="2"/>
  <circle cx="24" cy="18" r="8" fill="#e05c5c" opacity="0.9"/>
  <ellipse cx="24" cy="36" rx="12" ry="8" fill="#e05c5c" opacity="0.9"/>
  <line x1="16" y1="15" x2="20" y2="17" stroke="#2a1515" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="32" y1="15" x2="28" y2="17" stroke="#2a1515" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M19 22 Q24 20 29 22" stroke="#2a1515" stroke-width="1.5" fill="none" stroke-linecap="round"/>
</svg>"""

AVATAR_VISIONARY = """<svg viewBox="0 0 48 48" width="36" height="36" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="22" fill="#111e2a" stroke="#5c9ee0" stroke-width="2"/>
  <circle cx="24" cy="18" r="8" fill="#5c9ee0" opacity="0.9"/>
  <ellipse cx="24" cy="36" rx="12" ry="8" fill="#5c9ee0" opacity="0.9"/>
  <path d="M18 14 L24 8 L30 14" stroke="#111e2a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="21" cy="18" r="1.2" fill="#111e2a"/>
  <circle cx="27" cy="18" r="1.2" fill="#111e2a"/>
  <path d="M20 22 Q24 25 28 22" stroke="#111e2a" stroke-width="1.5" fill="none" stroke-linecap="round"/>
</svg>"""

AVATAR_PRAGMATIST = """<svg viewBox="0 0 48 48" width="36" height="36" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="22" fill="#112215" stroke="#5ce08a" stroke-width="2"/>
  <circle cx="24" cy="18" r="8" fill="#5ce08a" opacity="0.9"/>
  <ellipse cx="24" cy="36" rx="12" ry="8" fill="#5ce08a" opacity="0.9"/>
  <rect x="19" y="13" width="10" height="2" rx="1" fill="#112215"/>
  <circle cx="21" cy="18" r="1.2" fill="#112215"/>
  <circle cx="27" cy="18" r="1.2" fill="#112215"/>
  <path d="M20 21 Q24 24 28 21" stroke="#112215" stroke-width="1.5" fill="none" stroke-linecap="round"/>
</svg>"""

AVATAR_JUDGE = """<svg viewBox="0 0 48 48" width="36" height="36" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="22" fill="#1a1510" stroke="#c9a84c" stroke-width="2"/>
  <circle cx="24" cy="18" r="8" fill="#c9a84c" opacity="0.9"/>
  <ellipse cx="24" cy="36" rx="12" ry="8" fill="#c9a84c" opacity="0.9"/>
  <rect x="14" y="11" width="20" height="3" rx="1.5" fill="#1a1510"/>
  <rect x="17" y="8" width="14" height="2" rx="1" fill="#1a1510"/>
  <circle cx="21" cy="18" r="1.2" fill="#1a1510"/>
  <circle cx="27" cy="18" r="1.2" fill="#1a1510"/>
  <path d="M20 22 Q24 25 28 22" stroke="#1a1510" stroke-width="1.5" fill="none" stroke-linecap="round"/>
</svg>"""

AVATAR_HUMAN = """<svg viewBox="0 0 48 48" width="36" height="36" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="22" fill="#1e1a2a" stroke="#a084e8" stroke-width="2"/>
  <circle cx="24" cy="18" r="8" fill="#a084e8" opacity="0.9"/>
  <ellipse cx="24" cy="36" rx="12" ry="8" fill="#a084e8" opacity="0.9"/>
  <circle cx="21" cy="17" r="1.5" fill="#1e1a2a"/>
  <circle cx="27" cy="17" r="1.5" fill="#1e1a2a"/>
  <path d="M20 22 Q24 26 28 22" stroke="#1e1a2a" stroke-width="1.8" fill="none" stroke-linecap="round"/>
</svg>"""

AVATAR_MOD = """<svg viewBox="0 0 48 48" width="36" height="36" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="22" fill="#1a1a1a" stroke="#888" stroke-width="2"/>
  <circle cx="24" cy="18" r="8" fill="#666" opacity="0.9"/>
  <ellipse cx="24" cy="36" rx="12" ry="8" fill="#666" opacity="0.9"/>
  <circle cx="21" cy="18" r="1.2" fill="#1a1a1a"/>
  <circle cx="27" cy="18" r="1.2" fill="#1a1a1a"/>
  <path d="M20 22 Q24 24 28 22" stroke="#1a1a1a" stroke-width="1.5" fill="none" stroke-linecap="round"/>
</svg>"""

# ── Agent definitions ─────────────────────────────────────────────────────────
AGENTS = [
    {
        "name": "Skeptic",
        "color": "#e05c5c",
        "bg": "#2a1515",
        "avatar": AVATAR_SKEPTIC,
        "persona": (
            "You are the Skeptic in a fast group debate chat. Be blunt and sharp. "
            "Challenge weak claims. Max 2 sentences. No pleasantries. Don't talk a lot. "
            "If the Human says something, you can directly call them out by name."
        ),
    },
    {
        "name": "Visionary",
        "color": "#5c9ee0",
        "bg": "#111e2a",
        "avatar": AVATAR_VISIONARY,
        "persona": (
            "You are the Visionary in a fast group debate chat. Be bold and optimistic. "
            "See the big picture others miss. Max 2 sentences. Stay sharp and direct. Don't ramble. "
            "If the Human makes a point, engage with it specifically."
        ),
    },
    {
        "name": "Pragmatist",
        "color": "#5ce08a",
        "bg": "#112215",
        "avatar": AVATAR_PRAGMATIST,
        "persona": (
            "You are the Pragmatist in a fast group debate chat. Focus on what actually works. "
            "Cut through theory with real constraints. Max 2 sentences. Be concrete and direct. Don't waffle. "
            "If the Human raises a point, address it practically."
        ),
    },
]

# Special participants (not in the debate loop, used by state/UI)
MODERATOR = {
    "name": "Moderator",
    "color": "#888",
    "bg": "#1a1a1a",
    "avatar": AVATAR_MOD,
}

JUDGE = {
    "name": "Judge",
    "color": "#c9a84c",
    "bg": "#1a1510",
    "avatar": AVATAR_JUDGE,
}

HUMAN = {
    "name": "You",
    "color": "#a084e8",
    "bg": "#1e1a2a",
    "avatar": AVATAR_HUMAN,
}

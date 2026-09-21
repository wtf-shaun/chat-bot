import re
from datetime import datetime
from .personality_service import analyze_style

# WhatsApp-like formats; a new date-prefixed line starts a message. Other lines continue it.
PATTERNS = [
    re.compile(r"^(?P<date>[^-\n]+?)\s+-\s+(?P<sender>[^:]+):\s?(?P<message>.*)$"),
    re.compile(r"^(?P<date>[^|\n]+?)\s*\|\s*(?P<sender>[^:]+):\s?(?P<message>.*)$"),
]
DATE_FORMATS = ["%d/%m/%Y, %H:%M", "%m/%d/%Y, %H:%M", "%Y-%m-%d %H:%M", "%d/%m/%y, %H:%M"]

def _date(value):
    value = value.strip()
    for fmt in DATE_FORMATS:
        try: return datetime.strptime(value, fmt)
        except ValueError: pass
    return None

def parse_chat(text: str):
    if not text or not text.strip(): return []
    result = []
    current = None
    for line in text.replace("\r\n", "\n").split("\n"):
        match = next((p.match(line) for p in PATTERNS if p.match(line)), None)
        if match:
            if current: result.append(current)
            current = {"timestamp": _date(match.group("date")), "sender": match.group("sender").strip(), "message": match.group("message").strip()}
        elif current and line.strip():
            current["message"] += "\n" + line.strip()
    if current: result.append(current)
    for i, item in enumerate(result, 1): item["message_id"] = i
    return result

def participants(messages): return sorted({m["sender"] for m in messages})

def profile_for(messages, target): return analyze_style([m["message"] for m in messages if m["sender"] == target]).as_dict()

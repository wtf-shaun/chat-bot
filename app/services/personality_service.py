import re
from collections import Counter
from .schemas import StyleProfile

EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF]")
SLANG = {"lol", "lmao", "bro", "nah", "yeah", "yep", "omg", "bruh", "idk", "ngl", "fr"}
ABBREVIATIONS = re.compile(r"\b(?:idk|imo|tbh|ngl|lol|lmao|omg|btw|rn|wyd|wya| asap)\b", re.I)

def analyze_style(messages: list[str]) -> StyleProfile:
    messages = [m.strip() for m in messages if m.strip()]
    if not messages:
        return StyleProfile(0, "unknown", False, False, [], [], "unknown", "unknown", {}, 0, [], [])
    words = re.findall(r"\b[\w']+\b", " ".join(messages).lower())
    word_counts = Counter(words)
    emojis = Counter(e for text in messages for e in EMOJI_RE.findall(text))
    phrases = Counter()
    for text in messages:
        tokens = re.findall(r"\b[\w']+\b", text.lower())
        phrases.update(" ".join(tokens[i:i+2]) for i in range(len(tokens)-1))
    lengths = [len(re.findall(r"\S+", m)) for m in messages]
    lower = sum(m == m.lower() for m in messages) / len(messages)
    slang = sum(w in SLANG for w in words) >= max(1, len(words) // 80)
    return StyleProfile(
        round(sum(len(m) for m in messages) / len(messages), 1),
        "casual" if slang or lower > .55 else "neutral",
        slang, bool(emojis), [e for e, _ in emojis.most_common(8)],
        [p for p, n in phrases.most_common(8) if n > 1],
        "short" if sum(lengths) / len(lengths) < 12 else "medium" if sum(lengths) / len(lengths) <  thirty() else "long",
        "mostly_lowercase" if lower > .65 else "mixed",
        {p: sum(m.count(p) for m in messages) for p in ["!", "?", "...", ","]},
        round(sum("?" in m for m in messages) / len(messages), 3),
        sorted(set(ABBREVIATIONS.findall(" ".join(messages).lower()))),
        [w for w, n in word_counts.most_common(20) if n > 2],
    )

def thirty():
    return 30

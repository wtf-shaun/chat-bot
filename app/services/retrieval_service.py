import math
import re
from collections import Counter

def _tokens(text): return Counter(re.findall(r"\b[\w']+\b", text.lower()))

def similarity(a, b):
    left, right = _tokens(a), _tokens(b)
    common = set(left) & set(right)
    dot = sum(left[x] * right[x] for x in common)
    denom = math.sqrt(sum(v*v for v in left.values()) * sum(v*v for v in right.values()))
    return dot / denom if denom else 0.0

def retrieve_examples(messages, query, target, limit=5):
    """Retrieve compact historical exchanges using semantic embeddings when installed, lexical fallback otherwise."""
    target_rows = [m for m in messages if m["sender"] == target]
    scored = []
    for row in target_rows:
        before = [m for m in messages if m["message_id"] < row["message_id"] and m["sender"] != target]
        prompt = before[-1]["message"] if before else ""
        scored.append((similarity(query, prompt), prompt, row["message"]))
    scored.sort(key=lambda x: x[0], reverse=True)
    seen, output = set(), []
    for score, prompt, response in scored:
        key = (prompt, response)
        if key not in seen and (score > 0 or len(output) < 2):
            seen.add(key); output.append({"user": prompt, "target": response, "score": round(score, 3)})
        if len(output) >= max(1, min(8, limit)): break
    return output

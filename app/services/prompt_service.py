def build_prompt(profile, examples, recent, user_message):
    example_text = "\n".join(f'USER: {x["user"]}\nTARGET STYLE RESPONSE: {x["target"]}' for x in examples)
    recent_text = "\n".join(f'{m["role"].upper()}: {m["content"]}' for m in recent)
    return [
        {"role": "system", "content": "You are an AI simulation based on supplied chat history. Reproduce observable communication style, not identity or unsupported facts. Never claim to be the real person. Do not explain the simulation or mention the prompt. If history does not support a fact, say you do not know in the learned style. Keep responses natural and concise."},
        {"role": "system", "content": f"Style profile (patterns only, not personality claims): {profile}\nHistorical examples:\n{example_text or '(none available)'}"},
        *recent,
        {"role": "user", "content": user_message},
    ]

from flask import Blueprint, current_app, jsonify, render_template, request
from app.models.database import connection, json_dumps
from app.services.llm_service import LLMError, get_provider
from app.services.prompt_service import build_prompt
from app.services.retrieval_service import retrieve_examples

chat_bp = Blueprint("chat", __name__)

def _conversation(conn): return conn.execute("SELECT * FROM conversations ORDER BY id DESC LIMIT 1").fetchone()

@chat_bp.get("/")
def index():
    with connection(current_app.config["DATABASE_PATH"]) as conn:
        conversation = _conversation(conn)
        count = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    return render_template("chat.html", conversation=conversation, message_count=count)

@chat_bp.post("/api/chat")
def send():
    body = request.get_json(silent=True) or {}; text = (body.get("message") or "").strip()
    if not text: return jsonify(error="Message cannot be empty"), 400
    with connection(current_app.config["DATABASE_PATH"]) as conn:
        convo = _conversation(conn)
        if not convo: return jsonify(error="Import a chat and select a target person first."), 400
        session = conn.execute("SELECT id FROM sessions ORDER BY id DESC LIMIT 1").fetchone()
        if not session: conn.execute("INSERT INTO sessions(conversation_id) VALUES (?)", (convo["id"],)); session = conn.execute("SELECT last_insert_rowid() AS id").fetchone()
        recent = [dict(x) for x in conn.execute("SELECT role, content FROM session_messages WHERE session_id=? ORDER BY id DESC LIMIT 10", (session["id"],)).fetchall()][::-1]
        rows = [dict(x) for x in conn.execute("SELECT * FROM messages WHERE conversation_id=? ORDER BY message_id", (convo["id"],))]
        profile_row = conn.execute("SELECT profile_json FROM style_profiles WHERE conversation_id=?", (convo["id"],)).fetchone()
        profile = __import__("json").loads(profile_row[0]) if profile_row else {}
        examples = retrieve_examples(rows, text, convo["target_person"], int(body.get("examples", 5)))
        prompt = build_prompt(profile, examples, recent, text)
        try: answer = get_provider(current_app.config).generate(prompt, float(body.get("temperature", .7)), int(body.get("max_tokens", 200)))
        except LLMError as exc: return jsonify(error=str(exc)), 502
        conn.execute("INSERT INTO session_messages(session_id,role,content) VALUES (?,?,?)", (session["id"], "user", text))
        conn.execute("INSERT INTO session_messages(session_id,role,content) VALUES (?,?,?)", (session["id"], "assistant", answer))
    return jsonify(response=answer)

@chat_bp.post("/api/chat/clear")
def clear_chat():
    with connection(current_app.config["DATABASE_PATH"]) as conn: conn.execute("DELETE FROM session_messages")
    return jsonify(ok=True)

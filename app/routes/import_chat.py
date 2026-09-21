import json
from flask import Blueprint, current_app, jsonify, render_template, request
from app.models.database import connection, json_dumps
from app.services.parser_service import parse_chat, participants, profile_for

import_bp = Blueprint("import", __name__)

@import_bp.get("/import")
def page(): return render_template("import.html")

@import_bp.post("/api/import/preview")
def preview():
    uploaded = request.files.get("file")
    if not uploaded or not uploaded.filename.lower().endswith(".txt"): return jsonify(error="Upload a .txt chat export."), 400
    raw = uploaded.read(current_app.config["MAX_UPLOAD_BYTES"] + 1)
    if len(raw) > current_app.config["MAX_UPLOAD_BYTES"]: return jsonify(error="File is too large (10 MB maximum)."), 400
    messages = parse_chat(raw.decode("utf-8-sig", errors="replace"))
    if not messages: return jsonify(error="No supported messages were found."), 400
    return jsonify(messages=messages[:20], participants=participants(messages), total=len(messages), raw=raw.decode("utf-8-sig", errors="replace"))

@import_bp.post("/api/import/commit")
def commit():
    body = request.get_json(silent=True) or {}; messages = parse_chat(body.get("raw", "")); target = body.get("target")
    if not messages or target not in participants(messages): return jsonify(error="Choose a detected participant."), 400
    with connection(current_app.config["DATABASE_PATH"]) as conn:
        conn.execute("DELETE FROM conversations")
        conn.execute("INSERT INTO conversations(name,target_person) VALUES (?,?)", (body.get("name", "Imported chat"), target))
        cid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.executemany("INSERT INTO messages(conversation_id,message_id,timestamp,sender,message,is_target) VALUES (?,?,?,?,?,?)", [(cid,m["message_id"],m["timestamp"].isoformat() if m["timestamp"] else None,m["sender"],m["message"],int(m["sender"]==target)) for m in messages])
        conn.execute("INSERT INTO style_profiles(conversation_id,target_person,profile_json) VALUES (?,?,?)", (cid,target,json_dumps(profile_for(messages,target))))
    return jsonify(ok=True)

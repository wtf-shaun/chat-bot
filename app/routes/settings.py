from flask import Blueprint, current_app, jsonify, render_template, request
from app.models.database import connection
settings_bp = Blueprint("settings", __name__)
@settings_bp.get("/settings")
def settings(): return render_template("settings.html")
@settings_bp.post("/api/data/clear")
def clear_data():
    with connection(current_app.config["DATABASE_PATH"]) as conn:
        for table in ("session_messages", "sessions", "style_profiles", "messages", "conversations"): conn.execute(f"DELETE FROM {table}")
    return jsonify(ok=True)

# routes/broadcasts.py

from flask import Blueprint, request, jsonify
from db import get_db_connection, release_db_connection
from middleware.auth_middleware import token_required, admin_required
import psycopg2.extras

broadcasts_bp = Blueprint('broadcasts_bp', __name__)

# Any logged-in user can get announcements
@broadcasts_bp.route('', methods=['GET'])
@token_required
def get_broadcasts(current_user):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM broadcasts ORDER BY created_at DESC")
        broadcasts = [dict(row) for row in cur.fetchall()]
        return jsonify(broadcasts)
    finally:
        cur.close()
        release_db_connection(conn)

# Only an admin can create a new announcement
@broadcasts_bp.route('/', methods=['POST'])
@token_required
@admin_required
def add_broadcast(current_user):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute(
            "INSERT INTO broadcasts (message) VALUES (%s) RETURNING *",
            (data['message'],)
        )
        new_broadcast = dict(cur.fetchone())
        conn.commit()
        return jsonify(new_broadcast), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error adding broadcast: {e}"}), 500
    finally:
        cur.close()
        release_db_connection(conn)
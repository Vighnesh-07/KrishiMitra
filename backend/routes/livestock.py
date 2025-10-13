# routes/livestock.py
from flask import Blueprint, request, jsonify
from db import get_db_connection, release_db_connection
from middleware.auth_middleware import token_required
import psycopg2.extras

livestock_bp = Blueprint('livestock_bp', __name__)

@livestock_bp.route('', methods=['GET'])
@token_required
def get_user_livestock(current_user):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM livestock WHERE user_id = %s ORDER BY created_at DESC", (current_user['id'],))
        livestock = [dict(row) for row in cur.fetchall()]
        return jsonify(livestock)
    finally:
        cur.close(), release_db_connection(conn)

@livestock_bp.route('', methods=['POST'])
@token_required
def add_livestock(current_user):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute(
            "INSERT INTO livestock (user_id, animal_type, count, breed, health_status) VALUES (%s, %s, %s, %s, %s) RETURNING *",
            (current_user['id'], data['animal_type'], data['count'], data.get('breed'), data.get('health_status'))
        )
        new_livestock = dict(cur.fetchone())
        conn.commit()
        return jsonify(new_livestock), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error adding livestock: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)

@livestock_bp.route('/<int:item_id>', methods=['PUT'])
@token_required
def update_livestock(current_user, item_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE livestock SET animal_type=%s, count=%s, breed=%s, health_status=%s WHERE id = %s AND user_id = %s",
            (data['animal_type'], data['count'], data.get('breed'), data.get('health_status'), item_id, current_user['id'])
        )
        if cur.rowcount == 0: return jsonify({"message": "Livestock not found or permission denied"}), 404
        conn.commit()
        return jsonify({"message": "Livestock updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error updating livestock: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)

@livestock_bp.route('/<int:item_id>', methods=['DELETE'])
@token_required
def delete_livestock(current_user, item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM livestock WHERE id = %s AND user_id = %s", (item_id, current_user['id']))
        if cur.rowcount == 0: return jsonify({"message": "Livestock not found or permission denied"}), 404
        conn.commit()
        return jsonify({"message": "Livestock deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error deleting livestock: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)
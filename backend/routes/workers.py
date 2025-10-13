# routes/workers.py
from flask import Blueprint, request, jsonify
from db import get_db_connection, release_db_connection
from middleware.auth_middleware import token_required
import psycopg2.extras
from decimal import Decimal

workers_bp = Blueprint('workers_bp', __name__)

def row_to_dict(row):
    d = dict(row)
    for key, value in d.items():
        if isinstance(value, Decimal): d[key] = float(value)
    return d

@workers_bp.route('', methods=['GET'])
@token_required
def get_user_workers(current_user):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM workers WHERE user_id = %s ORDER BY created_at DESC", (current_user['id'],))
        workers = [row_to_dict(row) for row in cur.fetchall()]
        return jsonify(workers)
    finally:
        cur.close(), release_db_connection(conn)

@workers_bp.route('', methods=['POST'])
@token_required
def add_worker(current_user):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute(
            "INSERT INTO workers (user_id, worker_name, role, contact, salary, status) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
            (current_user['id'], data['worker_name'], data.get('role'), data.get('contact'), data.get('salary'), data.get('status'))
        )
        new_worker = row_to_dict(cur.fetchone())
        conn.commit()
        return jsonify(new_worker), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error adding worker: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)

@workers_bp.route('/<int:worker_id>', methods=['PUT'])
@token_required
def update_worker(current_user, worker_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE workers SET worker_name=%s, role=%s, contact=%s, salary=%s, status=%s WHERE id = %s AND user_id = %s",
            (data['worker_name'], data.get('role'), data.get('contact'), data.get('salary'), data.get('status'), worker_id, current_user['id'])
        )
        if cur.rowcount == 0: return jsonify({"message": "Worker not found or permission denied"}), 404
        conn.commit()
        return jsonify({"message": "Worker updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error updating worker: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)

@workers_bp.route('/<int:worker_id>', methods=['DELETE'])
@token_required
def delete_worker(current_user, worker_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM workers WHERE id = %s AND user_id = %s", (worker_id, current_user['id']))
        if cur.rowcount == 0: return jsonify({"message": "Worker not found or permission denied"}), 404
        conn.commit()
        return jsonify({"message": "Worker deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error deleting worker: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)
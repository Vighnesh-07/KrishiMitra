# routes/inventory.py
from flask import Blueprint, request, jsonify
from db import get_db_connection, release_db_connection
from middleware.auth_middleware import token_required
import psycopg2.extras
from decimal import Decimal

inventory_bp = Blueprint('inventory_bp', __name__)

def row_to_dict(row):
    d = dict(row)
    for key, value in d.items():
        if isinstance(value, Decimal): d[key] = float(value)
    return d

@inventory_bp.route('', methods=['GET'])
@token_required
def get_user_inventory(current_user):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM inventory WHERE user_id = %s ORDER BY created_at DESC", (current_user['id'],))
        inventory = [row_to_dict(row) for row in cur.fetchall()]
        return jsonify(inventory)
    finally:
        cur.close(), release_db_connection(conn)

@inventory_bp.route('', methods=['POST'])
@token_required
def add_inventory_item(current_user):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute(
            "INSERT INTO inventory (user_id, item_name, quantity, unit) VALUES (%s, %s, %s, %s) RETURNING *",
            (current_user['id'], data['item_name'], data['quantity'], data['unit'])
        )
        new_item = row_to_dict(cur.fetchone())
        conn.commit()
        return jsonify(new_item), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error adding inventory item: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)

@inventory_bp.route('/<int:item_id>', methods=['PUT'])
@token_required
def update_inventory_item(current_user, item_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE inventory SET item_name=%s, quantity=%s, unit=%s WHERE id = %s AND user_id = %s",
            (data['item_name'], data['quantity'], data['unit'], item_id, current_user['id'])
        )
        if cur.rowcount == 0: return jsonify({"message": "Item not found or permission denied"}), 404
        conn.commit()
        return jsonify({"message": "Inventory item updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error updating item: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)

@inventory_bp.route('/<int:item_id>', methods=['DELETE'])
@token_required
def delete_inventory_item(current_user, item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM inventory WHERE id = %s AND user_id = %s", (item_id, current_user['id']))
        if cur.rowcount == 0: return jsonify({"message": "Item not found or permission denied"}), 404
        conn.commit()
        return jsonify({"message": "Inventory item deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error deleting item: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)
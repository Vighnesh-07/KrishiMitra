# routes/crops.py
from flask import Blueprint, request, jsonify
from db import get_db_connection, release_db_connection
from middleware.auth_middleware import token_required
import psycopg2.extras
from decimal import Decimal

crops_bp = Blueprint('crops_bp', __name__)

def row_to_dict(row):
    d = dict(row)
    for key, value in d.items():
        if isinstance(value, Decimal): d[key] = float(value)
    return d

@crops_bp.route('', methods=['GET'])
@token_required
def get_user_crops(current_user):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM crops WHERE user_id = %s ORDER BY created_at DESC", (current_user['id'],))
        crops = [row_to_dict(row) for row in cur.fetchall()]
        return jsonify(crops)
    finally:
        cur.close(), release_db_connection(conn)

@crops_bp.route('', methods=['POST'])
@token_required
def add_crop(current_user):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute(
            """
            INSERT INTO crops (user_id, crop_name, sowing_date, harvest_date, area, area_unit, harvest_qty, revenue, expenses, wastage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *
            """,
            (current_user['id'], data['crop_name'], data.get('sowing_date'), data.get('harvest_date'), data['area'], data.get('area_unit'), data.get('harvest_qty'), data.get('revenue'), data.get('expenses'), data.get('wastage'))
        )
        new_crop = row_to_dict(cur.fetchone())
        conn.commit()
        return jsonify(new_crop), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error adding crop: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)

@crops_bp.route('/<int:crop_id>', methods=['PUT'])
@token_required
def update_crop(current_user, crop_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM crops WHERE id = %s AND user_id = %s", (crop_id, current_user['id']))
        if cur.fetchone() is None: return jsonify({"message": "Crop not found or permission denied"}), 404
        
        cur.execute(
            """
            UPDATE crops SET crop_name=%s, sowing_date=%s, harvest_date=%s, area=%s, area_unit=%s, harvest_qty=%s, revenue=%s, expenses=%s, wastage=%s
            WHERE id = %s
            """,
            (data['crop_name'], data.get('sowing_date'), data.get('harvest_date'), data['area'], data.get('area_unit'), data.get('harvest_qty'), data.get('revenue'), data.get('expenses'), data.get('wastage'), crop_id)
        )
        conn.commit()
        return jsonify({"message": "Crop updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error updating crop: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)

@crops_bp.route('/<int:crop_id>', methods=['DELETE'])
@token_required
def delete_crop(current_user, crop_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM crops WHERE id = %s AND user_id = %s", (crop_id, current_user['id']))
        if cur.rowcount == 0: return jsonify({"message": "Crop not found or permission denied"}), 404
        conn.commit()
        return jsonify({"message": "Crop deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error deleting crop: {e}"}), 500
    finally:
        cur.close(), release_db_connection(conn)
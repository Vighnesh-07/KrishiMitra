# routes/admin.py

from flask import Blueprint, jsonify
from db import get_db_connection, release_db_connection
from middleware.auth_middleware import token_required, admin_required
import psycopg2.extras
from decimal import Decimal

admin_bp = Blueprint('admin_bp', __name__)

# Helper function to safely convert database rows to dictionaries
def row_to_dict(row):
    d = dict(row)
    for key, value in d.items():
        if isinstance(value, Decimal):
            d[key] = float(value)
    return d

@admin_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_all_users(current_user):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT id, first_name, last_name, email, mobile_number, address FROM users WHERE is_admin = FALSE ORDER BY created_at DESC")
        users = [dict(row) for row in cur.fetchall()]
        cur.close()
        return jsonify(users)
    except Exception as e:
        print(f"Error in /admin/users: {e}")
        return jsonify({"message": "Server error while fetching users"}), 500
    finally:
        if conn:
            release_db_connection(conn)

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user, user_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        if cur.rowcount == 0:
            return jsonify({"message": "User not found"}), 404
        conn.commit()
        cur.close()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Error deleting user: {e}"}), 500
    finally:
        if conn:
            release_db_connection(conn)

@admin_bp.route('/analytics', methods=['GET'])
@token_required
@admin_required
def get_platform_analytics(current_user):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        analytics_data = {}
        
        cur.execute("SELECT COUNT(*) FROM users WHERE is_admin = FALSE;")
        analytics_data['totalUsers'] = cur.fetchone()[0]
        
        cur.execute("SELECT SUM(revenue) as total_revenue, SUM(harvest_qty) as total_harvest FROM crops;")
        kpi_financials = cur.fetchone()
        analytics_data['totalRevenue'] = float(kpi_financials['total_revenue'] or 0)
        analytics_data['totalHarvest'] = float(kpi_financials['total_harvest'] or 0)

        cur.execute("SELECT SUM(count) FROM livestock;")
        analytics_data['totalLivestock'] = cur.fetchone()[0] or 0

        cur.execute("SELECT crop_name, COUNT(*) as count FROM crops GROUP BY crop_name ORDER BY count DESC LIMIT 7;")
        analytics_data['cropDistribution'] = [row_to_dict(row) for row in cur.fetchall()]

        cur.execute("SELECT animal_type, SUM(count) as total_count FROM livestock GROUP BY animal_type;")
        analytics_data['livestockDistribution'] = [row_to_dict(row) for row in cur.fetchall()]
        
        cur.execute("""
            SELECT u.first_name, u.last_name, SUM(c.revenue) as total_revenue FROM crops c 
            JOIN users u ON c.user_id = u.id WHERE c.revenue IS NOT NULL
            GROUP BY u.id, u.first_name, u.last_name ORDER BY total_revenue DESC LIMIT 5;
        """)
        analytics_data['topUsersByRevenue'] = [row_to_dict(row) for row in cur.fetchall()]

        cur.execute("SELECT item_name, SUM(quantity) as total_quantity FROM inventory GROUP BY item_name ORDER BY total_quantity DESC LIMIT 5;")
        analytics_data['inventorySnapshot'] = [row_to_dict(row) for row in cur.fetchall()]

        cur.execute("""
            SELECT TO_CHAR(harvest_date, 'YYYY-MM') as month, SUM(harvest_qty) as total_harvest, SUM(wastage) as total_wastage 
            FROM crops WHERE harvest_date IS NOT NULL GROUP BY month ORDER BY month;
        """)
        analytics_data['harvestVsWastage'] = [row_to_dict(row) for row in cur.fetchall()]

        cur.close()
        return jsonify(analytics_data)
    except Exception as e:
        print(f"Error in /admin/analytics: {e}")
        return jsonify({"message": "Server error while fetching analytics"}), 500
    finally:
        if conn:
            release_db_connection(conn)
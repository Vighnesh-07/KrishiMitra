# routes/auth.py

from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import os
import psycopg2.extras
from db import get_db_connection, release_db_connection

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Basic validation
    if not all(k in data for k in ['firstName', 'lastName', 'email', 'password']):
        return jsonify({"message": "Missing required fields"}), 400

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (first_name, last_name, email, password_hash, mobile_number, address) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (data['firstName'], data['lastName'], data['email'], hashed_password.decode('utf-8'), data.get('mobileNumber'), data.get('address'))
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"message": "User registered successfully", "userId": user_id}), 201
    except psycopg2.Error as e:
        conn.rollback()
        if e.pgcode == '23505': # Unique violation
            return jsonify({"message": "An account with this email already exists."}), 409
        return jsonify({"message": f"Database error: {e.pgerror}"}), 500
    finally:
        cur.close()
        release_db_connection(conn)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400

    conn = get_db_connection()
    # DictCursor allows accessing columns by name
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
        user = cur.fetchone()

        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password_hash'].encode('utf-8')):
            token = jwt.encode(
                {'id': user['id'], 'isAdmin': user['is_admin']},
                os.getenv('JWT_SECRET'),
                algorithm="HS256"
            )
            return jsonify({
                "token": token,
                "user": {
                    "firstName": user['first_name'],
                    "email": user['email'],
                    "isAdmin": user['is_admin']
                }
            })
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    finally:
        cur.close()
        release_db_connection(conn)
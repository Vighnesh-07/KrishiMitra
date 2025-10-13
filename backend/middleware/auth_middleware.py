# middleware/auth_middleware.py

import os
import jwt
from functools import wraps
from flask import request, jsonify

def token_required(f):
    """
    Decorator to ensure a valid JWT is present in the request header.
    It decodes the token and passes the user data to the route.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check if the 'authorization' header is in the request
        if 'authorization' in request.headers:
            # The header format is "Bearer <token>"
            auth_header = request.headers['authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Malformed token header'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Verify the token using the secret key
            user_data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        # Pass the decoded user data to the decorated function
        return f(user_data, *args, **kwargs)

    return decorated


def admin_required(f):
    """
    Decorator to ensure the user is an admin.
    This decorator MUST be used AFTER @token_required.
    """
    @wraps(f)
    def decorated(user_data, *args, **kwargs):
        # The user_data is passed from the @token_required decorator
        if not user_data or not user_data.get('isAdmin'):
            return jsonify({'message': 'Admin access is required for this route!'}), 403 # 403 Forbidden
        
        # If the user is an admin, proceed to the actual route function
        return f(user_data, *args, **kwargs)
    
    return decorated
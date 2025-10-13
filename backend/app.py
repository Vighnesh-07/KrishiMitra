# app.py

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import all your route blueprints
from routes.auth import auth_bp
from routes.crops import crops_bp
from routes.inventory import inventory_bp
from routes.livestock import livestock_bp
from routes.workers import workers_bp
from routes.admin import admin_bp
from routes.broadcasts import broadcasts_bp

# Initialize the Flask App
app = Flask(__name__)

# IMPORTANT: Setup CORS correctly
# This allows your frontend (e.g., from localhost:5500) to talk to your backend (at localhost:5000)
CORS(app)

# Register all the blueprints with their URL prefixes
# Ensure there are NO trailing slashes '/' at the end of the prefixes
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(crops_bp, url_prefix='/api/crops')
app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
app.register_blueprint(livestock_bp, url_prefix='/api/livestock')
app.register_blueprint(workers_bp, url_prefix='/api/workers')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(broadcasts_bp, url_prefix='/api/broadcasts')

# A simple base route to confirm the server is running
@app.route('/')
def index():
    return "KrishiMitra Python Backend is running and ready to accept requests!"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port)
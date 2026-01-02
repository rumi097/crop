"""
Main Flask Application Entry Point
Smart Farming Platform - Organized Architecture
"""
from flask import Flask
from flask_cors import CORS
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

# Import configuration
from config.settings import Config

# Import database initialization
from models.database import init_db

# Import route registrations
from routes.auth_routes import register_auth_routes
from routes.error_handlers import register_error_handlers
from portals import (
    register_farmer_routes,
    register_buyer_routes,
    register_vendor_routes,
    register_labor_routes,
    register_admin_routes,
)

# Import utilities
from utils.auth import create_admin_user
from services.ml_models import load_models


def create_app():
    """Application factory pattern"""
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)  # Enable CORS for React frontend
    
    # Load configuration
    app.config.from_object(Config)
    
    # Create necessary folders
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('saved_models', exist_ok=True)
    
    # Initialize database
    init_db(app)
    
    # Register routes
    register_auth_routes(app)
    register_farmer_routes(app)
    register_buyer_routes(app)
    register_vendor_routes(app)
    register_labor_routes(app)
    register_admin_routes(app)
    register_error_handlers(app)
    
    return app


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Create default admin user
        try:
            from models.database import db
            create_admin_user(
                db,
                email='admin@smartfarming.com',
                password='admin123',
                full_name='System Administrator'
            )
        except Exception as e:
            print(f"Admin creation note: {e}")
        
        # Load ML models
        load_models()
    
    print("=" * 60)
    print("🌾 Smart Farming Platform API")
    print("=" * 60)
    print("✓ Multi-role system: Farmer, Buyer, Vendor, Labor, Admin")
    print("✓ Database: SQLite (smart_farming.db)")
    print("✓ Default admin: admin@smartfarming.com / admin123")
    print("=" * 60)
    
    # Run the application
    app.run(debug=False, host='0.0.0.0', port=5001)

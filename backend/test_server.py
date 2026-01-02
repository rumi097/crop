"""
Simple test server to verify authentication endpoints
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from models.database import db, init_db, User, UserRole
from utils.auth import generate_token

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'test-secret-key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "smart_farming.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

@app.route('/')
def home():
    return jsonify({'message': 'Test Server Running'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        token = generate_token(user.id, user.role)
        
        return jsonify({
            'success': True,
            'token': token,
            'user': user.to_dict()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['email', 'password', 'full_name', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Validate role
        try:
            role = UserRole(data['role'])
        except ValueError:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Create user
        user = User(
            email=data['email'],
            full_name=data['full_name'],
            phone=data.get('phone'),
            address=data.get('address'),
            role=role,
            is_verified=(role == UserRole.BUYER)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = generate_token(user.id, user.role)
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'token': token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 Test Server for Authentication")
    print("=" * 60)
    print("✓ Endpoints: /api/auth/login, /api/auth/register")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=5001)

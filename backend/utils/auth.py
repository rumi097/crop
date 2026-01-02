"""
Authentication utilities for Smart Farming Platform
Handles JWT token generation, validation, and role-based access control
"""

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from models.database import User, UserRole
import os


# JWT Configuration
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


def generate_token(user_id, role):
    """Generate JWT token for authenticated user"""
    payload = {
        'user_id': user_id,
        'role': role.value if isinstance(role, UserRole) else role,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token):
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}


def get_token_from_header():
    """Extract token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        # Format: "Bearer <token>"
        parts = auth_header.split()
        if parts[0].lower() != 'bearer':
            return None
        if len(parts) == 1:
            return None
        elif len(parts) > 2:
            return None
        return parts[1]
    except Exception:
        return None


def login_required(f):
    """Decorator to require authentication for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        payload = decode_token(token)
        
        if 'error' in payload:
            return jsonify({'error': payload['error']}), 401
        
        # Attach user info to request context
        request.current_user = {
            'user_id': payload['user_id'],
            'role': payload['role']
        }
        
        return f(*args, **kwargs)
    
    return decorated_function


def role_required(*allowed_roles):
    """Decorator to require specific role(s) for endpoints"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_header()
            
            if not token:
                return jsonify({'error': 'Authentication token is missing'}), 401
            
            payload = decode_token(token)
            
            if 'error' in payload:
                return jsonify({'error': payload['error']}), 401
            
            user_role = payload.get('role')
            
            # Convert string roles to list for comparison
            allowed_role_values = [role.value if isinstance(role, UserRole) else role for role in allowed_roles]
            
            if user_role not in allowed_role_values:
                return jsonify({
                    'error': 'Access denied. Insufficient permissions.',
                    'required_roles': allowed_role_values,
                    'user_role': user_role
                }), 403
            
            # Attach user info to request context
            request.current_user = {
                'user_id': payload['user_id'],
                'role': user_role
            }
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def get_current_user():
    """Get current authenticated user from request context"""
    return getattr(request, 'current_user', None)


def create_admin_user(db, email, password, full_name):
    """Utility function to create admin user"""
    from models.database import User, UserRole
    
    # Check if admin already exists
    existing_admin = User.query.filter_by(email=email).first()
    if existing_admin:
        print(f"Admin user {email} already exists")
        return existing_admin
    
    # Create new admin
    admin = User(
        email=email,
        full_name=full_name,
        role=UserRole.ADMIN,
        is_verified=True,
        is_active=True
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"✓ Admin user created: {email}")
    return admin

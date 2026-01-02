"""
Authentication and Public Routes
Handles user registration, login, and public endpoints
"""
from flask import request, jsonify
from datetime import datetime
from models.database import (
    db, User, UserRole, FarmerProfile, VendorProfile, LaborProfile,
    CropListing, VendorProduct
)
from utils.auth import generate_token, login_required, get_current_user


def register_auth_routes(app):
    """Register authentication and public routes"""
    
    @app.route('/')
    def home():
        """Home endpoint"""
        return jsonify({
            'message': 'Smart Farming Platform API',
            'version': '2.0',
            'features': [
                'Multi-role authentication',
                'Farmer portal with recommendations and marketplace',
                'Buyer portal for purchasing',
                'Vendor portal for agricultural inputs',
                'Labor portal for job opportunities',
                'Admin portal for platform management'
            ]
        })
    
    @app.route('/api/public/products', methods=['GET'])
    def get_public_products():
        """Get all public products (crops, vendor products) for landing page"""
        try:
            # Get query parameters
            category = request.args.get('category', None)
            search = request.args.get('search', '')
            limit = int(request.args.get('limit', 20))
            
            # Get crop listings
            crop_query = CropListing.query.filter_by(is_available=True)
            if category and category != 'all':
                crop_query = crop_query.filter_by(category=category)
            if search:
                crop_query = crop_query.filter(CropListing.crop_name.ilike(f'%{search}%'))
            crops = crop_query.limit(limit).all()
            
            # Get vendor products
            product_query = VendorProduct.query.filter_by(is_available=True)
            if category and category != 'all':
                product_query = product_query.filter_by(category=category)
            if search:
                product_query = product_query.filter(VendorProduct.product_name.ilike(f'%{search}%'))
            products = product_query.limit(limit).all()
            
            return jsonify({
                'success': True,
                'crops': [crop.to_dict() for crop in crops],
                'vendor_products': [product.to_dict() for product in products],
                'total_count': len(crops) + len(products)
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/public/labor-listings', methods=['GET'])
    def get_public_labor_listings():
        """Get available labor for landing page"""
        try:
            labor_profiles = LaborProfile.query.filter_by(availability=True).limit(20).all()
            
            results = []
            for profile in labor_profiles:
                user = User.query.get(profile.user_id)
                results.append({
                    'id': profile.id,
                    'full_name': user.full_name,
                    'skills': profile.skills,
                    'experience_years': profile.experience_years,
                    'daily_wage': profile.daily_wage,
                    'rating': profile.rating,
                    'phone': user.phone
                })
            
            return jsonify({'success': True, 'labor': results})
        
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
                is_verified=(role == UserRole.BUYER)  # Buyers auto-verified
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            # Create role-specific profile
            if role == UserRole.FARMER:
                farmer_profile = FarmerProfile(
                    user_id=user.id,
                    farm_name=data.get('farm_name'),
                    farm_size=data.get('farm_size'),
                    farm_location=data.get('farm_location')
                )
                db.session.add(farmer_profile)
            
            elif role == UserRole.VENDOR:
                vendor_profile = VendorProfile(
                    user_id=user.id,
                    business_name=data.get('business_name', ''),
                    business_license=data.get('business_license')
                )
                db.session.add(vendor_profile)
            
            elif role == UserRole.LABOR:
                labor_profile = LaborProfile(
                    user_id=user.id,
                    skills=data.get('skills'),
                    experience_years=data.get('experience_years', 0),
                    daily_wage=data.get('daily_wage', 0)
                )
                db.session.add(labor_profile)
            
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
    
    @app.route('/api/auth/profile', methods=['GET'])
    @login_required
    def get_profile():
        """Get current user profile"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            profile_data = user.to_dict()
            
            # Add role-specific profile data
            if user.role == UserRole.FARMER and user.farmer_profile:
                profile_data['farmer_profile'] = {
                    'farm_name': user.farmer_profile.farm_name,
                    'farm_size': user.farmer_profile.farm_size,
                    'farm_location': user.farmer_profile.farm_location,
                    'soil_type': user.farmer_profile.soil_type
                }
            elif user.role == UserRole.VENDOR and user.vendor_profile:
                profile_data['vendor_profile'] = {
                    'business_name': user.vendor_profile.business_name,
                    'rating': user.vendor_profile.rating,
                    'total_sales': user.vendor_profile.total_sales
                }
            elif user.role == UserRole.LABOR and user.labor_profile:
                profile_data['labor_profile'] = {
                    'skills': user.labor_profile.skills,
                    'experience_years': user.labor_profile.experience_years,
                    'daily_wage': user.labor_profile.daily_wage,
                    'rating': user.labor_profile.rating,
                    'availability': user.labor_profile.availability
                }
            
            return jsonify({'success': True, 'user': profile_data})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/auth/profile', methods=['PUT'])
    @login_required
    def update_profile():
        """Update current user profile (except email)"""
        try:
            current_user = get_current_user()
            user = User.query.get(current_user['user_id'])
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            data = request.json
            
            # Update basic user info (except email)
            if 'full_name' in data:
                user.full_name = data['full_name']
            if 'phone' in data:
                user.phone = data['phone']
            if 'address' in data:
                user.address = data['address']
            
            # Update role-specific profile data
            if user.role == UserRole.FARMER and user.farmer_profile:
                if 'farm_name' in data:
                    user.farmer_profile.farm_name = data['farm_name']
                if 'farm_size' in data:
                    user.farmer_profile.farm_size = data['farm_size']
                if 'farm_location' in data:
                    user.farmer_profile.farm_location = data['farm_location']
                if 'soil_type' in data:
                    user.farmer_profile.soil_type = data['soil_type']
                if 'irrigation_type' in data:
                    user.farmer_profile.irrigation_type = data['irrigation_type']
            
            elif user.role == UserRole.VENDOR and user.vendor_profile:
                if 'business_name' in data:
                    user.vendor_profile.business_name = data['business_name']
                if 'business_license' in data:
                    user.vendor_profile.business_license = data['business_license']
            
            elif user.role == UserRole.LABOR and user.labor_profile:
                if 'skills' in data:
                    user.labor_profile.skills = data['skills']
                if 'experience_years' in data:
                    user.labor_profile.experience_years = data['experience_years']
                if 'daily_wage' in data:
                    user.labor_profile.daily_wage = data['daily_wage']
                if 'availability' in data:
                    user.labor_profile.availability = data['availability']
            
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Return updated profile
            profile_data = user.to_dict()
            if user.role == UserRole.FARMER and user.farmer_profile:
                profile_data['farmer_profile'] = {
                    'farm_name': user.farmer_profile.farm_name,
                    'farm_size': user.farmer_profile.farm_size,
                    'farm_location': user.farmer_profile.farm_location,
                    'soil_type': user.farmer_profile.soil_type,
                    'irrigation_type': user.farmer_profile.irrigation_type
                }
            elif user.role == UserRole.VENDOR and user.vendor_profile:
                profile_data['vendor_profile'] = {
                    'business_name': user.vendor_profile.business_name,
                    'business_license': user.vendor_profile.business_license,
                    'rating': user.vendor_profile.rating,
                    'total_sales': user.vendor_profile.total_sales
                }
            elif user.role == UserRole.LABOR and user.labor_profile:
                profile_data['labor_profile'] = {
                    'skills': user.labor_profile.skills,
                    'experience_years': user.labor_profile.experience_years,
                    'daily_wage': user.labor_profile.daily_wage,
                    'rating': user.labor_profile.rating,
                    'availability': user.labor_profile.availability
                }
            
            return jsonify({'success': True, 'user': profile_data, 'message': 'Profile updated successfully'})
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

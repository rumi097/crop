"""
Database models for Smart Farming Platform
Multi-purpose agricultural system with role-based access
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import enum

db = SQLAlchemy()


class UserRole(enum.Enum):
    """User role types in the system"""
    FARMER = "farmer"
    BUYER = "buyer"
    VENDOR = "vendor"
    LABOR = "labor"
    ADMIN = "admin"


class OrderStatus(enum.Enum):
    """Order status types"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class User(db.Model):
    """Base user model for all user types"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.Enum(UserRole), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farmer_profile = db.relationship('FarmerProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    vendor_profile = db.relationship('VendorProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    labor_profile = db.relationship('LaborProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'role': self.role.value,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class FarmerProfile(db.Model):
    """Extended profile for farmers"""
    __tablename__ = 'farmer_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    farm_name = db.Column(db.String(200))
    farm_size = db.Column(db.Float)  # in acres/hectares
    farm_location = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    soil_type = db.Column(db.String(50))
    irrigation_type = db.Column(db.String(50))
    
    # Relationships
    user = db.relationship('User', back_populates='farmer_profile')
    crop_listings = db.relationship('CropListing', back_populates='farmer', cascade='all, delete-orphan')
    cost_records = db.relationship('CostRecord', back_populates='farmer', cascade='all, delete-orphan')
    labor_hiring = db.relationship('LaborHiring', back_populates='farmer', cascade='all, delete-orphan')
    equipment_owned = db.relationship('Equipment', back_populates='owner', cascade='all, delete-orphan')
    recommendation_history = db.relationship('RecommendationHistory', back_populates='farmer', cascade='all, delete-orphan')


class VendorProfile(db.Model):
    """Extended profile for vendors"""
    __tablename__ = 'vendor_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    business_name = db.Column(db.String(200), nullable=False)
    business_license = db.Column(db.String(100))
    rating = db.Column(db.Float, default=0.0)
    total_sales = db.Column(db.Integer, default=0)
    
    # Relationships
    user = db.relationship('User', back_populates='vendor_profile')
    products = db.relationship('VendorProduct', back_populates='vendor', cascade='all, delete-orphan')


class LaborProfile(db.Model):
    """Extended profile for labor/workers"""
    __tablename__ = 'labor_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    skills = db.Column(db.Text)  # JSON string of skills
    experience_years = db.Column(db.Integer)
    daily_wage = db.Column(db.Float)
    availability = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    
    # Relationships
    user = db.relationship('User', back_populates='labor_profile')
    work_history = db.relationship('LaborHiring', back_populates='labor', cascade='all, delete-orphan')


class CropListing(db.Model):
    """Crops listed by farmers for sale"""
    __tablename__ = 'crop_listings'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # vegetables, fruits, grains, etc.
    quantity = db.Column(db.Float, nullable=False)  # in kg or tons
    unit = db.Column(db.String(20), default='kg')
    price_per_unit = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(255))  # Specific location for this listing
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    harvest_date = db.Column(db.Date)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    farmer = db.relationship('FarmerProfile', back_populates='crop_listings')
    orders = db.relationship('Order', back_populates='crop_listing')
    
    def to_dict(self):
        """Convert to dictionary"""
        farmer_user = User.query.get(self.farmer.user_id) if self.farmer else None
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'farmer_name': farmer_user.full_name if farmer_user else 'Unknown',
            'farm_name': self.farmer.farm_name if self.farmer else 'Unknown Farm',
            'farmer_location': self.farmer.farm_location if self.farmer else 'Location not specified',
            'crop_name': self.crop_name,
            'category': self.category,
            'quantity': self.quantity,
            'unit': self.unit,
            'price_per_unit': self.price_per_unit,
            'location': self.location,  # Specific listing location
            'description': self.description,
            'image_url': self.image_url,
            'harvest_date': self.harvest_date.isoformat() if self.harvest_date else None,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat()
        }


class VendorProduct(db.Model):
    """Agricultural inputs sold by vendors"""
    __tablename__ = 'vendor_products'
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor_profiles.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))  # seeds, fertilizers, tools, pesticides
    brand = db.Column(db.String(100))
    quantity_available = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='unit')
    price_per_unit = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    specifications = db.Column(db.Text)  # JSON string
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    vendor = db.relationship('VendorProfile', back_populates='products')
    orders = db.relationship('Order', back_populates='vendor_product')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'product_name': self.product_name,
            'category': self.category,
            'brand': self.brand,
            'quantity_available': self.quantity_available,
            'unit': self.unit,
            'price_per_unit': self.price_per_unit,
            'description': self.description,
            'image_url': self.image_url,
            'specifications': self.specifications,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat()
        }


class Order(db.Model):
    """Orders placed by buyers"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_type = db.Column(db.String(20))  # crop, vendor_product
    crop_listing_id = db.Column(db.Integer, db.ForeignKey('crop_listings.id'), nullable=True)
    vendor_product_id = db.Column(db.Integer, db.ForeignKey('vendor_products.id'), nullable=True)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    is_contract_farming = db.Column(db.Boolean, default=False)
    delivery_date = db.Column(db.Date)
    delivery_address = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    buyer = db.relationship('User', foreign_keys=[buyer_id])
    crop_listing = db.relationship('CropListing', back_populates='orders')
    vendor_product = db.relationship('VendorProduct', back_populates='orders')
    payments = db.relationship('Payment', back_populates='order', cascade='all, delete-orphan')


class Payment(db.Model):
    """Payment records for orders"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # cash, card, upi, bank_transfer
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    transaction_id = db.Column(db.String(100))
    payment_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', back_populates='payments')


class CostRecord(db.Model):
    """Farming cost tracking for farmers"""
    __tablename__ = 'cost_records'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(50))  # Kharif, Rabi, Zaid
    year = db.Column(db.Integer, nullable=False)
    
    # Cost breakdown
    seed_cost = db.Column(db.Float, default=0.0)
    fertilizer_cost = db.Column(db.Float, default=0.0)
    pesticide_cost = db.Column(db.Float, default=0.0)
    labor_cost = db.Column(db.Float, default=0.0)
    equipment_cost = db.Column(db.Float, default=0.0)
    irrigation_cost = db.Column(db.Float, default=0.0)
    other_cost = db.Column(db.Float, default=0.0)
    total_cost = db.Column(db.Float, default=0.0)
    
    # Revenue
    revenue = db.Column(db.Float, default=0.0)
    profit_loss = db.Column(db.Float, default=0.0)
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farmer = db.relationship('FarmerProfile', back_populates='cost_records')


class LaborHiring(db.Model):
    """Labor hiring and work records"""
    __tablename__ = 'labor_hiring'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    labor_id = db.Column(db.Integer, db.ForeignKey('labor_profiles.id'), nullable=True)
    job_title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    work_type = db.Column(db.String(50))  # planting, harvesting, irrigation, etc.
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    total_days = db.Column(db.Integer, default=0)
    daily_wage = db.Column(db.Float, nullable=True)
    total_wage = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(200))  # Work location
    laborers_needed = db.Column(db.Integer, default=1)  # Number of workers needed
    status = db.Column(db.String(20), default='open')  # open, active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    farmer = db.relationship('FarmerProfile', back_populates='labor_hiring')
    labor = db.relationship('LaborProfile', back_populates='work_history')


class Equipment(db.Model):
    """Farm equipment owned by farmers (for sharing/renting)"""
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    equipment_name = db.Column(db.String(200), nullable=False)
    equipment_type = db.Column(db.String(50))  # tractor, harvester, sprayer, etc.
    description = db.Column(db.Text)
    rental_price_per_day = db.Column(db.Float)
    is_available_for_rent = db.Column(db.Boolean, default=False)
    is_available_for_share = db.Column(db.Boolean, default=False)
    condition = db.Column(db.String(20))  # excellent, good, fair
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('FarmerProfile', back_populates='equipment_owned')
    rentals = db.relationship('EquipmentRental', back_populates='equipment', cascade='all, delete-orphan')


class EquipmentRental(db.Model):
    """Equipment rental transactions"""
    __tablename__ = 'equipment_rentals'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    renter_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    rental_rate = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    equipment = db.relationship('Equipment', back_populates='rentals')
    renter = db.relationship('FarmerProfile', foreign_keys=[renter_id])


class RecommendationHistory(db.Model):
    """History of crop and fertilizer recommendations for farmers"""
    __tablename__ = 'recommendation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    recommendation_type = db.Column(db.String(20))  # crop or fertilizer
    
    # Input parameters (JSON string)
    input_parameters = db.Column(db.Text, nullable=False)
    
    # Results
    recommendation_result = db.Column(db.Text, nullable=False)
    confidence_score = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    farmer = db.relationship('FarmerProfile', back_populates='recommendation_history')


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully")

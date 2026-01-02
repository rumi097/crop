"""
Comprehensive data population script for all portals
Adds 5-10 sample data entries for Farmer, Buyer, Labor, Vendor, and Admin portals
"""

import sys
from datetime import datetime, timedelta, date
from app import app
from models.database import (
    db, User, UserRole, FarmerProfile, VendorProfile, LaborProfile,
    CropListing, VendorProduct, Order, OrderStatus, Payment, CostRecord,
    LaborHiring, Equipment, EquipmentRental, RecommendationHistory
)
import json
import random

def clear_all_data():
    """Clear existing data (optional - use with caution)"""
    print("Clearing existing data...")
    with app.app_context():
        # Delete in correct order to respect foreign keys
        RecommendationHistory.query.delete()
        EquipmentRental.query.delete()
        Equipment.query.delete()
        Payment.query.delete()
        Order.query.delete()
        LaborHiring.query.delete()
        CostRecord.query.delete()
        VendorProduct.query.delete()
        CropListing.query.delete()
        FarmerProfile.query.delete()
        VendorProfile.query.delete()
        LaborProfile.query.delete()
        User.query.delete()
        db.session.commit()
        print("✓ All data cleared")

def create_users():
    """Create sample users for all roles"""
    print("\n1. Creating users...")
    
    users_data = [
        # Farmers (10 users)
        {'email': 'farmer1@farm.com', 'password': 'pass123', 'full_name': 'Rajesh Kumar', 'phone': '9876543210', 
         'address': 'Village Ramnagar, Punjab', 'role': UserRole.FARMER},
        {'email': 'farmer2@farm.com', 'password': 'pass123', 'full_name': 'Suresh Patil', 'phone': '9876543211',
         'address': 'Village Shirpur, Maharashtra', 'role': UserRole.FARMER},
        {'email': 'farmer3@farm.com', 'password': 'pass123', 'full_name': 'Ramesh Singh', 'phone': '9876543212',
         'address': 'Village Chandpur, Uttar Pradesh', 'role': UserRole.FARMER},
        {'email': 'farmer4@farm.com', 'password': 'pass123', 'full_name': 'Mahesh Reddy', 'phone': '9876543213',
         'address': 'Village Nalgonda, Telangana', 'role': UserRole.FARMER},
        {'email': 'farmer5@farm.com', 'password': 'pass123', 'full_name': 'Prakash Yadav', 'phone': '9876543214',
         'address': 'Village Rohtak, Haryana', 'role': UserRole.FARMER},
        {'email': 'farmer6@farm.com', 'password': 'pass123', 'full_name': 'Vijay Sharma', 'phone': '9876543215',
         'address': 'Village Jaipur, Rajasthan', 'role': UserRole.FARMER},
        {'email': 'farmer7@farm.com', 'password': 'pass123', 'full_name': 'Anil Desai', 'phone': '9876543216',
         'address': 'Village Surat, Gujarat', 'role': UserRole.FARMER},
        {'email': 'farmer8@farm.com', 'password': 'pass123', 'full_name': 'Krishna Naik', 'phone': '9876543217',
         'address': 'Village Dharwad, Karnataka', 'role': UserRole.FARMER},
        {'email': 'farmer9@farm.com', 'password': 'pass123', 'full_name': 'Ganesh Rao', 'phone': '9876543218',
         'address': 'Village Visakhapatnam, Andhra Pradesh', 'role': UserRole.FARMER},
        {'email': 'farmer10@farm.com', 'password': 'pass123', 'full_name': 'Deepak Verma', 'phone': '9876543219',
         'address': 'Village Lucknow, Uttar Pradesh', 'role': UserRole.FARMER},
        
        # Buyers (8 users)
        {'email': 'buyer1@market.com', 'password': 'pass123', 'full_name': 'Amit Wholesaler', 'phone': '9123456780',
         'address': 'Market Road, Delhi', 'role': UserRole.BUYER},
        {'email': 'buyer2@market.com', 'password': 'pass123', 'full_name': 'Priya Traders', 'phone': '9123456781',
         'address': 'Gandhi Market, Mumbai', 'role': UserRole.BUYER},
        {'email': 'buyer3@market.com', 'password': 'pass123', 'full_name': 'Rohan Export House', 'phone': '9123456782',
         'address': 'Export Zone, Bangalore', 'role': UserRole.BUYER},
        {'email': 'buyer4@market.com', 'password': 'pass123', 'full_name': 'Sneha Food Corp', 'phone': '9123456783',
         'address': 'Food Street, Hyderabad', 'role': UserRole.BUYER},
        {'email': 'buyer5@market.com', 'password': 'pass123', 'full_name': 'Vikram Agro Buyers', 'phone': '9123456784',
         'address': 'Market Complex, Chennai', 'role': UserRole.BUYER},
        {'email': 'buyer6@market.com', 'password': 'pass123', 'full_name': 'Kavita Retail Chain', 'phone': '9123456785',
         'address': 'Sector 5, Pune', 'role': UserRole.BUYER},
        {'email': 'buyer7@market.com', 'password': 'pass123', 'full_name': 'Rajesh Grocery Hub', 'phone': '9123456786',
         'address': 'Market Area, Kolkata', 'role': UserRole.BUYER},
        {'email': 'buyer8@market.com', 'password': 'pass123', 'full_name': 'Meera Organic Store', 'phone': '9123456787',
         'address': 'Green Plaza, Ahmedabad', 'role': UserRole.BUYER},
        
        # Vendors (7 users)
        {'email': 'vendor1@supply.com', 'password': 'pass123', 'full_name': 'Green Seeds Co', 'phone': '9234567890',
         'address': 'Industrial Area, Ludhiana', 'role': UserRole.VENDOR},
        {'email': 'vendor2@supply.com', 'password': 'pass123', 'full_name': 'FertilizerPro Ltd', 'phone': '9234567891',
         'address': 'Chemical Zone, Vadodara', 'role': UserRole.VENDOR},
        {'email': 'vendor3@supply.com', 'password': 'pass123', 'full_name': 'AgriTools India', 'phone': '9234567892',
         'address': 'Tool Market, Coimbatore', 'role': UserRole.VENDOR},
        {'email': 'vendor4@supply.com', 'password': 'pass123', 'full_name': 'BioFert Solutions', 'phone': '9234567893',
         'address': 'Biotech Park, Pune', 'role': UserRole.VENDOR},
        {'email': 'vendor5@supply.com', 'password': 'pass123', 'full_name': 'Pesticide Plus', 'phone': '9234567894',
         'address': 'Agri Complex, Nagpur', 'role': UserRole.VENDOR},
        {'email': 'vendor6@supply.com', 'password': 'pass123', 'full_name': 'Irrigation Systems Co', 'phone': '9234567895',
         'address': 'Tech Hub, Jaipur', 'role': UserRole.VENDOR},
        {'email': 'vendor7@supply.com', 'password': 'pass123', 'full_name': 'Farm Equipment Depot', 'phone': '9234567896',
         'address': 'Machinery Market, Indore', 'role': UserRole.VENDOR},
        
        # Labor (10 users)
        {'email': 'labor1@work.com', 'password': 'pass123', 'full_name': 'Mohan Worker', 'phone': '9345678901',
         'address': 'Labor Colony, Punjab', 'role': UserRole.LABOR},
        {'email': 'labor2@work.com', 'password': 'pass123', 'full_name': 'Ravi Laborer', 'phone': '9345678902',
         'address': 'Worker Street, Haryana', 'role': UserRole.LABOR},
        {'email': 'labor3@work.com', 'password': 'pass123', 'full_name': 'Sanjay Helper', 'phone': '9345678903',
         'address': 'Daily Wage Area, UP', 'role': UserRole.LABOR},
        {'email': 'labor4@work.com', 'password': 'pass123', 'full_name': 'Kumar Field Worker', 'phone': '9345678904',
         'address': 'Farm Area, Bihar', 'role': UserRole.LABOR},
        {'email': 'labor5@work.com', 'password': 'pass123', 'full_name': 'Shankar Harvester', 'phone': '9345678905',
         'address': 'Village Center, MP', 'role': UserRole.LABOR},
        {'email': 'labor6@work.com', 'password': 'pass123', 'full_name': 'Dinesh Farm Hand', 'phone': '9345678906',
         'address': 'Rural Area, Rajasthan', 'role': UserRole.LABOR},
        {'email': 'labor7@work.com', 'password': 'pass123', 'full_name': 'Sunil Planter', 'phone': '9345678907',
         'address': 'Village Square, Gujarat', 'role': UserRole.LABOR},
        {'email': 'labor8@work.com', 'password': 'pass123', 'full_name': 'Manoj Irrigator', 'phone': '9345678908',
         'address': 'Farm Colony, Maharashtra', 'role': UserRole.LABOR},
        {'email': 'labor9@work.com', 'password': 'pass123', 'full_name': 'Ajay Skilled Worker', 'phone': '9345678909',
         'address': 'Labor Hub, Karnataka', 'role': UserRole.LABOR},
        {'email': 'labor10@work.com', 'password': 'pass123', 'full_name': 'Pawan General Helper', 'phone': '9345678910',
         'address': 'Worker Zone, Telangana', 'role': UserRole.LABOR},
        
        # Admin (1 user)
        {'email': 'admin@smartfarm.com', 'password': 'admin123', 'full_name': 'System Administrator', 'phone': '9999999999',
         'address': 'Head Office, New Delhi', 'role': UserRole.ADMIN}
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            email=user_data['email'],
            full_name=user_data['full_name'],
            phone=user_data['phone'],
            address=user_data['address'],
            role=user_data['role'],
            is_verified=True,
            is_active=True
        )
        user.set_password(user_data['password'])
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    print(f"✓ Created {len(users)} users")
    return users

def create_farmer_profiles(users):
    """Create farmer profiles with farm details"""
    print("\n2. Creating farmer profiles...")
    
    farmers = [u for u in users if u.role == UserRole.FARMER]
    
    farm_data = [
        {'farm_name': 'Green Valley Farm', 'farm_size': 25.5, 'farm_location': 'Ramnagar, Punjab', 
         'soil_type': 'Alluvial', 'irrigation_type': 'Canal'},
        {'farm_name': 'Sunrise Agriculture', 'farm_size': 18.0, 'farm_location': 'Shirpur, Maharashtra',
         'soil_type': 'Black Cotton', 'irrigation_type': 'Drip'},
        {'farm_name': 'Golden Harvest Fields', 'farm_size': 30.0, 'farm_location': 'Chandpur, UP',
         'soil_type': 'Loamy', 'irrigation_type': 'Tube well'},
        {'farm_name': 'Organic Paradise', 'farm_size': 15.5, 'farm_location': 'Nalgonda, Telangana',
         'soil_type': 'Red Sandy', 'irrigation_type': 'Sprinkler'},
        {'farm_name': 'Nature\'s Bounty', 'farm_size': 22.0, 'farm_location': 'Rohtak, Haryana',
         'soil_type': 'Sandy Loam', 'irrigation_type': 'Canal'},
        {'farm_name': 'Royal Farms', 'farm_size': 28.5, 'farm_location': 'Jaipur, Rajasthan',
         'soil_type': 'Desert Soil', 'irrigation_type': 'Drip'},
        {'farm_name': 'Green Gold Estate', 'farm_size': 20.0, 'farm_location': 'Surat, Gujarat',
         'soil_type': 'Alluvial', 'irrigation_type': 'Sprinkler'},
        {'farm_name': 'Harvest Hub', 'farm_size': 32.0, 'farm_location': 'Dharwad, Karnataka',
         'soil_type': 'Red Laterite', 'irrigation_type': 'Tube well'},
        {'farm_name': 'Fertile Acres', 'farm_size': 26.5, 'farm_location': 'Visakhapatnam, AP',
         'soil_type': 'Coastal Alluvial', 'irrigation_type': 'Canal'},
        {'farm_name': 'Premium Crops Farm', 'farm_size': 19.0, 'farm_location': 'Lucknow, UP',
         'soil_type': 'Loamy', 'irrigation_type': 'Tube well'}
    ]
    
    for i, farmer in enumerate(farmers):
        profile = FarmerProfile(
            user_id=farmer.id,
            farm_name=farm_data[i]['farm_name'],
            farm_size=farm_data[i]['farm_size'],
            farm_location=farm_data[i]['farm_location'],
            latitude=random.uniform(20.0, 32.0),
            longitude=random.uniform(72.0, 85.0),
            soil_type=farm_data[i]['soil_type'],
            irrigation_type=farm_data[i]['irrigation_type']
        )
        db.session.add(profile)
    
    db.session.commit()
    print(f"✓ Created {len(farmers)} farmer profiles")

def create_vendor_profiles(users):
    """Create vendor profiles with business details"""
    print("\n3. Creating vendor profiles...")
    
    vendors = [u for u in users if u.role == UserRole.VENDOR]
    
    business_data = [
        {'business_name': 'Green Seeds Co', 'business_license': 'LIC001', 'rating': 4.5},
        {'business_name': 'FertilizerPro Ltd', 'business_license': 'LIC002', 'rating': 4.7},
        {'business_name': 'AgriTools India', 'business_license': 'LIC003', 'rating': 4.3},
        {'business_name': 'BioFert Solutions', 'business_license': 'LIC004', 'rating': 4.8},
        {'business_name': 'Pesticide Plus', 'business_license': 'LIC005', 'rating': 4.2},
        {'business_name': 'Irrigation Systems Co', 'business_license': 'LIC006', 'rating': 4.6},
        {'business_name': 'Farm Equipment Depot', 'business_license': 'LIC007', 'rating': 4.4}
    ]
    
    for i, vendor in enumerate(vendors):
        profile = VendorProfile(
            user_id=vendor.id,
            business_name=business_data[i]['business_name'],
            business_license=business_data[i]['business_license'],
            rating=business_data[i]['rating'],
            total_sales=random.randint(50, 500)
        )
        db.session.add(profile)
    
    db.session.commit()
    print(f"✓ Created {len(vendors)} vendor profiles")

def create_labor_profiles(users):
    """Create labor profiles with skills and experience"""
    print("\n4. Creating labor profiles...")
    
    laborers = [u for u in users if u.role == UserRole.LABOR]
    
    skills_list = [
        'Planting, Harvesting, Irrigation',
        'Tractor Operation, Plowing',
        'Pesticide Spraying, Crop Maintenance',
        'Harvesting, Threshing, General Farm Work',
        'Planting, Weeding, Fertilizer Application',
        'Irrigation Management, Equipment Maintenance',
        'Seed Sowing, Plant Care',
        'Sprinkler Installation, Drip Irrigation',
        'All Farm Activities, Tractor Driving',
        'General Labor, Harvesting, Loading'
    ]
    
    for i, laborer in enumerate(laborers):
        profile = LaborProfile(
            user_id=laborer.id,
            skills=skills_list[i],
            experience_years=random.randint(2, 15),
            daily_wage=random.randint(300, 800),
            availability=True,
            rating=round(random.uniform(3.5, 5.0), 1)
        )
        db.session.add(profile)
    
    db.session.commit()
    print(f"✓ Created {len(laborers)} labor profiles")

def create_crop_listings():
    """Create 10 crop listings from farmers"""
    print("\n5. Creating crop listings...")
    
    farmer_profiles = FarmerProfile.query.all()
    
    crops_data = [
        {'crop_name': 'Wheat', 'category': 'grains', 'quantity': 500, 'unit': 'kg', 'price_per_unit': 25,
         'harvest_date': date.today() + timedelta(days=15), 'location': 'Punjab',
         'description': 'Premium quality wheat, pesticide-free'},
        {'crop_name': 'Rice', 'category': 'grains', 'quantity': 1000, 'unit': 'kg', 'price_per_unit': 30,
         'harvest_date': date.today() + timedelta(days=20), 'location': 'Punjab',
         'description': 'Basmati rice, aromatic and long grain'},
        {'crop_name': 'Tomatoes', 'category': 'vegetables', 'quantity': 300, 'unit': 'kg', 'price_per_unit': 20,
         'harvest_date': date.today() + timedelta(days=5), 'location': 'Maharashtra',
         'description': 'Fresh red tomatoes, Grade A quality'},
        {'crop_name': 'Potatoes', 'category': 'vegetables', 'quantity': 800, 'unit': 'kg', 'price_per_unit': 15,
         'harvest_date': date.today() + timedelta(days=10), 'location': 'UP',
         'description': 'Organic potatoes, medium sized'},
        {'crop_name': 'Onions', 'category': 'vegetables', 'quantity': 600, 'unit': 'kg', 'price_per_unit': 18,
         'harvest_date': date.today() + timedelta(days=7), 'location': 'Maharashtra',
         'description': 'Red onions, good storage quality'},
        {'crop_name': 'Cotton', 'category': 'cash_crops', 'quantity': 400, 'unit': 'kg', 'price_per_unit': 60,
         'harvest_date': date.today() + timedelta(days=30), 'location': 'Telangana',
         'description': 'Premium cotton, high fiber quality'},
        {'crop_name': 'Sugarcane', 'category': 'cash_crops', 'quantity': 2000, 'unit': 'kg', 'price_per_unit': 3.5,
         'harvest_date': date.today() + timedelta(days=25), 'location': 'UP',
         'description': 'Sweet sugarcane, high sucrose content'},
        {'crop_name': 'Mangoes', 'category': 'fruits', 'quantity': 250, 'unit': 'kg', 'price_per_unit': 80,
         'harvest_date': date.today() + timedelta(days=40), 'location': 'Gujarat',
         'description': 'Alphonso mangoes, export quality'},
        {'crop_name': 'Cauliflower', 'category': 'vegetables', 'quantity': 350, 'unit': 'kg', 'price_per_unit': 22,
         'harvest_date': date.today() + timedelta(days=8), 'location': 'Haryana',
         'description': 'Fresh white cauliflower, organically grown'},
        {'crop_name': 'Maize', 'category': 'grains', 'quantity': 700, 'unit': 'kg', 'price_per_unit': 18,
         'harvest_date': date.today() + timedelta(days=18), 'location': 'Karnataka',
         'description': 'Yellow maize, suitable for feed and food'}
    ]
    
    for i, crop_data in enumerate(crops_data):
        listing = CropListing(
            farmer_id=farmer_profiles[i % len(farmer_profiles)].id,
            crop_name=crop_data['crop_name'],
            category=crop_data['category'],
            quantity=crop_data['quantity'],
            unit=crop_data['unit'],
            price_per_unit=crop_data['price_per_unit'],
            description=crop_data['description'],
            harvest_date=crop_data['harvest_date'],
            is_available=True
        )
        db.session.add(listing)
    
    db.session.commit()
    print(f"✓ Created {len(crops_data)} crop listings")

def create_vendor_products():
    """Create 10 vendor products"""
    print("\n6. Creating vendor products...")
    
    vendor_profiles = VendorProfile.query.all()
    
    products_data = [
        {'product_name': 'Premium Wheat Seeds', 'category': 'Seeds', 'brand': 'GreenSeeds', 
         'quantity': 500, 'unit': 'kg', 'price_per_unit': 80, 
         'description': 'High yield wheat seeds, disease resistant'},
        {'product_name': 'Hybrid Rice Seeds', 'category': 'Seeds', 'brand': 'AgriPro', 
         'quantity': 300, 'unit': 'kg', 'price_per_unit': 150,
         'description': 'Hybrid rice seeds with 30% more yield'},
        {'product_name': 'NPK Fertilizer 19:19:19', 'category': 'Fertilizers', 'brand': 'FertilizerPro', 
         'quantity': 1000, 'unit': 'kg', 'price_per_unit': 35,
         'description': 'Balanced NPK fertilizer for all crops'},
        {'product_name': 'Organic Compost', 'category': 'Fertilizers', 'brand': 'BioFert', 
         'quantity': 2000, 'unit': 'kg', 'price_per_unit': 15,
         'description': '100% organic compost, enriched with micronutrients'},
        {'product_name': 'Pesticide Spray Pro', 'category': 'Pesticides', 'brand': 'PesticidePlus', 
         'quantity': 200, 'unit': 'liter', 'price_per_unit': 250,
         'description': 'Broad spectrum pesticide for vegetables'},
        {'product_name': 'Bio Fungicide', 'category': 'Pesticides', 'brand': 'BioFert', 
         'quantity': 150, 'unit': 'liter', 'price_per_unit': 300,
         'description': 'Organic fungicide, safe for all crops'},
        {'product_name': 'Drip Irrigation Kit', 'category': 'Irrigation', 'brand': 'IrriSystems', 
         'quantity': 50, 'unit': 'unit', 'price_per_unit': 5000,
         'description': 'Complete drip irrigation system for 1 acre'},
        {'product_name': 'Sprinkler Set', 'category': 'Irrigation', 'brand': 'IrriSystems', 
         'quantity': 80, 'unit': 'unit', 'price_per_unit': 3000,
         'description': 'Rotating sprinkler with adjustable range'},
        {'product_name': 'Power Tiller', 'category': 'Equipment', 'brand': 'FarmEquip', 
         'quantity': 15, 'unit': 'unit', 'price_per_unit': 45000,
         'description': '7HP power tiller with rotavator attachment'},
        {'product_name': 'Hand Tools Kit', 'category': 'Tools', 'brand': 'AgriTools', 
         'quantity': 200, 'unit': 'set', 'price_per_unit': 1500,
         'description': 'Complete set of farm hand tools'}
    ]
    
    for i, product_data in enumerate(products_data):
        product = VendorProduct(
            vendor_id=vendor_profiles[i % len(vendor_profiles)].id,
            product_name=product_data['product_name'],
            category=product_data['category'],
            brand=product_data['brand'],
            quantity_available=product_data['quantity'],
            unit=product_data['unit'],
            price_per_unit=product_data['price_per_unit'],
            description=product_data['description'],
            is_available=True
        )
        db.session.add(product)
    
    db.session.commit()
    print(f"✓ Created {len(products_data)} vendor products")

def create_orders():
    """Create 10 sample orders from buyers"""
    print("\n7. Creating orders...")
    
    buyers = User.query.filter_by(role=UserRole.BUYER).all()
    crop_listings = CropListing.query.all()
    vendor_products = VendorProduct.query.all()
    
    orders_data = []
    
    # 5 crop orders
    for i in range(5):
        crop = crop_listings[i]
        buyer = buyers[i % len(buyers)]
        quantity = random.randint(50, 200)
        
        order = Order(
            buyer_id=buyer.id,
            order_type='crop',
            crop_listing_id=crop.id,
            quantity=quantity,
            unit_price=crop.price_per_unit,
            total_price=quantity * crop.price_per_unit,
            status=random.choice([OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.COMPLETED]),
            delivery_address=buyer.address,
            delivery_date=date.today() + timedelta(days=random.randint(5, 30)),
            notes=f'Order for {crop.crop_name}'
        )
        db.session.add(order)
        orders_data.append(order)
    
    # 5 vendor product orders
    for i in range(5):
        product = vendor_products[i]
        buyer = buyers[(i + 3) % len(buyers)]
        quantity = random.randint(10, 50)
        
        order = Order(
            buyer_id=buyer.id,
            order_type='vendor_product',
            vendor_product_id=product.id,
            quantity=quantity,
            unit_price=product.price_per_unit,
            total_price=quantity * product.price_per_unit,
            status=random.choice([OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.COMPLETED]),
            delivery_address=buyer.address,
            delivery_date=date.today() + timedelta(days=random.randint(3, 20)),
            notes=f'Order for {product.product_name}'
        )
        db.session.add(order)
        orders_data.append(order)
    
    db.session.commit()
    print(f"✓ Created {len(orders_data)} orders")

def create_cost_records():
    """Create 10 cost records for farmers"""
    print("\n8. Creating cost records...")
    
    farmer_profiles = FarmerProfile.query.all()
    
    crops = ['Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Maize', 'Tomatoes', 'Potatoes', 'Onions', 'Soybean', 'Mustard']
    seasons = ['Kharif', 'Rabi', 'Zaid']
    
    for i in range(10):
        farmer = farmer_profiles[i % len(farmer_profiles)]
        crop = crops[i]
        season = random.choice(seasons)
        
        seed_cost = random.randint(5000, 15000)
        fertilizer_cost = random.randint(8000, 20000)
        pesticide_cost = random.randint(3000, 10000)
        labor_cost = random.randint(10000, 30000)
        equipment_cost = random.randint(5000, 15000)
        irrigation_cost = random.randint(4000, 12000)
        other_cost = random.randint(2000, 8000)
        total_cost = seed_cost + fertilizer_cost + pesticide_cost + labor_cost + equipment_cost + irrigation_cost + other_cost
        revenue = total_cost * random.uniform(1.2, 2.0)
        
        record = CostRecord(
            farmer_id=farmer.id,
            crop_name=crop,
            season=season,
            year=2024,
            seed_cost=seed_cost,
            fertilizer_cost=fertilizer_cost,
            pesticide_cost=pesticide_cost,
            labor_cost=labor_cost,
            equipment_cost=equipment_cost,
            irrigation_cost=irrigation_cost,
            other_cost=other_cost,
            total_cost=total_cost,
            revenue=revenue,
            profit_loss=revenue - total_cost,
            notes=f'{season} season {crop} cultivation records'
        )
        db.session.add(record)
    
    db.session.commit()
    print(f"✓ Created 10 cost records")

def create_labor_postings():
    """Create 10 labor job postings"""
    print("\n9. Creating labor postings...")
    
    farmer_profiles = FarmerProfile.query.all()
    labor_profiles = LaborProfile.query.all()
    
    jobs_data = [
        {'job_title': 'Wheat Harvesting Workers', 'work_type': 'harvesting', 'laborers_needed': 5,
         'description': 'Need experienced workers for wheat harvesting', 'daily_wage': 500},
        {'job_title': 'Rice Planting Help', 'work_type': 'planting', 'laborers_needed': 8,
         'description': 'Rice planting season, need skilled workers', 'daily_wage': 450},
        {'job_title': 'Irrigation System Installer', 'work_type': 'irrigation', 'laborers_needed': 2,
         'description': 'Install drip irrigation system', 'daily_wage': 700},
        {'job_title': 'Pesticide Spraying Team', 'work_type': 'spraying', 'laborers_needed': 3,
         'description': 'Pesticide spraying for cotton fields', 'daily_wage': 600},
        {'job_title': 'General Farm Maintenance', 'work_type': 'maintenance', 'laborers_needed': 4,
         'description': 'Daily farm maintenance and upkeep', 'daily_wage': 400},
        {'job_title': 'Vegetable Picking Workers', 'work_type': 'harvesting', 'laborers_needed': 10,
         'description': 'Tomato and vegetable picking', 'daily_wage': 450},
        {'job_title': 'Weeding and Cultivation', 'work_type': 'weeding', 'laborers_needed': 6,
         'description': 'Manual weeding of crop fields', 'daily_wage': 400},
        {'job_title': 'Tractor Operator', 'work_type': 'machinery', 'laborers_needed': 1,
         'description': 'Experienced tractor driver needed', 'daily_wage': 800},
        {'job_title': 'Fertilizer Application Team', 'work_type': 'fertilizer', 'laborers_needed': 4,
         'description': 'Apply organic fertilizer across farm', 'daily_wage': 500},
        {'job_title': 'Cotton Picking Workers', 'work_type': 'harvesting', 'laborers_needed': 12,
         'description': 'Cotton harvesting season workers', 'daily_wage': 550}
    ]
    
    for i, job_data in enumerate(jobs_data):
        farmer = farmer_profiles[i % len(farmer_profiles)]
        start_date = date.today() + timedelta(days=random.randint(1, 15))
        end_date = start_date + timedelta(days=random.randint(10, 60))
        
        # Some jobs are open, some are filled
        if i < 5:
            labor_id = labor_profiles[i % len(labor_profiles)].id
            status = 'active'
        else:
            labor_id = None
            status = 'open'
        
        posting = LaborHiring(
            farmer_id=farmer.id,
            labor_id=labor_id,
            job_title=job_data['job_title'],
            description=job_data['description'],
            work_type=job_data['work_type'],
            start_date=start_date,
            end_date=end_date,
            total_days=(end_date - start_date).days,
            daily_wage=job_data['daily_wage'],
            total_wage=job_data['daily_wage'] * (end_date - start_date).days if labor_id else 0,
            location=farmer.farm_location,
            laborers_needed=job_data['laborers_needed'],
            status=status
        )
        db.session.add(posting)
    
    db.session.commit()
    print(f"✓ Created 10 labor postings")

def create_equipment_and_rentals():
    """Create 7 equipment entries and 5 rental records"""
    print("\n10. Creating equipment and rentals...")
    
    farmer_profiles = FarmerProfile.query.all()
    
    equipment_data = [
        {'name': 'Heavy Duty Tractor', 'type': 'tractor', 'rental_price': 2000, 'condition': 'excellent'},
        {'name': 'Combine Harvester', 'type': 'harvester', 'rental_price': 5000, 'condition': 'good'},
        {'name': 'Rotary Tiller', 'type': 'tiller', 'rental_price': 1500, 'condition': 'excellent'},
        {'name': 'Pesticide Sprayer', 'type': 'sprayer', 'rental_price': 500, 'condition': 'good'},
        {'name': 'Water Pump', 'type': 'pump', 'rental_price': 800, 'condition': 'fair'},
        {'name': 'Seed Drill', 'type': 'planter', 'rental_price': 1200, 'condition': 'excellent'},
        {'name': 'Thresher Machine', 'type': 'thresher', 'rental_price': 1800, 'condition': 'good'}
    ]
    
    equipment_list = []
    for i, equip_data in enumerate(equipment_data):
        equipment = Equipment(
            owner_id=farmer_profiles[i % len(farmer_profiles)].id,
            equipment_name=equip_data['name'],
            equipment_type=equip_data['type'],
            description=f'{equip_data["name"]} available for rent',
            rental_price_per_day=equip_data['rental_price'],
            is_available_for_rent=True,
            is_available_for_share=True,
            condition=equip_data['condition']
        )
        db.session.add(equipment)
        equipment_list.append(equipment)
    
    db.session.commit()
    
    # Create 5 rental records
    for i in range(5):
        equipment = equipment_list[i]
        renter = farmer_profiles[(i + 3) % len(farmer_profiles)]
        start_date = date.today() - timedelta(days=random.randint(5, 30))
        rental_days = random.randint(3, 15)
        end_date = start_date + timedelta(days=rental_days)
        
        rental = EquipmentRental(
            equipment_id=equipment.id,
            renter_id=renter.id,
            start_date=start_date,
            end_date=end_date,
            total_days=rental_days,
            rental_rate=equipment.rental_price_per_day,
            total_cost=equipment.rental_price_per_day * rental_days,
            status=random.choice(['completed', 'active'])
        )
        db.session.add(rental)
    
    db.session.commit()
    print(f"✓ Created {len(equipment_list)} equipment and 5 rental records")

def create_recommendation_history():
    """Create 8 recommendation history records"""
    print("\n11. Creating recommendation history...")
    
    farmer_profiles = FarmerProfile.query.all()
    
    recommendations = [
        {'type': 'crop', 'input': {'N': 90, 'P': 42, 'K': 43, 'temperature': 20.8, 'humidity': 82, 'ph': 6.5, 'rainfall': 202},
         'result': 'Rice', 'confidence': 0.95},
        {'type': 'crop', 'input': {'N': 85, 'P': 58, 'K': 41, 'temperature': 21.7, 'humidity': 80, 'ph': 7.0, 'rainfall': 226},
         'result': 'Maize', 'confidence': 0.89},
        {'type': 'fertilizer', 'input': {'soil_type': 'Loamy', 'crop': 'Wheat', 'N': 37, 'P': 0, 'K': 0},
         'result': 'Urea', 'confidence': 0.92},
        {'type': 'crop', 'input': {'N': 20, 'P': 25, 'K': 30, 'temperature': 25.0, 'humidity': 65, 'ph': 6.8, 'rainfall': 150},
         'result': 'Cotton', 'confidence': 0.87},
        {'type': 'fertilizer', 'input': {'soil_type': 'Sandy', 'crop': 'Rice', 'N': 10, 'P': 55, 'K': 20},
         'result': 'DAP', 'confidence': 0.91},
        {'type': 'crop', 'input': {'N': 40, 'P': 50, 'K': 60, 'temperature': 22.5, 'humidity': 70, 'ph': 6.2, 'rainfall': 180},
         'result': 'Sugarcane', 'confidence': 0.93},
        {'type': 'fertilizer', 'input': {'soil_type': 'Black', 'crop': 'Cotton', 'N': 25, 'P': 30, 'K': 35},
         'result': 'NPK 19:19:19', 'confidence': 0.88},
        {'type': 'crop', 'input': {'N': 60, 'P': 55, 'K': 44, 'temperature': 23.0, 'humidity': 75, 'ph': 6.9, 'rainfall': 195},
         'result': 'Chickpea', 'confidence': 0.86}
    ]
    
    for i, rec in enumerate(recommendations):
        farmer = farmer_profiles[i % len(farmer_profiles)]
        
        history = RecommendationHistory(
            farmer_id=farmer.id,
            recommendation_type=rec['type'],
            input_parameters=json.dumps(rec['input']),
            recommendation_result=rec['result'],
            confidence_score=rec['confidence']
        )
        db.session.add(history)
    
    db.session.commit()
    print(f"✓ Created {len(recommendations)} recommendation history records")

def print_summary():
    """Print summary of all created data"""
    print("\n" + "="*70)
    print("DATA POPULATION SUMMARY")
    print("="*70)
    
    with app.app_context():
        print(f"\n📊 Total Users: {User.query.count()}")
        print(f"   - Farmers: {User.query.filter_by(role=UserRole.FARMER).count()}")
        print(f"   - Buyers: {User.query.filter_by(role=UserRole.BUYER).count()}")
        print(f"   - Vendors: {User.query.filter_by(role=UserRole.VENDOR).count()}")
        print(f"   - Labor: {User.query.filter_by(role=UserRole.LABOR).count()}")
        print(f"   - Admin: {User.query.filter_by(role=UserRole.ADMIN).count()}")
        
        print(f"\n🌾 Farmer Portal Data:")
        print(f"   - Farmer Profiles: {FarmerProfile.query.count()}")
        print(f"   - Crop Listings: {CropListing.query.count()}")
        print(f"   - Cost Records: {CostRecord.query.count()}")
        print(f"   - Labor Postings: {LaborHiring.query.count()}")
        print(f"   - Equipment: {Equipment.query.count()}")
        print(f"   - Equipment Rentals: {EquipmentRental.query.count()}")
        print(f"   - Recommendations: {RecommendationHistory.query.count()}")
        
        print(f"\n🛒 Buyer Portal Data:")
        print(f"   - Orders: {Order.query.count()}")
        print(f"   - Marketplace Items: {CropListing.query.count() + VendorProduct.query.count()}")
        
        print(f"\n🏪 Vendor Portal Data:")
        print(f"   - Vendor Profiles: {VendorProfile.query.count()}")
        print(f"   - Products: {VendorProduct.query.count()}")
        print(f"   - Product Orders: {Order.query.filter_by(order_type='vendor_product').count()}")
        
        print(f"\n👷 Labor Portal Data:")
        print(f"   - Labor Profiles: {LaborProfile.query.count()}")
        print(f"   - Job Postings: {LaborHiring.query.count()}")
        print(f"   - Active Jobs: {LaborHiring.query.filter(LaborHiring.labor_id.isnot(None)).count()}")
        
        print("\n" + "="*70)
        print("✅ All portal data populated successfully!")
        print("="*70)
        
        print("\n📝 Sample Login Credentials:")
        print("   Farmer:  farmer1@farm.com / pass123")
        print("   Buyer:   buyer1@market.com / pass123")
        print("   Vendor:  vendor1@supply.com / pass123")
        print("   Labor:   labor1@work.com / pass123")
        print("   Admin:   admin@smartfarm.com / admin123")

def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("SMART FARMING PLATFORM - COMPREHENSIVE DATA POPULATION")
    print("="*70)
    
    with app.app_context():
        # Optional: Uncomment to clear existing data
        # clear_all_data()
        
        # Create all data
        users = create_users()
        create_farmer_profiles(users)
        create_vendor_profiles(users)
        create_labor_profiles(users)
        create_crop_listings()
        create_vendor_products()
        create_orders()
        create_cost_records()
        create_labor_postings()
        create_equipment_and_rentals()
        create_recommendation_history()
        
        # Print summary
        print_summary()

if __name__ == '__main__':
    main()

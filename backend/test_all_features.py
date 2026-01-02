"""
Comprehensive testing script for Smart Farming Platform
Tests all registration, login, and dashboard features
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5001/api"
test_results = []

def log_test(test_name, status, message=""):
    """Log test results"""
    symbol = "✓" if status else "✗"
    test_results.append({
        "test": test_name,
        "status": status,
        "message": message
    })
    print(f"{symbol} {test_name}: {message}")

def test_registration():
    """Test registration for all user types"""
    print("\n" + "="*60)
    print("TESTING REGISTRATION")
    print("="*60)
    
    # Test Farmer Registration
    farmer_data = {
        "email": f"farmer_test_{datetime.now().timestamp()}@test.com",
        "password": "Test123!",
        "full_name": "Test Farmer",
        "phone": "1234567890",
        "address": "Test Farm Address, Delhi",
        "role": "farmer",
        "farm_name": "Green Valley Farm",
        "farm_size": 10.5,
        "farm_location": "Delhi"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=farmer_data)
        if response.status_code == 201:
            log_test("Farmer Registration", True, "Farmer registered successfully")
            return farmer_data["email"], farmer_data["password"], "farmer"
        else:
            log_test("Farmer Registration", False, f"Status: {response.status_code}, Error: {response.json()}")
    except Exception as e:
        log_test("Farmer Registration", False, str(e))
    
    # Test Buyer Registration
    buyer_data = {
        "email": f"buyer_test_{datetime.now().timestamp()}@test.com",
        "password": "Test123!",
        "full_name": "Test Buyer",
        "phone": "9876543210",
        "address": "Test Buyer Address",
        "role": "buyer",
        "company_name": "FoodCorp Ltd",
        "business_type": "Retail"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=buyer_data)
        log_test("Buyer Registration", response.status_code == 201, 
                f"Status: {response.status_code}")
    except Exception as e:
        log_test("Buyer Registration", False, str(e))
    
    # Test Vendor Registration
    vendor_data = {
        "email": f"vendor_test_{datetime.now().timestamp()}@test.com",
        "password": "Test123!",
        "full_name": "Test Vendor",
        "phone": "5555555555",
        "address": "Test Vendor Address",
        "role": "vendor",
        "business_name": "AgriSupply Co",
        "business_type": "Seeds"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=vendor_data)
        log_test("Vendor Registration", response.status_code == 201,
                f"Status: {response.status_code}")
    except Exception as e:
        log_test("Vendor Registration", False, str(e))
    
    # Test Labor Registration
    labor_data = {
        "email": f"labor_test_{datetime.now().timestamp()}@test.com",
        "password": "Test123!",
        "full_name": "Test Labor",
        "phone": "7777777777",
        "address": "Test Labor Address",
        "role": "labor",
        "skills": "Harvesting, Planting",
        "experience_years": 5,
        "daily_wage": 500
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=labor_data)
        log_test("Labor Registration", response.status_code == 201,
                f"Status: {response.status_code}")
    except Exception as e:
        log_test("Labor Registration", False, str(e))
    
    return farmer_data["email"], farmer_data["password"], "farmer"

def test_login(email, password):
    """Test login functionality"""
    print("\n" + "="*60)
    print("TESTING LOGIN")
    print("="*60)
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            log_test("Login", True, f"Login successful, Token received")
            return token
        else:
            log_test("Login", False, f"Status: {response.status_code}")
            return None
    except Exception as e:
        log_test("Login", False, str(e))
        return None

def test_farmer_features(token):
    """Test all farmer portal features"""
    print("\n" + "="*60)
    print("TESTING FARMER PORTAL FEATURES")
    print("="*60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test Crop Listing Creation
    crop_data = {
        "crop_name": "Wheat",
        "quantity": 100,
        "unit": "quintal",
        "price_per_unit": 2000,
        "quality_grade": "A",
        "harvest_date": "2026-01-15",
        "available_from": "2026-01-20",
        "description": "Fresh organic wheat"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/farmer/crop-listings", 
                               json=crop_data, headers=headers)
        listing_id = None
        if response.status_code == 201:
            listing_id = response.json().get("listing", {}).get("id")
            log_test("Crop Listing Creation", True, f"Listing ID: {listing_id}")
        else:
            log_test("Crop Listing Creation", False, 
                    f"Status: {response.status_code}, Error: {response.json()}")
    except Exception as e:
        log_test("Crop Listing Creation", False, str(e))
    
    # Test Get Crop Listings
    try:
        response = requests.get(f"{BASE_URL}/farmer/crop-listings", headers=headers)
        log_test("Get Crop Listings", response.status_code == 200,
                f"Retrieved {len(response.json().get('listings', []))} listings")
    except Exception as e:
        log_test("Get Crop Listings", False, str(e))
    
    # Test Cost Tracking
    cost_data = {
        "category": "Seeds",
        "amount": 5000,
        "date": "2026-01-01",
        "description": "Wheat seeds purchase",
        "payment_method": "Cash"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/farmer/costs",
                               json=cost_data, headers=headers)
        log_test("Cost Entry Creation", response.status_code == 201,
                f"Status: {response.status_code}")
    except Exception as e:
        log_test("Cost Entry Creation", False, str(e))
    
    # Test Get Costs
    try:
        response = requests.get(f"{BASE_URL}/farmer/costs", headers=headers)
        log_test("Get Cost Records", response.status_code == 200,
                f"Retrieved {len(response.json().get('costs', []))} records")
    except Exception as e:
        log_test("Get Cost Records", False, str(e))
    
    # Test Labor Posting
    labor_data = {
        "job_title": "Harvest Workers",
        "description": "Need workers for wheat harvesting",
        "work_type": "Harvesting",
        "start_date": "2026-01-15",
        "end_date": "2026-01-20",
        "daily_wage": 700,
        "location": "Delhi, India",
        "laborers_needed": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/farmer/labor-postings",
                               json=labor_data, headers=headers)
        if response.status_code == 201:
            log_test("Labor Posting Creation", True, "Labor posting created")
        else:
            log_test("Labor Posting Creation", False,
                    f"Status: {response.status_code}, Error: {response.json()}")
    except Exception as e:
        log_test("Labor Posting Creation", False, str(e))
    
    # Test Get Labor Postings
    try:
        response = requests.get(f"{BASE_URL}/farmer/labor-postings", headers=headers)
        log_test("Get Labor Postings", response.status_code == 200,
                f"Retrieved postings")
    except Exception as e:
        log_test("Get Labor Postings", False, str(e))
    
    # Test Weather API
    try:
        response = requests.get(f"{BASE_URL}/farmer/weather?location=Delhi", headers=headers)
        log_test("Weather Widget", response.status_code == 200,
                "Weather data retrieved")
    except Exception as e:
        log_test("Weather Widget", False, str(e))

def test_public_endpoints():
    """Test public endpoints"""
    print("\n" + "="*60)
    print("TESTING PUBLIC ENDPOINTS")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/public/products")
        log_test("Public Products List", response.status_code == 200,
                f"Retrieved {len(response.json().get('products', []))} products")
    except Exception as e:
        log_test("Public Products List", False, str(e))
    
    try:
        response = requests.get(f"{BASE_URL}/public/labor-listings")
        log_test("Public Labor Listings", response.status_code == 200,
                f"Retrieved {len(response.json().get('listings', []))} listings")
    except Exception as e:
        log_test("Public Labor Listings", False, str(e))

def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = len(test_results)
    passed = sum(1 for t in test_results if t["status"])
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Success Rate: {(passed/total*100):.1f}%\n")
    
    if failed > 0:
        print("Failed Tests:")
        for test in test_results:
            if not test["status"]:
                print(f"  ✗ {test['test']}: {test['message']}")

if __name__ == "__main__":
    print("\n🌾 Smart Farming Platform - Comprehensive Testing")
    print("="*60)
    
    # Test Registration
    email, password, role = test_registration()
    
    # Test Login
    token = test_login(email, password)
    
    if token:
        # Test Farmer Features
        test_farmer_features(token)
    
    # Test Public Endpoints
    test_public_endpoints()
    
    # Print Summary
    print_summary()

# Smart Farming Platform - API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

---

## Authentication Endpoints

### Register User
Register a new user account.

**Endpoint**: `POST /api/auth/register`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "phone": "1234567890",
  "role": "farmer",
  // Role-specific fields:
  "farm_name": "Green Acres Farm",      // For farmers
  "business_name": "AgriSupply Inc",    // For vendors
  "skills": "Planting, Harvesting",     // For labor
  "daily_wage": 500                     // For labor
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Registration successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "farmer",
    "is_verified": false,
    "is_active": true
  }
}
```

### Login
Authenticate and receive JWT token.

**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "farmer"
  }
}
```

### Get Profile
Get current user profile.

**Endpoint**: `GET /api/auth/profile`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "farmer",
    "farmer_profile": {
      "farm_name": "Green Acres Farm",
      "farm_size": 10.5,
      "farm_location": "Rural Area, State"
    }
  }
}
```

---

## Public Endpoints

### Get Public Products
Get all publicly available products and crops.

**Endpoint**: `GET /api/public/products`

**Query Parameters**:
- `category` (optional): Filter by category
- `search` (optional): Search query
- `limit` (optional): Number of results (default: 20)

**Response** (200 OK):
```json
{
  "success": true,
  "crops": [
    {
      "id": 1,
      "crop_name": "Rice",
      "category": "grains",
      "quantity": 1000,
      "unit": "kg",
      "price_per_unit": 25.0,
      "is_available": true
    }
  ],
  "vendor_products": [
    {
      "id": 1,
      "product_name": "Organic Fertilizer",
      "category": "fertilizers",
      "price_per_unit": 500.0
    }
  ],
  "total_count": 15
}
```

### Get Labor Listings
Get available labor workers.

**Endpoint**: `GET /api/public/labor-listings`

**Response** (200 OK):
```json
{
  "success": true,
  "labor": [
    {
      "id": 1,
      "full_name": "Worker Name",
      "skills": "Planting, Harvesting",
      "experience_years": 5,
      "daily_wage": 500.0,
      "rating": 4.5
    }
  ]
}
```

---

## Farmer Portal Endpoints

### Crop Recommendation
Get AI-powered crop recommendation.

**Endpoint**: `POST /api/farmer/crop-recommendation`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.87,
  "humidity": 82.0,
  "pH": 6.5,
  "rainfall": 202.9
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "recommendation": {
    "crop": "rice",
    "confidence": 0.95,
    "top_3_predictions": [
      {"crop": "rice", "probability": 0.95},
      {"crop": "wheat", "probability": 0.03},
      {"crop": "maize", "probability": 0.02}
    ]
  }
}
```

### Fertilizer Recommendation
Get fertilizer recommendation based on soil nutrients.

**Endpoint**: `POST /api/farmer/fertilizer-recommendation`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "soil_type": "loamy",
  "crop_type": "wheat",
  "N": 30,
  "P": 20,
  "K": 25
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "recommendation": {
    "fertilizer": "Urea",
    "amount": "174 kg/ha",
    "deficiencies": {
      "nitrogen": "high",
      "phosphorus": "medium",
      "potassium": "low"
    }
  }
}
```

### Get Recommendation History
View past crop and fertilizer recommendations.

**Endpoint**: `GET /api/farmer/recommendation-history`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "success": true,
  "history": [
    {
      "id": 1,
      "type": "crop",
      "input": {"N": 90, "P": 42, "K": 43, ...},
      "result": {"crop": "rice", "confidence": 0.95},
      "date": "2026-01-01T10:00:00"
    }
  ]
}
```

### Manage Crop Listings
Get or create crop listings for the marketplace.

**Endpoint**: `GET /api/farmer/crop-listings`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "success": true,
  "listings": [
    {
      "id": 1,
      "crop_name": "Rice",
      "category": "grains",
      "quantity": 1000,
      "unit": "kg",
      "price_per_unit": 25.0,
      "is_available": true,
      "created_at": "2026-01-01T10:00:00"
    }
  ]
}
```

**Endpoint**: `POST /api/farmer/crop-listings`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "crop_name": "Rice",
  "category": "grains",
  "quantity": 1000,
  "unit": "kg",
  "price_per_unit": 25.0,
  "description": "High quality basmati rice",
  "harvest_date": "2026-02-01"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Crop listing created",
  "listing": {...}
}
```

### Cost Tracking
Track farming costs and analyze profit/loss.

**Endpoint**: `POST /api/farmer/costs`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "crop_name": "Rice",
  "season": "Kharif",
  "year": 2026,
  "seed_cost": 5000,
  "fertilizer_cost": 8000,
  "pesticide_cost": 3000,
  "labor_cost": 15000,
  "equipment_cost": 10000,
  "irrigation_cost": 5000,
  "other_cost": 2000,
  "revenue": 60000,
  "notes": "Good harvest this season"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Cost record created",
  "record_id": 1
}
```

### Weather Information
Get real-time weather for farm location.

**Endpoint**: `GET /api/farmer/weather?location=CityName`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "success": true,
  "weather": {
    "temperature": 28.5,
    "humidity": 65,
    "description": "partly cloudy",
    "wind_speed": 5.2,
    "pressure": 1013
  }
}
```

---

## Buyer Portal Endpoints

### Browse Marketplace
Browse available crops and products.

**Endpoint**: `GET /api/buyer/marketplace`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `category` (optional)
- `search` (optional)

**Response** (200 OK):
```json
{
  "success": true,
  "crops": [...],
  "products": [...]
}
```

### Manage Orders
Place or view orders.

**Endpoint**: `POST /api/buyer/orders`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "order_type": "crop",
  "crop_listing_id": 1,
  "quantity": 500,
  "unit_price": 25.0,
  "is_contract_farming": false,
  "delivery_date": "2026-02-15",
  "delivery_address": "123 Main St, City",
  "notes": "Please deliver in morning"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Order placed successfully",
  "order_id": 1
}
```

---

## Vendor Portal Endpoints

### Manage Products
Get or create vendor products.

**Endpoint**: `GET /api/vendor/products`

**Headers**: `Authorization: Bearer <token>`

**Endpoint**: `POST /api/vendor/products`

**Request Body**:
```json
{
  "product_name": "Organic Fertilizer",
  "category": "fertilizers",
  "brand": "GreenGrow",
  "quantity_available": 1000,
  "unit": "kg",
  "price_per_unit": 50.0,
  "description": "100% organic fertilizer",
  "specifications": "NPK 10:20:10"
}
```

### View Orders
Get orders for vendor's products.

**Endpoint**: `GET /api/vendor/orders`

**Headers**: `Authorization: Bearer <token>`

---

## Labor Portal Endpoints

### View Job Postings
Get available job postings from farmers.

**Endpoint**: `GET /api/labor/job-postings`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "success": true,
  "postings": [
    {
      "id": 1,
      "farmer_name": "John Farmer",
      "farmer_location": "Rural Area",
      "job_title": "Harvesting Worker",
      "work_type": "harvesting",
      "start_date": "2026-02-01",
      "daily_wage": 500.0
    }
  ]
}
```

### Apply for Job
Apply for a job posting.

**Endpoint**: `POST /api/labor/apply/:posting_id`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Application successful"
}
```

### My Jobs
View accepted jobs.

**Endpoint**: `GET /api/labor/my-jobs`

**Headers**: `Authorization: Bearer <token>`

---

## Admin Portal Endpoints

### User Management
Get all users.

**Endpoint**: `GET /api/admin/users`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `role` (optional): Filter by user role

### Verify User
Verify a user account.

**Endpoint**: `POST /api/admin/verify-user/:user_id`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "success": true,
  "message": "User verified"
}
```

### Platform Analytics
Get platform statistics.

**Endpoint**: `GET /api/admin/analytics`

**Headers**: `Authorization: Bearer <token>`

**Response** (200 OK):
```json
{
  "success": true,
  "analytics": {
    "total_users": 150,
    "farmers": 50,
    "buyers": 60,
    "vendors": 25,
    "labor": 10,
    "total_orders": 234,
    "total_crops": 89,
    "total_products": 145
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication token is missing"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied. Insufficient permissions.",
  "required_roles": ["farmer"],
  "user_role": "buyer"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting
- No rate limiting currently implemented
- Consider adding for production

## Pagination
- Most list endpoints support `limit` parameter
- Future: Add `offset` and `page` parameters

## Data Validation
- All inputs are validated
- Numeric fields must be valid numbers
- Required fields are enforced
- Email format validated on registration

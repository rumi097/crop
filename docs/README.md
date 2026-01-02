# Smart Farming Platform 🌾

A comprehensive multi-purpose smart farming web application with role-based portals connecting farmers, buyers, vendors, laborers, and administrators in one unified platform.

## Overview

Smart Farming Platform is a full-stack web application designed to modernize and streamline agricultural operations. It provides specialized portals for different user types, enabling efficient marketplace transactions, farm management, labor coordination, and agricultural supply chain optimization.

## Key Features

### 🌾 Farmer Portal
- **AI-Powered Recommendations**: Get crop and fertilizer recommendations based on soil parameters, weather, and historical data
- **Recommendation History**: View and analyze all past crop and fertilizer recommendations
- **Online Marketplace**: List crops for sale with categorization and pricing
- **Cost Tracking & Profit Analysis**: Track all farming expenses (seeds, fertilizer, labor, equipment) and calculate profit/loss per crop and season
- **Labor Management**: Post job openings, hire workers, track workdays and wages
- **Equipment Sharing**: Rent or share farm equipment with nearby farmers
- **Input Procurement**: Order seeds, fertilizers, and tools from verified vendors
- **Weather Integration**: Real-time weather information for farm location

### 🛒 Buyer Portal
- **Browse Marketplace**: Access categorized bazaar of fresh crops and agricultural products
- **Normal & Bulk Orders**: Place regular purchases or bulk orders
- **Contract Farming**: Place advance orders for future harvests
- **Order Tracking**: Monitor order status and delivery
- **Payment Management**: Secure payment processing and history

### 🏪 Vendor Portal
- **Product Listing**: List agricultural inputs (seeds, fertilizers, pesticides, tools)
- **Inventory Management**: Track stock levels and product availability
- **Order Fulfillment**: Manage incoming orders from farmers
- **Sales Analytics**: View business performance and ratings

### 👷 Labor Portal
- **Job Listings**: Browse available farm work opportunities
- **Easy Application**: Apply for jobs posted by farmers
- **Work History**: Track employment records and earnings
- **Skill Showcase**: Display skills, experience, and daily wage rates

### ⚙️ Admin Portal
- **User Verification**: Approve and verify farmers, vendors, and labor accounts
- **Platform Analytics**: View comprehensive statistics and insights
- **Product Moderation**: Monitor and moderate listings and products
- **Category Management**: Manage product and crop categories
- **User Management**: Oversee all platform users and activities

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: SQLAlchemy with SQLite (upgradeable to PostgreSQL/MySQL)
- **Authentication**: JWT-based secure authentication with role-based access control
- **ML/AI**: scikit-learn for crop recommendations, TensorFlow for future enhancements
- **APIs**: RESTful API architecture

### Frontend
- **Framework**: React 18.2.0
- **Routing**: React Router DOM 6.14.0
- **HTTP Client**: Axios 1.4.0
- **Styling**: Custom CSS with modern responsive design

### Machine Learning
- **Crop Recommendation**: Random Forest Classifier trained on soil and climate data
- **Fertilizer Recommendation**: Rule-based system with nutrient deficiency analysis
- **Weather API**: OpenWeatherMap integration for real-time weather data

## Installation & Setup

### Prerequisites
- Python 3.10+ (3.13 compatible)
- Node.js 16+ and npm
- Git

### Backend Setup

1. **Clone the repository**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional):
   ```bash
   export JWT_SECRET_KEY="your-secret-key"
   export WEATHER_API_KEY="your-openweathermap-api-key"
   export DATABASE_URL="sqlite:///smart_farming.db"
   ```

5. **Run the backend server**:
   ```bash
   python app.py
   ```
   Server will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```
   Application will open on `http://localhost:3000`

## Default Admin Account

- **Email**: `admin@smartfarming.com`
- **Password**: `admin123`

⚠️ **Change this in production!**

## User Roles

1. **Farmer**: Full access to farming tools, recommendations, marketplace listing, cost tracking
2. **Buyer**: Browse marketplace, place orders, track purchases
3. **Vendor**: Manage agricultural input products, fulfill orders
4. **Labor**: Find jobs, apply for work, track employment
5. **Admin**: Platform management, user verification, analytics

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile (protected)

### Public
- `GET /api/public/products` - Get all public products
- `GET /api/public/labor-listings` - Get available labor

### Farmer (Protected)
- `POST /api/farmer/crop-recommendation` - Get crop recommendation
- `POST /api/farmer/fertilizer-recommendation` - Get fertilizer recommendation
- `GET /api/farmer/recommendation-history` - View recommendation history
- `GET/POST /api/farmer/crop-listings` - Manage crop listings
- `GET/POST /api/farmer/costs` - Cost tracking
- `GET/POST /api/farmer/labor-postings` - Labor management
- `GET/POST /api/farmer/equipment` - Equipment management
- `GET /api/farmer/weather` - Weather information

### Buyer (Protected)
- `GET /api/buyer/marketplace` - Browse marketplace
- `GET/POST /api/buyer/orders` - Manage orders

### Vendor (Protected)
- `GET/POST /api/vendor/products` - Manage products
- `GET /api/vendor/orders` - View received orders

### Labor (Protected)
- `GET /api/labor/job-postings` - View available jobs
- `POST /api/labor/apply/:id` - Apply for job
- `GET /api/labor/my-jobs` - View my jobs

### Admin (Protected)
- `GET /api/admin/users` - Get all users
- `POST /api/admin/verify-user/:id` - Verify user
- `GET /api/admin/analytics` - Platform analytics

## Database Schema

The application uses a comprehensive relational database with the following main tables:
- **users**: Base user accounts with role-based access
- **farmer_profiles**: Extended farmer information
- **vendor_profiles**: Vendor business details
- **labor_profiles**: Labor skills and availability
- **crop_listings**: Crops for sale by farmers
- **vendor_products**: Agricultural inputs from vendors
- **orders**: Purchase orders with contract farming support
- **cost_records**: Farming cost tracking and profit analysis
- **labor_hiring**: Job postings and employment records
- **equipment**: Shareable farm equipment
- **recommendation_history**: ML recommendation logs

## Features in Detail

### Cost Tracking System
Farmers can track:
- Seed costs
- Fertilizer expenses
- Pesticide costs
- Labor wages
- Equipment costs
- Irrigation expenses
- Other miscellaneous costs

The system automatically calculates:
- Total costs per crop
- Revenue from sales
- Profit/Loss analysis per crop and season

### Contract Farming
Buyers can place advance orders for future harvests, providing farmers with:
- Guaranteed market for produce
- Price certainty
- Production planning support

### Equipment Sharing
Farmers can:
- List owned equipment for rent or sharing
- Set rental prices per day
- Track equipment usage and earnings
- Find nearby equipment to rent

## Development

### Training ML Models

1. **Crop Recommendation Model**:
   ```bash
   python scripts/train_crop_model.py
   ```

2. **View Model Performance**:
   Models are saved in `backend/saved_models/`

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Production Deployment

### Backend
1. Use PostgreSQL or MySQL instead of SQLite
2. Set strong JWT_SECRET_KEY
3. Enable HTTPS
4. Set up proper CORS origins
5. Use production-grade WSGI server (Gunicorn)

### Frontend
1. Build production bundle: `npm run build`
2. Serve with Nginx or Apache
3. Configure API_URL environment variable

### Environment Variables
```bash
export FLASK_ENV=production
export DATABASE_URL="postgresql://user:pass@localhost/smartfarming"
export JWT_SECRET_KEY="strong-random-secret"
export WEATHER_API_KEY="your-api-key"
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Email: support@smartfarming.com

## Acknowledgments

- Machine Learning datasets from Kaggle
- Weather data from OpenWeatherMap
- Icons and UI inspiration from modern agricultural platforms

---

**Smart Farming Platform** - Connecting Agriculture Community 🌾

*Built with ❤️ for farmers, by developers who care about agriculture*

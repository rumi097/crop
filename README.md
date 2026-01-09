# 🌾 Smart Farming Platform

A comprehensive multi-portal agricultural management system built with React and Flask.

## 📁 Project Structure

```
Crop/
├── backend/              # Flask Backend API
│   ├── config/          # Configuration files
│   │   └── settings.py  # App configuration
│   ├── models/          # Database models
│   │   ├── database.py  # SQLAlchemy models
│   │   ├── crop_recommendation.py
│   │   └── fertilizer_recommendation.py
│   ├── portals/         # Portal-specific routes
│   │   ├── admin_routes.py
│   │   ├── buyer_routes.py
│   │   ├── farmer_routes.py
│   │   ├── labor_routes.py
│   │   └── vendor_routes.py
│   ├── routes/          # General routes
│   │   ├── auth_routes.py
│   │   └── error_handlers.py
│   ├── services/        # Business logic & ML models
│   │   └── ml_models.py
│   ├── utils/           # Utility functions
│   │   ├── auth.py
│   │   ├── evaluation.py
│   │   └── preprocessing.py
│   ├── app.py          # Main application entry point
│   └── requirements.txt
│
├── frontend/            # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/           # Login & Register
│   │   │   ├── portals/        # Portal components
│   │   │   │   ├── AdminPortal.js
│   │   │   │   ├── BuyerPortal.js
│   │   │   │   ├── FarmerPortal.js
│   │   │   │   ├── LaborPortal.js
│   │   │   │   └── VendorPortal.js
│   │   │   └── shared/         # Shared components
│   │   ├── styles/
│   │   │   ├── base/           # Base styles
│   │   │   │   ├── reset.css
│   │   │   │   └── animations.css
│   │   │   ├── components/     # Component styles
│   │   │   │   ├── header.css
│   │   │   │   ├── cards.css
│   │   │   │   ├── forms.css
│   │   │   │   ├── buttons.css
│   │   │   │   ├── badges.css
│   │   │   │   ├── tables.css
│   │   │   │   ├── alerts.css
│   │   │   │   ├── loading.css
│   │   │   │   ├── tabs.css
│   │   │   │   └── modal.css
│   │   │   ├── portals/        # Portal-specific styles
│   │   │   │   ├── admin.css
│   │   │   │   ├── buyer.css
│   │   │   │   ├── farmer.css
│   │   │   │   ├── labor.css
│   │   │   │   └── vendor.css
│   │   │   ├── utilities/      # Utility styles
│   │   │   │   ├── layout.css
│   │   │   │   ├── spacing.css
│   │   │   │   ├── misc.css
│   │   │   │   └── responsive.css
│   │   │   └── main.css       # CSS Variables & Theme
│   │   ├── App.js
│   │   ├── App.css            # Main stylesheet (imports all)
│   │   └── index.js
│   └── package.json
│
├── data/                # Training data & datasets
├── scripts/             # Training & utility scripts
├── docs/               # Documentation files
│   ├── API_DOCUMENTATION.md
│   ├── QUICKSTART.md
│   ├── PROJECT_SUMMARY.md
│   └── TESTING.md
├── setup.sh            # Setup script for Unix/Mac
├── setup.bat           # Setup script for Windows
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Crop
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Run the Application**

   Terminal 1 (Backend):
   ```bash
   cd backend
   source venv/bin/activate
   python app.py
   ```

   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm start
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001

## 👥 User Portals

### 1. **Farmer Portal** 🚜
- Crop recommendations based on soil and weather
- Fertilizer recommendations
- Marketplace for selling crops
- Cost tracking and financial management
- Labor hiring management
- Equipment sharing

### 2. **Buyer Portal** 🛒
- Browse agricultural products
- Place orders
- Contract farming
- Order tracking
- Payment management

### 3. **Vendor Portal** 📦
- List agricultural inputs (seeds, fertilizers, etc.)
- Inventory management
- Order fulfillment
- Sales analytics

### 4. **Labor Portal** 👷
- View job postings
- Apply for farming work
- Profile management
- Availability status

### 5. **Admin Portal** ⚙️
- User verification
- Platform analytics
- Content moderation
- System management

## 🔐 Default Credentials

**Admin Account:**
- Email: admin@smartfarming.com
- Password: admin123

## 🛠️ Tech Stack

**Backend:**
- Flask (Python web framework)
- SQLAlchemy (ORM)
- JWT Authentication
- Machine Learning models (scikit-learn, TensorFlow)

**Frontend:**
- React.js
- Modern CSS3 (organized modular architecture)
- Responsive design

## 📚 Documentation

For more detailed information, see the documentation in the `/docs` folder:
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Quick Start Guide](docs/QUICKSTART.md)
- [Project Summary](docs/PROJECT_SUMMARY.md)
- [Testing Guide](docs/TESTING.md)

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines first.

## 📄 License

This project is licensed under the MIT License.

## 🌟 Features

- ✅ Multi-role authentication system
- ✅ ML-powered crop recommendations
- ✅ Real-time marketplace
- ✅ Financial tracking
- ✅ Equipment sharing economy
- ✅ Labor marketplace
- ✅ Admin analytics dashboard
- ✅ Responsive mobile-first design
- ✅ Modular and maintainable codebase

---

Built with ❤️ for farmers and the agricultural community

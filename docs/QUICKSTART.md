# Quick Start Guide - Smart Farming Platform

Get up and running in 5 minutes! 🚀

## Prerequisites

Ensure you have these installed:
- ✅ Python 3.10 or higher
- ✅ Node.js 16 or higher
- ✅ npm or yarn

## Step 1: Backend Setup (2 minutes)

### 1.1 Navigate to backend directory
```bash
cd backend
```

### 1.2 Create virtual environment
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### 1.3 Install dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-SQLAlchemy (database)
- PyJWT (authentication)
- scikit-learn (ML)
- And other dependencies

### 1.4 Start the backend server
```bash
python app.py
```

✅ **Backend running at**: `http://localhost:5000`

You should see:
```
✓ Database tables created successfully
✓ Admin user created: admin@smartfarming.com
✓ Crop model loaded (or warning if not trained yet)
✓ Fertilizer model initialized
🌾 Smart Farming Platform API
```

**Keep this terminal open!**

---

## Step 2: Frontend Setup (2 minutes)

### 2.1 Open a NEW terminal and navigate to frontend
```bash
cd frontend
```

### 2.2 Install dependencies
```bash
npm install
```

This will install:
- React
- React Router
- Axios
- And other dependencies

### 2.3 Start the development server
```bash
npm start
```

✅ **Frontend running at**: `http://localhost:3000`

Your browser should automatically open. If not, manually visit `http://localhost:3000`

---

## Step 3: Test the Application (1 minute)

### 3.1 View the Landing Page
- You'll see the public homepage with products, vendor items, and labor listings
- Try clicking through different tabs

### 3.2 Login as Admin
1. Click **Login** button
2. Enter credentials:
   - **Email**: `admin@smartfarming.com`
   - **Password**: `admin123`
3. Click **Login**

✅ You're now in the **Admin Portal**!

### 3.3 Register a New User
1. Click **Logout**
2. Click **Register**
3. Fill in the form:
   - **Role**: Select "Farmer" (or any other role)
   - **Email**: Your email
   - **Password**: Your password
   - **Full Name**: Your name
   - **Phone**: Optional
   - **Role-specific fields** (e.g., Farm Name for Farmers)
4. Click **Register**

✅ You're now in your **Role-specific Portal**!

---

## Quick Feature Tour

### As a Farmer 🌾
1. Click **Recommendations** tab
2. Fill in soil parameters (N, P, K, temperature, humidity, pH, rainfall)
3. Click **Get Recommendation**
4. View your recommended crop!
5. Try the **History** tab to see past recommendations

### As a Buyer 🛒
1. Click **Marketplace** tab
2. Browse available crops and products
3. Click **Order Now** on any item
4. View your orders in **My Orders** tab

### As a Vendor 🏪
1. Click **My Products** tab
2. Add a new product (seeds, fertilizer, etc.)
3. View orders in **Orders Received** tab

### As Labor 👷
1. Click **Available Jobs** tab
2. Browse job postings from farmers
3. Click **Apply Now** to apply for a job
4. View accepted jobs in **My Jobs** tab

### As Admin ⚙️
1. View **Analytics** dashboard
2. Check **User Management** tab
3. Verify users by clicking **Verify** button

---

## Environment Variables (Optional)

Create a `.env` file in the backend directory for custom configuration:

```bash
# Backend (.env)
JWT_SECRET_KEY=your-secret-key-here
WEATHER_API_KEY=your-openweathermap-api-key
DATABASE_URL=sqlite:///smart_farming.db
```

Create `.env` file in frontend directory:
```bash
# Frontend (.env)
REACT_APP_API_URL=http://localhost:5000
```

---

## Common Issues & Solutions

### Issue 1: Port Already in Use
**Error**: `Address already in use`

**Solution**:
```bash
# Kill process on port 5000 (backend)
# On macOS/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Issue 2: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: Database Errors
**Error**: Database-related errors

**Solution**:
```bash
# Delete existing database and restart
rm backend/smart_farming.db  # macOS/Linux
del backend\smart_farming.db # Windows

# Restart backend server
python app.py
```

### Issue 4: CORS Errors
**Error**: `Access to fetch at 'http://localhost:5000' from origin 'http://localhost:3000' has been blocked`

**Solution**: Already configured! If issue persists, check:
1. Backend is running on port 5000
2. Frontend is running on port 3000
3. CORS is enabled in `app.py` (already done)

---

## Training ML Models (Optional)

### Crop Recommendation Model
```bash
cd scripts
python train_crop_model.py
```

The trained model will be saved to `backend/saved_models/crop_model.pkl`

**Note**: A pre-trained model may already be included. Check `backend/saved_models/` directory.

---

## Default Test Accounts

### Admin Account
- **Email**: `admin@smartfarming.com`
- **Password**: `admin123`
- **Features**: Full platform access, user management, analytics

### Create Your Own Accounts
Register through the UI with different roles:
- **Farmer**: Get crop recommendations, list crops, track costs
- **Buyer**: Browse marketplace, place orders
- **Vendor**: List agricultural products, manage inventory
- **Labor**: Find jobs, apply for work

---

## API Testing with cURL

### Test Health Endpoint
```bash
curl http://localhost:5000/
```

### Test Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@smartfarming.com",
    "password": "admin123"
  }'
```

### Test Protected Endpoint
```bash
# First, get token from login, then:
curl http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Project Structure Quick Reference

```
📁 backend/
  ├── 📄 app.py                 # Main Flask app
  ├── 📁 models/
  │   ├── 📄 database.py        # Database models
  │   ├── 📄 crop_recommendation.py
  │   └── 📄 fertilizer_recommendation.py
  └── 📁 utils/
      └── 📄 auth.py            # Authentication

📁 frontend/
  ├── 📁 src/
  │   ├── 📄 App.js             # Main React component
  │   └── 📁 components/
  │       ├── 📄 LandingPage.js # Homepage
  │       ├── 📁 auth/          # Login, Register
  │       └── 📁 portals/       # Role-based dashboards
  └── 📄 package.json
```

---

## Next Steps

1. **Explore Features**: Try all role-based portals
2. **Read Documentation**: Check [README.md](README.md) for detailed info
3. **API Reference**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
4. **Project Details**: Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## Getting Help

- 📖 Check [README.md](README.md) for comprehensive documentation
- 🔍 Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- 📝 Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture overview
- 🐛 Check error messages carefully - they're usually descriptive
- 💬 Create an issue on GitHub for bugs or questions

---

## Production Deployment

For production deployment, see the **Production Deployment** section in [README.md](README.md).

Key points:
- Use PostgreSQL instead of SQLite
- Set strong JWT secret key
- Enable HTTPS
- Build React app: `npm run build`
- Use production WSGI server (Gunicorn)

---

🎉 **Congratulations!** You're now running the Smart Farming Platform!

Enjoy exploring the features and building on this foundation. Happy farming! 🌾

---

**Quick Start Guide** - Smart Farming Platform  
*Get started in 5 minutes or less*

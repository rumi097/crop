# Railway Deployment Guide for Smart Farming Platform

## Prerequisites
- GitHub account with your code pushed
- Railway account (sign up at railway.app)

## Deployment Steps

### 1. Sign Up / Login to Railway
- Go to https://railway.app
- Sign in with GitHub

### 2. Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository: `rumi097/crop`
- Railway will auto-detect your Python backend

### 3. Configure Environment Variables (Optional)
In Railway dashboard, go to Variables and add:
```
PORT=5001
FLASK_ENV=production
```

### 4. Deploy Backend
Railway will automatically:
- Detect Python and install dependencies from requirements.txt
- Run the gunicorn server (via Procfile)
- Provide a public URL like: https://your-app.up.railway.app

### 5. Update Frontend API URL
After backend is deployed, you'll get a URL. Update your frontend:

In `frontend/src/` files, replace:
```javascript
axios.defaults.baseURL = 'http://localhost:5001';
```
with:
```javascript
axios.defaults.baseURL = 'https://your-backend-url.up.railway.app';
```

### 6. Deploy Frontend (Optional - Separate Service)
Railway can also host your React build:
- Add another service in same project
- Point to same repo
- Set root directory to `frontend`
- Build command: `npm install && npm run build`
- Start command: `npx serve -s build -p $PORT`

OR deploy frontend separately on Vercel/Netlify and keep backend on Railway.

### 7. Database Persistence
Railway provides persistent disk storage, so your SQLite database will be preserved across deployments.

### 8. Push Updates
After initial deployment, any push to GitHub main branch will auto-deploy:
```bash
git add .
git commit -m "Update message"
git push origin main
```

## Important Notes

1. **Free Tier**: Railway offers $5/month free credits (enough for development)
2. **Database**: SQLite works on Railway with persistent storage
3. **ML Models**: Your saved_models/ folder will be included
4. **CORS**: Already configured to accept all origins
5. **Port**: Uses Railway's dynamic PORT environment variable

## Troubleshooting

- Check Railway logs if deployment fails
- Ensure all dependencies are in requirements.txt
- Verify gunicorn is installed (now added)
- Check that PORT environment variable is used

## Public URL
After deployment, your app will be available at:
- Backend: https://[your-project].up.railway.app
- API endpoints: https://[your-project].up.railway.app/api/...

## Cost Estimate (Free Tier)
- First 500 hours/month: FREE
- Beyond that: ~$0.01/hour
- Should stay within free tier for demo/development use

# 🚀 HackHazard 2026 - Deployment Guide

**Domain**: alitatech.xyz  
**Repository**: https://github.com/Lakshdeep12/HackHazard-2026-  
**Status**: 🔴 Not deployed yet (showing 404)

---

## 📋 What You Have

✅ **Frontend**: React/TanStack dashboard (builds successfully)  
✅ **Backend**: FastAPI with websockets, auth, vector search  
✅ **Domain**: CNAME configured  
✅ **GitHub**: Repository ready  
❌ **Vercel**: Not connected yet  
❌ **Backend Host**: Not set up yet

---

## 🎯 Quick Setup (5-10 minutes)

### Step 1: Prepare Repository

Before deploying, update your `.gitignore` to NOT ignore the built frontend:

```bash
# Edit Dashboard/.gitignore
# Remove or comment out this line:
# dist

# Alternative: Add to Dashboard/.gitignore
!dist/
!dist/**/*
```

**Why?** Vercel needs the `Dashboard/dist/client` folder to deploy.

Then commit:
```bash
cd "d:\HackHazard 2026"
git add -A
git commit -m "Build: Prepare for Vercel deployment"
git push origin main
```

### Step 2: Deploy Frontend to Vercel

1. **Go to**: https://vercel.com/
2. **Sign up/Log in** with GitHub
3. **Click**: "Import Project"
4. **Select**: `Lakshdeep12/HackHazard-2026-`
5. **Configure**:
   - **Build Command**: `cd Dashboard && npm install && npm run build`
   - **Output Directory**: `Dashboard/dist/client`
   - **Framework**: Other (Vite)
6. **Environment Variables** (optional for now):
   - `NEXT_PUBLIC_API_BASE_URL` = `https://api.guardaiian.example.com`
7. **Deploy!** 🚀

**Result**: Your site will be live at `https://alitatech.xyz` in ~3-5 minutes

### Step 3: Deploy Backend (Choose One)

#### Option A: Render.com (Recommended - Free tier)

1. **Go to**: https://render.com/
2. **Sign up** with GitHub
3. **Click**: "New +" → "Web Service"
4. **Select**: Your GitHub repo
5. **Configure**:
   - **Name**: `hackhazard-backend`
   - **Runtime**: Docker
   - **Build**: `cd Backend && docker build -t app .`
   - **Start**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. **Environment Variables**:
   ```
   APP_ENV=prod
   BACKEND_CORS_ORIGINS=["https://alitatech.xyz"]
   REDIS_URL=(skip for now, or add Redis addon)
   JWT_SECRET_KEY=generate-random-secret-key
   DATABASE_URL=sqlite+aiosqlite:///./guardaiian.db
   ```
7. **Deploy!**

**Result**: Backend will be at `https://hackhazard-backend.onrender.com`

#### Option B: Railway.app

1. **Go to**: https://railway.app/
2. **Create new project** → Import from GitHub
3. **Select** your repo
4. **Select** Dockerfile
5. **Add environment variables** (same as above)
6. **Deploy!**

### Step 4: Connect Frontend to Backend

After backend is running, update the frontend environment:

**Edit**: `Dashboard/.env.production`
```
VITE_API_BASE_URL=https://hackhazard-backend.onrender.com
VITE_WS_URL=wss://hackhazard-backend.onrender.com/api/v1/ws/alerts
```

Then redeploy:
```bash
cd Dashboard
npm run build
git add .
git commit -m "chore: Update backend URLs for production"
git push origin main
```

Vercel will auto-rebuild! ✨

### Step 5: Test Everything

1. Visit https://alitatech.xyz
2. Check browser console for any errors
3. Try logging in or accessing API features
4. Check WebSocket connection (if applicable)

---

## 📊 Current Issues to Fix

### Issue 1: 404 Page
**Cause**: Root `index.html` is a placeholder, Vercel not configured  
**Fix**: Deploy to Vercel following Step 2 above

### Issue 2: Backend URL Not Set
**Cause**: `.env.production` has example URL  
**Fix**: Update after backend deployment (Step 4)

### Issue 3: Missing Environment Secrets
**Cause**: Backend needs API keys for LLMs, auth tokens  
**Fix**: Set in deployment platform's environment section

---

## 🔧 Local Development

To run locally before deploying:

### Frontend:
```bash
cd Dashboard
npm install
npm run dev
# Visit http://localhost:5173
```

### Backend:
```bash
cd Backend
pip install -r requirements.txt
# Set .env or .env.local
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
# Visit http://localhost:8000/docs
```

---

## ✅ Deployment Checklist

- [ ] GitHub repo has all commits pushed
- [ ] Vercel account created
- [ ] Vercel project connected to repo
- [ ] Build command set: `cd Dashboard && npm install && npm run build`
- [ ] Output directory set: `Dashboard/dist/client`
- [ ] Frontend deployed and shows dashboard (not 404)
- [ ] Backend hosting chosen (Render/Railway)
- [ ] Backend environment variables configured
- [ ] Backend deployed and health check passes
- [ ] Frontend `.env.production` updated with backend URL
- [ ] Frontend redeployed
- [ ] Integration tested (frontend calls backend API)

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Still showing 404 | Make sure Vercel is building `Dashboard/dist/client` |
| Backend 502 error | Check environment variables, database connection |
| CORS errors | Ensure `BACKEND_CORS_ORIGINS` includes Vercel URL |
| WebSocket fails | Check WSS URL is correct, not WS |
| Build times out | Increase timeout in Vercel settings |

---

## 📞 Next Steps

1. **Complete** the deployment steps above
2. **Monitor** builds on Vercel and Render dashboards
3. **Test** the live site
4. **Iterate** on any issues

Once deployed, your project will be live! 🎉

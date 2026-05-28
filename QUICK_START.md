# ⚡ Quick Start - Deploy HackHazard 2026 in 10 Minutes

## 🎯 Goal
Get your frontend live at **alitatech.xyz** and backend running

## 📋 Prerequisites
- ✅ GitHub account (already have repo)
- ✅ Vercel account (free)
- ✅ Render.com or Railway account (free tier)

---

## 🚀 5-Step Deployment

### STEP 1: Verify Local Build (2 min)
```bash
cd "d:\HackHazard 2026\Dashboard"
npm run build
# Should create Dashboard/dist/client/
```

### STEP 2: Push to GitHub (1 min)
```bash
cd "d:\HackHazard 2026"
git add -A
git commit -m "feat: Prepare for production deployment"
git push origin main
```

### STEP 3: Deploy Frontend to Vercel (3 min)

**Go to:** https://vercel.com/new

1. Click **"Import Project"**
2. Select **`Lakshdeep12/HackHazard-2026-`**
3. Configure:
   - Framework Preset: **"Other"**
   - Build Command: `cd Dashboard && npm install && npm run build`
   - Output Directory: `Dashboard/dist/client`
4. Click **"Deploy"** 🚀

Wait ~3-5 minutes → Your site is now LIVE! 🎉

### STEP 4: Deploy Backend to Render (5 min)

**Go to:** https://render.com

1. Click **"New +"** → **"Web Service"**
2. Connect GitHub account and select repo
3. Configure:
   - **Name:** `hackhazard-backend`
   - **Runtime:** Select **"Docker"**
   - **Branch:** `main`
   - **Build Command:** (leave empty for Dockerfile)
   - **Start Command:** (leave empty for Dockerfile)
4. **Environment Variables:**
   Copy and paste variables from `Backend/.env.render`
   - Change these to strong random values:
     - `JWT_SECRET_KEY` = [generate random string]
     - `DASHBOARD_API_KEY` = [generate random string]
     - `DASHBOARD_ADMIN_PASSWORD` = [strong password]
5. Click **"Create Web Service"** 🚀

Wait ~5-10 minutes for build. Once ready, note your backend URL (like `https://hackhazard-backend.onrender.com`)

### STEP 5: Connect Frontend to Backend (2 min)

1. Go to your **Vercel Dashboard**
2. Open your project
3. Go to **Settings** → **Environment Variables**
4. Add/Update:
   ```
   VITE_API_BASE_URL=https://hackhazard-backend.onrender.com
   VITE_WS_URL=wss://hackhazard-backend.onrender.com/api/v1/ws/alerts
   ```
5. Go to **Deployments** → Click redeploy on latest deployment

Wait ~2-3 minutes for rebuild.

---

## ✅ You're Done!

Visit **https://alitatech.xyz** and your site should be live! 🎉

### Verify it works:
- [ ] Can see the dashboard (not a 404 page)
- [ ] Can access different dashboard sections
- [ ] API calls are working (check browser DevTools → Network)
- [ ] No CORS errors in console

---

## 🔧 Troubleshooting

### Still seeing 404?
- Check Vercel deployment finished (green checkmark)
- Verify output directory is `Dashboard/dist/client`

### Backend not responding?
- Check Render logs for errors
- Verify environment variables are set
- Check health endpoint: `/api/v1/health`

### CORS errors?
- Make sure `BACKEND_CORS_ORIGINS` includes `https://alitatech.xyz`

### Changes not showing up?
- Trigger rebuild in Vercel dashboard
- Clear browser cache (Ctrl+Shift+R)

---

## 🎓 What's Running

| Component | URL | Technology |
|-----------|-----|-----------|
| Frontend | https://alitatech.xyz | React + Vite + Vercel |
| Backend API | https://hackhazard-backend.onrender.com | FastAPI + Render |
| API Docs | `.../api/v1/docs` | SwaggerUI |
| Health Check | `.../api/v1/health` | JSON response |

---

## 📝 Next Steps

1. **Monitor Deployments:**
   - Vercel Dashboard: https://vercel.com/dashboard
   - Render Dashboard: https://dashboard.render.com

2. **Add Custom Domain** (optional):
   - Already configured: CNAME → alitatech.xyz

3. **Configure More:**
   - Add database (PostgreSQL on Render)
   - Add Redis for rate limiting
   - Set up monitoring

---

## 💡 Pro Tips

- **Auto-redeploy**: Both Vercel and Render watch your GitHub repo
- **Push to main** = Auto-deploy to production
- **Local testing**: Use `npm run dev` in Dashboard + run backend locally
- **Logs**: Check Vercel/Render dashboards for errors

---

**Questions?** Check `DEPLOYMENT.md` for detailed guide!

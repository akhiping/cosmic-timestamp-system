# Deployment Guide - Cosmic Timestamp System

## ✅ Ready for Render Deployment

Your app is now configured to deploy on Render. Here's what was fixed:

### Changes Made:

1. **Flask App (`src/04_build_web_demo.py`)**:
   - ✅ Now binds to `0.0.0.0` instead of `localhost` (required for Render)
   - ✅ Uses `PORT` environment variable from Render
   - ✅ Absolute paths for CSV file (works in production)

2. **Dependencies (`requirements.txt`)**:
   - ✅ Added `gunicorn` for production server
   - ✅ Cleaned up commented-out packages

3. **WSGI Entry Point (`wsgi.py`)**:
   - ✅ Created production-ready entry point
   - ✅ Handles the numbered Python file (`04_build_web_demo.py`)

4. **Render Configuration (`render.yaml`)**:
   - ✅ Fixed to run from `cosmic-timestamp-system/` directory
   - ✅ Uses Gunicorn as production server
   - ✅ Proper build and start commands

5. **Git Ignore (`.gitignore`)**:
   - ✅ Added `venv/` and `__pycache__/` 
   - ✅ Removed committed venv (was confusing Render's detection)

---

## 🚀 Deploy to Render

### Option 1: Using Dashboard (Recommended)

1. **Push your code to GitHub:**
   ```bash
   cd /home/akhiping/Documents/Mantaray
   git add cosmic-timestamp-system/
   git commit -m "Fix Render deployment configuration"
   git push
   ```

2. **In Render Dashboard:**
   - Go to: https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render will auto-detect `render.yaml`
   - Click "Apply" to use the config
   - Click "Create Web Service"

3. **Wait for deployment** (~2-3 minutes)
   - Render will run `pip install -r requirements.txt`
   - Then start the app with Gunicorn
   - Your site will be live at: `https://cosmic-timestamp-system.onrender.com`

### Option 2: Using Render CLI

```bash
# Install Render CLI
pip install render

# Login
render login

# Deploy
cd cosmic-timestamp-system
render deploy
```

---

## 📋 Deployment Checklist

Before deploying, verify:

- [ ] `cosmic-timestamp-system/render.yaml` exists
- [ ] `cosmic-timestamp-system/requirements.txt` exists  
- [ ] `cosmic-timestamp-system/output/frb_fingerprints_enhanced.csv` exists
- [ ] `cosmic-timestamp-system/templates/index.html` exists
- [ ] `venv/` directory is removed (not committed)
- [ ] Code is pushed to GitHub

---

## 🔍 Troubleshooting

### If Render build fails:

**"requirements.txt not found"**
- ✅ FIXED: `render.yaml` now includes `cd cosmic-timestamp-system`

**"Module not found"**  
- ✅ FIXED: Using `wsgi.py` as entry point

**"Cannot bind to port"**
- ✅ FIXED: App now uses `$PORT` environment variable

### If app starts but doesn't load:

1. Check Render logs (Dashboard → your service → "Logs" tab)
2. Look for errors loading CSV file:
   ```
   FileNotFoundError: frb_fingerprints_enhanced.csv
   ```
   - ✅ Should be fixed with absolute paths

3. Check if Flask routes are registered:
   ```
   You should see: /, /api/frbs, /api/seal, /api/verify
   ```

### If you get a blank page:

- Check browser console (F12) for JavaScript errors
- Check Network tab for failed API calls
- Verify `/api/frbs` returns JSON data

---

## 🌐 Alternative: Deploy to PythonAnywhere

If Render still has issues, try PythonAnywhere (simpler for Flask):

1. Create account at: https://www.pythonanywhere.com
2. Upload your code
3. Set up web app:
   - Python version: 3.10
   - Framework: Flask  
   - WSGI file points to: `/home/yourusername/cosmic-timestamp-system/wsgi.py`
4. Install requirements in console:
   ```bash
   pip install --user -r requirements.txt
   ```
5. Reload web app

---

## 📝 What to Do After Deployment

1. **Test the live site:**
   - Visit your Render URL
   - Click "Available FRBs" - should load FRB list
   - Try sealing a document
   - Verify the seal

2. **Update README.md:**
   - Replace `[Try it here](#)` with your actual URL
   - Example: `[Try it here](https://cosmic-timestamp-system.onrender.com)`

3. **Share your project:**
   - Add the live URL to your GitHub repo description
   - Share on Twitter/LinkedIn with #FRB #Astronomy #Cryptography

---

## 🎉 Your Site is Ready!

Once deployed, your Cosmic Timestamp System will be publicly accessible. Anyone can:
- View available Fast Radio Bursts
- Seal documents with FRB timestamps
- Verify cosmic seals

**Live URL:** `https://cosmic-timestamp-system.onrender.com` (or your custom domain)

---

## 💡 Next Steps (Optional)

1. **Custom Domain:** Connect your own domain in Render settings
2. **HTTPS:** Render provides free SSL/TLS automatically
3. **Monitoring:** Set up health checks and alerts
4. **Scaling:** Upgrade to paid tier if traffic grows

---

**Questions?** Check the main README.md or Render documentation.


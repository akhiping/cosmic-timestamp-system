# 🚀 QUICK START: Deploy Your Cosmic Timestamp System

## Push to GitHub and Deploy to Render (5 minutes)

```bash
# 1. Navigate to your repo root
cd /home/akhiping/Documents/Mantaray

# 2. Add all changes
git add .

# 3. Commit
git commit -m "Fix Render deployment - move render.yaml to root"

# 4. Push to GitHub
git push origin main
```

## Then in Render Dashboard:

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Click **"Apply"** then **"Create Web Service"**

## That's it! 🎉

Your site will be live at:  
`https://cosmic-timestamp-system.onrender.com`

(Render will give you the exact URL)

---

## If Something Goes Wrong:

Check the **"Logs"** tab in your Render service dashboard to see error messages.

Most common issues are already fixed in the configuration files.

---

## Test Locally First (Optional):

```bash
cd cosmic-timestamp-system
python3 src/04_build_web_demo.py
# Visit http://localhost:5000
```

If it works locally, it will work on Render.


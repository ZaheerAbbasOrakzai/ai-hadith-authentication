# PythonAnywhere Deployment Guide

## Why PythonAnywhere?
- Designed specifically for Python web apps
- Built-in Flask support
- Persistent file storage (SQLite works)
- Always running (no cold starts)
- File uploads work
- Free tier available

## Deployment Steps

### Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com
2. Click "Create a free account"
3. Use your email: abbas02082000@gmail.com
4. Choose a username (e.g., zaheerabbas)
5. Verify your email

### Step 2: Create a Web App
1. Login to PythonAnywhere
2. Go to "Web" tab
3. Click "Add a new web app"
4. Click "Next"
5. Choose "Flask" framework
6. Choose "Python 3.9" (or latest)
7. Click "Next"
8. Enter path: `/home/zaheerabbas/ai-hadith-authenticator` (use your username)
9. Click "Next"

### Step 3: Upload Your Code

**Option A: Using Git (Recommended)**
1. Go to "Consoles" tab
2. Click "Bash"
3. Run these commands:
   ```bash
   cd ~
   git clone https://github.com/ZaheerAbbasOrakzai/ai-hadith-authentication.git
   cd ai-hadith-authentication
   pip install -r requirements-render.txt
   ```

**Option B: Using Drag & Drop**
1. Go to "Files" tab
2. Navigate to your home directory
3. Click "Upload a file or directory"
4. Upload your entire project folder

### Step 4: Configure Web App
1. Go to "Web" tab
2. Find "Code" section
3. Update "Working directory": `/home/zaheerabbas/ai-hadith-authentication`
4. Update "WSGI configuration file": `/home/zaheerabbas/ai-hadith-authenticator/ai_hadith_wsgi.py`

### Step 5: Create WSGI File
1. Go to "Files" tab
2. Navigate to `/home/zaheerabbas/ai-hadith-authentication/`
3. Create new file: `ai_hadith_wsgi.py`
4. Add this content:
   ```python
   import sys
   import os

   # Add your project directory to the Python path
   project_home = '/home/zaheerabbas/ai-hadith-authenticator'
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path

   # Import your Flask app
   from app import app as application

   # Make sure app is in production mode
   application.config['DEBUG'] = False
   ```

### Step 6: Install Dependencies
1. Go to "Consoles" tab
2. Click "Bash"
3. Run:
   ```bash
   cd ~/ai-hadith-authentication
   pip install -r requirements-render.txt
   ```

### Step 7: Set Environment Variables
1. Go to "Web" tab
2. Scroll to "Environment variables" section
3. Add these variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   MONGODB_URI=mongodb://localhost:27017/hadith_db
   ```

### Step 8: Reload Web App
1. Go to "Web" tab
2. Click the green "Reload" button
3. Wait a few seconds
4. Check the log files if there are errors

### Step 9: Access Your App
Your app will be live at:
```
https://zaheerabbas.pythonanywhere.com
```
(Replace zaheerabbas with your username)

## Troubleshooting

### If you get "Module not found" errors:
- Make sure all dependencies are installed
- Check the virtual environment is activated
- Run `pip install -r requirements-render.txt` again

### If you get database errors:
- SQLite database will be created automatically
- Make sure the directory has write permissions

### If you get 500 errors:
- Check the error log in "Web" tab
- Look at the server log for detailed error messages

### If file uploads don't work:
- Make sure the uploads directory exists
- Check directory permissions

## Custom Domain (Optional)

1. Go to "Web" tab
2. Find "Web app" section
3. Click "Add a custom domain"
4. Enter your domain (e.g., www.yourdomain.com)
5. Update DNS records as instructed

## Monitoring

- Check logs in "Web" tab → "Log files"
- Monitor CPU usage in "Account" tab
- Check disk space in "Files" tab

## Upgrading to Paid Plan

If you need more resources:
- Go to "Account" tab
- Click "Upgrade"
- Paid plans start at $5/month
- More RAM, CPU, and bandwidth

## Support

- PythonAnywhere forums: https://www.pythonanywhere.com/forums/
- Documentation: https://help.pythonanywhere.com/

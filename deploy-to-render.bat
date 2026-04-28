@echo off
echo ========================================
echo AI Hadith Authenticator - Deployment
echo ========================================
echo.

echo Step 1: Create GitHub Repository
echo 1. Go to https://github.com/new
echo 2. Repository name: ai-hadith-authenticator
echo 3. Make it Public
echo 4. Click "Create repository"
echo.
pause

echo.
echo Step 2: Push to GitHub
echo.
git remote add origin https://github.com/YOUR_USERNAME/ai-hadith-authenticator.git
echo.
echo IMPORTANT: Replace YOUR_USERNAME with your actual GitHub username in the command above!
echo.
pause

echo.
git branch -M main
git push -u origin main
echo.

echo ========================================
echo Step 3: Deploy to Render
echo ========================================
echo.
echo 1. Go to https://render.com
echo 2. Sign up/login with your email: abbas02082000@gmail.com
echo 3. Click "New +" -> "Web Service"
echo 4. Connect your GitHub repository
echo 5. Select "ai-hadith-authenticator"
echo 6. Render will auto-detect the render.yaml file
echo 7. Click "Create Web Service"
echo 8. Wait 2-3 minutes for deployment
echo.
echo Your app will be live at: https://ai-hadith-authenticator.onrender.com
echo.
pause

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo IMPORTANT: After deployment, set these environment variables in Render:
echo - FLASK_ENV=production
echo - SECRET_KEY=generate-a-secure-key
echo - MONGODB_URI=mongodb://localhost:27017/hadith_db
echo - MAIL_USERNAME=your-email@gmail.com (optional)
echo - MAIL_PASSWORD=your-app-password (optional)
echo.
echo For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
pause

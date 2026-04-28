@echo off
echo ========================================
echo Step 1: GitHub Repository Setup
echo ========================================
echo.
echo 1. Open your browser and go to: https://github.com/new
echo 2. Repository name: ai-hadith-authenticator
echo 3. Description: AI-Powered Hadith Authentication System
echo 4. Make it PUBLIC
echo 5. Click "Create repository"
echo.
echo IMPORTANT: After creating, copy your repository URL!
echo It will look like: https://github.com/YOUR_USERNAME/ai-hadith-authenticator.git
echo.
pause

echo.
echo ========================================
echo Step 2: Enter Your GitHub Username
echo ========================================
echo.
set /p GITHUB_USERNAME="Enter your GitHub username: "

echo.
echo ========================================
echo Step 3: Push to GitHub
echo ========================================
echo.
git remote add origin https://github.com/%GITHUB_USERNAME%/ai-hadith-authenticator.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo Success! Code pushed to GitHub
echo ========================================
echo.
echo Your repository: https://github.com/%GITHUB_USERNAME%/ai-hadith-authenticator
echo.
pause

echo.
echo ========================================
echo Step 4: Deploy to Render
echo ========================================
echo.
echo 1. Go to https://render.com
echo 2. Sign up/login with: abbas02082000@gmail.com
echo 3. Click "New +" -> "Web Service"
echo 4. Click "Connect GitHub repository"
echo 5. Find and select: ai-hadith-authenticator
echo 6. Render will auto-detect Python and render.yaml
echo 7. Click "Create Web Service"
echo 8. Wait 2-3 minutes for deployment
echo.
echo Your app will be live at: https://ai-hadith-authenticator.onrender.com
echo.
start https://render.com
echo.
pause

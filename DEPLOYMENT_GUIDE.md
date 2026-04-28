# Deployment Guide - AI Hadith Authenticator

## Why Render Instead of Netlify?

Your Flask app requires:
- **SQLite database** (stateful - not supported by Netlify Functions)
- **File uploads** (persistent storage needed)
- **Session management** (stateful)
- **MongoDB connections** (continuous connection)

**Render** provides all these features for FREE, while Netlify is designed for static sites and serverless functions.

## Deployment Steps (Render - FREE)

### Option 1: Deploy via Render Dashboard (Recommended)

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up with your email: abbas02082000@gmail.com
   - Verify your email

2. **Connect Your GitHub Repository**
   - Push your code to GitHub
   - In Render dashboard, click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Select the `ai-hadith-authenticator` repo

3. **Configure Build Settings**
   - **Name**: ai-hadith-authenticator
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements-render.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`

4. **Set Environment Variables**
   - Go to "Environment" tab
   - Add these variables:
     ```
     FLASK_ENV=production
     SECRET_KEY=your-secret-key-here
     MONGODB_URI=mongodb://localhost:27017/hadith_db
     MAIL_USERNAME=your-email@gmail.com
     MAIL_PASSWORD=your-app-password
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Your app will be live at: `https://ai-hadith-authenticator.onrender.com`

### Option 2: Deploy via Render CLI

1. **Install Render CLI**
   ```bash
   npm install -g @render/cli
   ```

2. **Login to Render**
   ```bash
   render login
   ```
   - Enter your email: abbas02082000@gmail.com
   - Verify via email link

3. **Initialize Project**
   ```bash
   cd c:\Users\abbas\Desktop\ai-hadith-authenticator
   render init
   ```

4. **Deploy**
   ```bash
   render deploy
   ```

## Post-Deployment Setup

### 1. Database Setup
The SQLite database (`users.db`) will be created automatically on first run.

### 2. MongoDB Setup (Optional)
If you want to use MongoDB instead of SQLite:
- Create a free MongoDB Atlas account
- Get your connection string
- Update `MONGODB_URI` environment variable in Render

### 3. Email Setup (Optional)
For email features:
- Use Gmail App Password (not your regular password)
- Update `MAIL_USERNAME` and `MAIL_PASSWORD` in Render

### 4. File Uploads
Render provides ephemeral storage. For persistent file storage:
- Use AWS S3 (free tier available)
- Or use Cloudflare R2 (free tier available)
- Update file upload code to use cloud storage

## Troubleshooting

### App won't start
- Check Render logs in dashboard
- Ensure `requirements-render.txt` is present
- Check Python version compatibility

### Database errors
- SQLite will auto-create on first run
- Ensure write permissions in the app directory

### Timeout errors
- Increase timeout in start command (currently 120s)
- Optimize database queries

## Free Tier Limits (Render)

- **512 MB RAM**
- **0.1 CPU**
- **512 MB Disk**
- **Spins down after 15 minutes of inactivity**
- **Cold start: ~30 seconds**

## Alternative: Railway (Also FREE)

If you prefer Railway:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python
6. Add environment variables
7. Deploy!

## Alternative: Fly.io (Also FREE)

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Initialize: `fly launch`
4. Deploy: `fly deploy`

## Monitoring Your App

- **Render Dashboard**: View logs, metrics, and status
- **Uptime**: https://status.render.com
- **Your App Logs**: Available in Render dashboard

## Updating Your App

1. Make changes locally
2. Commit and push to GitHub
3. Render auto-deploys on push
4. Wait 2-3 minutes for deployment

## Custom Domain (Optional)

1. Go to Render dashboard
2. Select your service
3. Go to "Settings" → "Domains"
4. Add your custom domain
5. Update DNS records

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Your Email**: abbas02082000@gmail.com

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Repository connected to Render
- [ ] Environment variables set
- [ ] App deployed successfully
- [ ] App accessible at URL
- [ ] Database working
- [ ] File uploads working
- [ ] Email configured (if needed)

## Next Steps

After successful deployment:
1. Test all features
2. Set up monitoring alerts
3. Configure custom domain (optional)
4. Set up backup strategy
5. Monitor usage and performance

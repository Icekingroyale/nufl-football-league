# Deploying to Choreo

This guide will help you deploy your Football League Management System to Choreo, an AI-native internal developer platform.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository
3. A Choreo account (sign up at https://choreo.dev/)

## Deployment Steps

### 1. Prepare Your Repository

Your repository is already configured for Choreo deployment with:
- `choreo.json` - Service configuration
- `backend/Dockerfile` - Backend containerization
- `frontend/Dockerfile` - Frontend containerization
- `frontend/nginx.conf` - Nginx configuration for React routing

### 2. Deploy to Choreo

1. **Sign up/Login to Choreo**
   - Go to https://choreo.dev/
   - Sign up with your GitHub account

2. **Create a New Project**
   - Click "Create Project"
   - Choose "Deploy from Git"
   - Select your GitHub repository

3. **Configure Services**
   - Choreo will automatically detect the `choreo.json` configuration
   - It will create two services:
     - `football-league-backend` (Python/Flask)
     - `football-league-frontend` (React/Vite)

4. **Set Environment Variables**
   - For the backend service:
     - `FLASK_APP=app.py`
     - `FLASK_ENV=production`
     - `SECRET_KEY=your-secret-key-here`
   - For the frontend service:
     - `VITE_API_URL=https://your-backend-service-url.choreo.dev`

5. **Deploy**
   - Click "Deploy" to start the deployment process
   - Choreo will build and deploy both services

### 3. Post-Deployment Configuration

1. **Update Frontend API URL**
   - Once deployed, get your backend service URL
   - Update the frontend environment variable `VITE_API_URL` with the actual backend URL

2. **Test the Application**
   - Visit your frontend URL
   - Test admin login functionality
   - Verify all features work correctly

## Advantages of Choreo

- **Built-in Authentication**: No need to handle complex auth setup
- **Docker Support**: Full containerization support
- **Auto-scaling**: Automatic scaling based on traffic
- **Monitoring**: Built-in observability and monitoring
- **Multi-cloud**: Deploy across different cloud providers
- **Free Tier**: Generous free tier for development

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure the backend CORS configuration includes your frontend URL
   - Check that `supports_credentials=True` is set

2. **Database Issues**
   - The SQLite database will be created automatically on first run
   - Sample data will be populated automatically

3. **Build Failures**
   - Check the build logs in Choreo dashboard
   - Ensure all dependencies are in `requirements.txt` and `package.json`

### Getting Help

- Check Choreo documentation: https://choreo.dev/docs
- Join Choreo community: https://discord.gg/choreo
- Review build logs in the Choreo dashboard

## Environment Variables Reference

### Backend Environment Variables
- `FLASK_APP=app.py` - Flask application entry point
- `FLASK_ENV=production` - Production environment
- `SECRET_KEY=your-secret-key` - Flask secret key for sessions
- `DATABASE_URL=/app/football_league.db` - Database path
- `UPLOAD_FOLDER=/app/uploads` - Upload directory

### Frontend Environment Variables
- `VITE_API_URL=https://your-backend-url.choreo.dev` - Backend API URL

## Security Notes

- Generate a strong `SECRET_KEY` for production
- Use environment variables for sensitive configuration
- Enable HTTPS in production (handled by Choreo)
- Regularly update dependencies for security patches 
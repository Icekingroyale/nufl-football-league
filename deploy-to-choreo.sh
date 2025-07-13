#!/bin/bash

# Deploy to Choreo Script
# This script helps prepare your application for Choreo deployment

echo "🚀 Preparing Football League App for Choreo Deployment"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git and push to GitHub first."
    exit 1
fi

# Check if all required files exist
echo "📋 Checking required files..."

required_files=(
    "choreo.json"
    "backend/Dockerfile"
    "frontend/Dockerfile"
    "frontend/nginx.conf"
    "backend/requirements.txt"
    "frontend/package.json"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - Missing!"
        exit 1
    fi
done

echo ""
echo "✅ All required files are present!"
echo ""

# Generate a secret key for production
echo "🔑 Generating secret key for production..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
echo "Generated SECRET_KEY: $SECRET_KEY"
echo ""

# Instructions
echo "📝 Next Steps:"
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Prepare for Choreo deployment'"
echo "   git push origin main"
echo ""
echo "2. Go to https://choreo.dev/ and sign up/login"
echo ""
echo "3. Create a new project and select 'Deploy from Git'"
echo ""
echo "4. Select your GitHub repository"
echo ""
echo "5. Set these environment variables in Choreo:"
echo "   Backend Service:"
echo "   - FLASK_APP=app.py"
echo "   - FLASK_ENV=production"
echo "   - SECRET_KEY=$SECRET_KEY"
echo ""
echo "   Frontend Service:"
echo "   - VITE_API_URL=https://your-backend-service-url.choreo.dev"
echo ""
echo "6. Deploy and enjoy your free hosting! 🎉"
echo ""
echo "📚 For detailed instructions, see CHOREO_DEPLOYMENT.md" 
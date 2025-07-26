import os
from app import create_app

# Create the Flask application instance
app = create_app()

# This is for production WSGI servers like Gunicorn
if __name__ == "__main__":
    # Only used for direct execution, not recommended for production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
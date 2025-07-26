import os
from flask import Flask, request, make_response
from flask_cors import CORS

# Import blueprints (to be created)
def create_app():
    app = Flask(__name__)
    # Ensure the database directory exists
    db_dir = os.path.dirname(__file__)
    os.makedirs(db_dir, exist_ok=True)
    app.config['DATABASE'] = os.path.join(db_dir, 'football_league.db')
    # Ensure the uploads directory exists
    uploads_dir = os.path.join(db_dir, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = uploads_dir
    app.secret_key = os.environ.get('SECRET_KEY', 'your-very-secret-key')

    # Configure CORS for production - allow all origins temporarily for debugging
    CORS(app, 
         supports_credentials=True,
         origins=['*'],  # Allow all origins temporarily
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         expose_headers=['Set-Cookie'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

    # Add CORS preflight handler
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,X-Requested-With")
            response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response

    # Register blueprints
    from .routes.teams import teams_bp
    from .routes.players import players_bp
    from .routes.fixtures import fixtures_bp
    from .routes.news import news_bp
    from .routes.auth import auth_bp
    from .routes.uploads import uploads_bp
    from .routes.misc import misc_bp

    app.register_blueprint(teams_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(fixtures_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(misc_bp)

    # Import models and utils if needed
    from . import models, utils

    # Initialize DB if needed
    models.init_db(app)

    return app 
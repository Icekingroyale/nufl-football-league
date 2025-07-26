import os
from flask import Flask
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

    # Configure CORS for production
    CORS(app, 
         supports_credentials=True,
         origins=['https://nufl.netlify.app', 'http://localhost:5173', 'http://localhost:3000'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         expose_headers=['Set-Cookie'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

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
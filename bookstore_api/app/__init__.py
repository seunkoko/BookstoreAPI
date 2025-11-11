import os

from flask import Flask
from dotenv import load_dotenv
from .extensions import db, migrate, ma

# Import config
from .config import DevelopmentConfig, ProductionConfig, TestConfig
# Import routes
from .routes import auth_bp, api_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # Load configuration based of FLASK_ENV environment variable
    env_name = os.getenv("FLASK_ENV")
    if env_name == 'production':
        app.config.from_object(ProductionConfig)
    elif env_name == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(TestConfig)

    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    return app

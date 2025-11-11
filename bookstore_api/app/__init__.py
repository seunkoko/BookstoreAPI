import os

from flask import Flask, jsonify
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from .extensions import db, migrate, ma
from .helpers import ApiError
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

    @app.errorhandler(404)
    def resource_not_found(exception):
        """Return custom JSON when resource does not exist"""
        default_message = "The requested item could not be found."
        return jsonify({
            "status": 'fail',
            "error": exception.description if hasattr(exception, "description") else default_message
        }), 404
    
    @app.errorhandler(ApiError)
    def api_error_handler(error):
        """Return custom JSON when ApiError is raised"""
        # Add some logging so that we can monitor different types of errors
        app.logger.error(f"{error.to_dict()}")

        return jsonify({
            "status": 'fail',
            "error": error.message
        }), error.status_code
    
    @app.errorhandler(HTTPException)
    def api_httpException_handler(error):
        """Return custom JSON when HttpException is raised"""
        # Add some logging so that we can monitor different types of errors
        app.logger.error(f"{error}")

        return jsonify({
            "status": 'fail',
            "error": error.description
        }), error.code

    with app.app_context():
        db.create_all()

    return app

import os

from flask import Flask
from dotenv import load_dotenv
# Import config
from .config import DevelopmentConfig, ProductionConfig, TestConfig

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load configuration based of FLASK_ENV environment variable
    env_name = os.getenv("FLASK_ENV")

    if env_name == 'production':
        app.config.from_object(ProductionConfig)
    elif env_name == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(TestConfig)

    return app

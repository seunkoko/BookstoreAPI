import os

from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base configuration settings
    ENV = 'base'
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=3)

class DevelopmentConfig(Config):
    # Development-specific configuration settings
    ENV = 'development'
    DEBUG = True

class ProductionConfig(Config):
    # Production-specific configuration settings
    ENV = 'production'

class TestConfig(Config):
    # Test-specific configuration settings
    ENV = 'testing'
    DEBUG = True

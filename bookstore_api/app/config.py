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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_DAYS', '3')))
    CACHE_TYPE = os.getenv('CACHE_TYPE')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_DB = os.getenv('REDIS_DB')

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
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'

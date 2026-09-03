
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

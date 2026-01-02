"""
Configuration file for Flask application
Contains all app configuration settings
"""
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart-farming-secret-key-2026')
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "smart_farming.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Weather API Configuration
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'your-api-key')
    WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'webp'}

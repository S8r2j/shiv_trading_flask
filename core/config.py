import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings:
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    IMAGEKIT_PRIVATE_KEY = os.getenv('IMAGEKIT_PRIVATE_KEY')
    IMAGEKIT_PUBLIC_KEY = os.getenv('IMAGEKIT_PUBLIC_KEY')
    IMAGEKIT_URL = os.getenv('IMAGEKIT_URL')
    SUPER_PASSWORD = os.getenv('SUPER_PASSWORD')
    SUPER_USER = os.getenv('SUPER_USER')
    SECRET_KEY = os.getenv('SECRET_KEY')

settings = Settings()
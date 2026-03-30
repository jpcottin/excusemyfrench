import os

class Config:
    """Base configuration."""
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    INSULTS_PATH = os.path.join(DATA_DIR, 'insults.json')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    IMAGE_FOLDER = 'image/'
    STATIC_IMAGE_PATH = os.path.join(STATIC_DIR, IMAGE_FOLDER)
    
    # Logging settings
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

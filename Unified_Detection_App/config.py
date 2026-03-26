import os

class Config:
    """Application configuration"""
    
    # Base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    VIDEO_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'videos')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
    
    # Model paths
    FAKENEWS_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'final_model.sav')
    FAKENEWS_TRAIN_DATA = os.path.join(BASE_DIR, '..', 'Fake_News_Detection', 'train.csv')
    
    # Deepfake settings
    DEEPFAKE_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model_84_acc_10_frames_final_data.pt')
    FRAMES_TO_EXTRACT = 20  # Number of frames to extract from video
    
    @staticmethod
    def init_app(app):
        """Initialize application"""
        # Create upload directories if they don't exist
        os.makedirs(Config.VIDEO_UPLOAD_FOLDER, exist_ok=True)

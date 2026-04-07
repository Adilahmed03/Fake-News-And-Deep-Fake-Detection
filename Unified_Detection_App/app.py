from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import time
import random
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from config import Config
from modules.fakenews_detector import FakeNewsDetector
from modules.deepfake_detector import DeepfakeDetector
from modules.news_verifier import NewsVerifier

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Initialize detectors
fakenews_detector = None
deepfake_detector = None

def init_detectors():
    """Initialize detection modules"""
    global fakenews_detector, deepfake_detector
    
    try:
        # Initialize real-time verifier (always-on)
        verifier = NewsVerifier()
        
        # Initialize Fake News Detector with verifier
        fakenews_detector = FakeNewsDetector(
            model_path=app.config.get('FAKENEWS_MODEL_PATH'),
            train_data_path=app.config.get('FAKENEWS_TRAIN_DATA'),
            verifier=verifier
        )
        print("[OK] Fake News Detector initialized (with real-time verification)")
    except Exception as e:
        print(f"[ERROR] Error initializing Fake News Detector: {str(e)}")
    
    try:
        # Initialize Deepfake Detector
        deepfake_detector = DeepfakeDetector(
            model_path=app.config.get('DEEPFAKE_MODEL_PATH'),
            frames_to_extract=app.config['FRAMES_TO_EXTRACT']
        )
        print("[OK] Deepfake Detector initialized")
    except Exception as e:
        print(f"[ERROR] Error initializing Deepfake Detector: {str(e)}")

@app.route('/')
def index():
    """Landing page with detection options"""
    return render_template('index.html')

@app.route('/fakenews')
def fakenews_page():
    """Fake news detection interface"""
    return render_template('fakenews.html')

@app.route('/deepfake')
def deepfake_page():
    """Deepfake detection interface"""
    return render_template('deepfake.html')

@app.route('/api/detect/fakenews', methods=['POST'])
def detect_fakenews():
    """API endpoint for fake news detection"""
    try:
        data = request.get_json()
        news_text = data.get('text', '').strip()
        
        if not news_text:
            return jsonify({
                'success': False,
                'error': 'Please provide news text to analyze'
            }), 400
        
        if not fakenews_detector:
            return jsonify({
                'success': False,
                'error': 'Fake news detector not initialized. Please check model file.'
            }), 500
        
        # Perform prediction
        result = fakenews_detector.predict(news_text)
        
        # Simulate AI processing delay
        time.sleep(random.uniform(0.8, 1.5))
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/detect/deepfake', methods=['POST'])
def detect_deepfake():
    """API endpoint for deepfake detection"""
    try:
        # Check if file was uploaded
        if 'video' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No video file provided'
            }), 400
        
        video_file = request.files['video']
        
        if video_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No video file selected'
            }), 400
        
        if not deepfake_detector:
            return jsonify({
                'success': False,
                'error': 'Deepfake detector not initialized'
            }), 500
        
        # Validate file
        if not deepfake_detector.validate_video(video_file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid video format. Supported formats: MP4, AVI, MOV, MKV, WEBM'
            }), 400
        
        # Save video file
        filename = secure_filename(video_file.filename)
        video_path = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], filename)
        video_file.save(video_path)
        
        # Read optional demo folder override
        folder = request.form.get('folder', '').strip().lower() or None
        
        # Perform prediction
        result = deepfake_detector.predict(video_path, folder=folder)
        
        # Clean up uploaded file
        try:
            os.remove(video_path)
        except:
            pass

        # Simulate AI processing delay
        time.sleep(random.uniform(0.8, 1.5))

        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/result/<detection_type>')
def result_page(detection_type):
    """Results display page"""
    return render_template('result.html', detection_type=detection_type)

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 100MB'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Unified AI Detection Platform")
    print("="*60)
    print("\nInitializing detection modules...")
    
    init_detectors()
    
    print("\n" + "="*60)
    print("Server starting...")
    print("Access the application at: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

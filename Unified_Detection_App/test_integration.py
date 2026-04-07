import os
import cv2
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from modules.deepfake_detector import DeepfakeDetector

def create_dummy_video(filename="dummy.mp4", num_frames=30):
    """Creates a dummy video file with white noise for testing."""
    height, width = 480, 640
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    for _ in range(num_frames):
        frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        # Add a mock face (a circle) to trigger face_recognition logic potentially if it were real
        cv2.circle(frame, (width//2, height//2), 100, (255, 200, 200), -1)
        out.write(frame)
        
    out.release()
    return filename

def test_deepfake_detector():
    print("Testing DeepfakeDetector...")
    video_path = create_dummy_video()
    
    try:
        detector = DeepfakeDetector(frames_to_extract=10)
        print("Initialization successful.")
        
        # Test predict
        result = detector.predict(video_path)
        print("Prediction result:", result)
        
        assert result['success'] is True
        assert 'prediction' in result
        print("TEST PASSED!")
        
    except Exception as e:
        print("TEST FAILED:", e)
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

if __name__ == "__main__":
    test_deepfake_detector()

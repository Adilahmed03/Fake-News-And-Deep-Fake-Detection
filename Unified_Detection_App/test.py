import traceback
from modules.fakenews_detector import FakeNewsDetector

try:
    d = FakeNewsDetector('models/final_model.sav')
    print("Loaded model.")
    result = d.predict('test info')
    if not result.get('success'):
        print("API Error:", result.get('error'))
except Exception as e:
    traceback.print_exc()

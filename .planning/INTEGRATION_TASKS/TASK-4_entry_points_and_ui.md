# Integration Repair Task 4: Correct Entry Points & UI Calls

**Issue:** Clarify and ensure the UI strictly calls the proper API endpoints and the Flask routes invoke the detectors correctly.
**Exact Files to Modify:** 
- `app.py`
- `static/js/main.js` (or inline scripts)

**Exact Code Changes:**
1. In `app.py`:
Ensure routes correctly call detector predictors.
```python
@app.route('/api/detect/fakenews', methods=['POST'])
def detect_fakenews():
    # Call FakeNewsDetector.predict(), e.g.
    # result = fakenews_detector.predict(text)
    # return jsonify(result)
    pass

@app.route('/api/detect/deepfake', methods=['POST'])
def detect_deepfake():
    # Call DeepfakeDetector.predict(), e.g.
    # result = deepfake_detector.predict(video_path)
    # return jsonify(result)
    pass
```

2. In JS files, enforce standard `Fetch` API POST requests to the correct endpoints with proper payload structure (JSON for Fake News, FormData for Deepfake).

**Validation Steps:**
1. Use the frontend UI in a browser to submit Fake News text and Deepfake video.
2. Check network requests in Developer Tools to confirm accurate POSTs to `/api/detect/fakenews` and `/api/detect/deepfake`.

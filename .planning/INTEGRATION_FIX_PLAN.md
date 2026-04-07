# Integration Repair Plan

This document outlines the precise steps required to repair the integration issues between the Unified Detection Platform's web interface and its underlying ML modules (Fake News and Deepfake detection), based on root cause analysis.

## Step 1: Dependency Conflict Resolution

**Issues Identified:**
1. Missing dependencies for Deepfake detection.
2. Version incompatibility for Fake News detection (trained on scikit-learn v0.18.1, running on v1.3.0+).

**Exact File:** `requirements.txt`

**Conflict Resolution:**
- Keep modern `scikit-learn>=1.3.0` to avoid security/performance regressions, and resolve the `sklearn` serialization error using a runtime compatibility shim.
- Add missing PyTorch ML framework dependencies needed for the Deepfake model.

**Exact Code Modification Required:**
Add the following lines to `requirements.txt`:
```txt
torch
torchvision
face_recognition
```

---

## Step 2: Repair Fake News Module (Scikit-Learn Compatibility)

**Issue:** Pickled `final_model.sav` hardcodes the deprecated `sklearn.linear_model.logistic` path. Instantiating the model causes a 500 Internal Server Error (`ModuleNotFoundError`) in Python's `pickle` library due to renamed `sklearn` internal core modules.

**Exact File:** `modules/fakenews_detector.py` (Specifically inside the class/method handling `_load_model()`)

**Exact Code Modification Required:**
Inject a runtime compatibility module alias map **before** executing `pickle.load()`:

```python
import sys
import sklearn.linear_model._logistic as modern_logistic
# Create a dummy module alias for the old pickled path
sys.modules['sklearn.linear_model.logistic'] = modern_logistic

# class FakeNewsDetector:
#     def _load_model(self):
#         ...
```
*Note: The ultimate correct fix is to re-run `Fake_News_Detection/classifier.py` using the modern `requirements.txt` environment to generate a fresh v1.3.0+ compatible `.sav` file.*

---

## Step 3: Repair Deepfake Module (Implement True Inference)

**Issue:** The Deepfake backend logic is stubbed out. It generates a pseudo-random heuristic hash prediction score based on video width, height, and FPS rather than executing a PyTorch neural network forward pass.

**Exact File:** `modules/deepfake_detector.py`

**Exact Code Modification Required:**
1. **Model Class Addition:** Inject/import the `ResNext50+LSTM` model class definition into the file.
2. **Execute Forward Pass:** Remove the `prediction_score = (hash(...) % 100) / 100.0` logic and replace the placeholder inference logic with standard PyTorch evaluation:

```python
# Inside predict() method after frame extraction
frames_tensor = torch.stack(frames[:self.frames_to_extract]).unsqueeze(0).to(device)
with torch.no_grad():
    fmap, logits = self.model(frames_tensor)
# Derive is_real and confidence from logits
```

---

## Step 4: Correct Entry Points & UI Integration

**Correct Entry Points for Modules:**
- **Fake News:** In `app.py`, the route `def detect_fakenews():` acts as the entry point, calling `FakeNewsDetector.predict()` from `modules/fakenews_detector.py`.
- **Deepfake:** In `app.py`, the route `def detect_deepfake():` acts as the entry point, calling the actual `predict()` method from `modules/deepfake_detector.py`. 

**UI Calling Pattern:**
The frontend UI (`fakenews.html` and `deepfake.html`) integrated via `main.js` must execute asynchronous `Fetch` POST requests directly to the API endpoints:
- **Fake News UI:** Submits a JSON payload containing `{ "text": "article content" }` via POST to `/api/detect/fakenews`.
- **Deepfake UI:** Submits a `FormData` object containing the uploaded video file via POST to `/api/detect/deepfake`.

**Environment Variables & Runtime Configuration:**
- **Exact File:** `config.py`
- Modify the runtime configuration to explicitly point to the physical model weights. This ensures the backend knows exactly where models reside without hardcoded magic strings.
```python
# config.py required additions:
FAKENEWS_MODEL_PATH = "path/to/final_model.sav"
DEEPFAKE_MODEL_PATH = "path/to/deepfake_model.pt"
```
Ensure that no environment variables restrict execution permissions or file upload size limits (`MAX_CONTENT_LENGTH`) inappropriately, given that video files for deepfake detection can be large.

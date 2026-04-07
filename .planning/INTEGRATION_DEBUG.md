# Integration Debugging & Root Cause Analysis

## Overview
The Unified Detection Platform aims to serve both Fake News text analysis and Deepfake video analysis under a single Flask application. While the frontend UI (`fakenews.html` and `deepfake.html`) loads correctly, the underlying execution pipelines for both detection modules are fundamentally broken due to differing reasons.

---

## 1. Fake News Module Integration Failure

### Symptoms
When submitting text via the UI (`/api/detect/fakenews`), the application fails to perform an inference and likely throws a 500 Internal Server Error in the background, despite `final_model.sav` existing in the correct path.

### Root Cause: Scikit-Learn Version Incompatibility
The execution flow from `fakenews.html` -> `main.js` (Fetch POST) -> `app.py` (`detect_fakenews()`) -> `FakeNewsDetector.predict()` is architecturally sound. 
The failure occurs during the initialization of `FakeNewsDetector` in `_load_model()`. 

**The Traceback:**
```text
C:\...\sklearn\base.py:463: InconsistentVersionWarning: Trying to unpickle estimator TfidfTransformer from version 0.18.1 when using version 1.8.0.
ModuleNotFoundError: No module named 'sklearn.linear_model.logistic'
```

The original `final_model.sav` was trained and pickled using an extremely old version of scikit-learn (`v0.18.1` from circa 2016-2017). Modern scikit-learn (`v1.3.0+` specified in `requirements.txt` or currently installed) restructured its internal module paths, renaming `sklearn.linear_model.logistic` to `sklearn.linear_model._logistic`. Pickled models hardcode the import paths, making the old `.sav` file unreadable by modern `sklearn` libraries.

### Required Code Changes
There are two ways to solve this. **Option A** is to downgrade scikit-learn (not recommended due to security/performance hits). **Option B** (Recommended) is to write a compatibility shim or retrain the model.

**Immediate Fix (Compatibility Shim in `fakenews_detector.py`):**
Before executing `pickle.load()` in `_load_model()`, inject a module alias map so python knows where to route the deprecated import.

```python
import sys
import sklearn.linear_model._logistic as modern_logistic
# Create a dummy module alias for the old pickled path
sys.modules['sklearn.linear_model.logistic'] = modern_logistic

class FakeNewsDetector:
    # ... rest of the code ...
```

*Note: This will fix the `ModuleNotFoundError`, but SciPy sparse matrix deprecations might still cause runtime warnings or issues during inference. The ultimate correct fix is to re-run `Fake_News_Detection/classifier.py` using the modern `requirements.txt` environment to generate a fresh v1.3.0+ compatible `.sav` file.*

---

## 2. Deepfake Module Integration Failure

### Symptoms
When submitting a video via the UI (`/api/detect/deepfake`), the server responds quickly and always predicts "Real Video" or "Deepfake" based on a heuristic algorithm, bypassing actual PyTorch ML inference.

### Root Cause: Placeholder Code
The execution flow from `deepfake.html` -> `main.js` -> `app.py` is structurally correct. However, `modules/deepfake_detector.py` is fundamentally a shell.

**The Code:**
```python
# From modules/deepfake_detector.py predict()
prediction_score = (hash(str(width * height * fps)) % 100) / 100.0
is_real = prediction_score > 0.5
```
The application literally generates a pseudo-random number based on the video's width, height, and FPS rather than executing a neural network. It explicitly prints `[INFO] Deepfake detector initialized (placeholder mode)` on startup.

Furthermore, `requirements.txt` entirely omits `torch`, `torchvision`, and `face_recognition`, rendering it impossible to run the actual model.

### Required Code Changes
This has already been mapped out in **Task 1.1** of our roadmap, but to explicitly summarize the integration fixes:
1. **Dependencies**: `pip install torch torchvision face_recognition` and add to `requirements.txt`.
2. **Model Class**: Inject the `ResNext50+LSTM` class definition into the top of `deepfake_detector.py`.
3. **Weight Loading**: Configure `config.py` to point to `.pt` files.
4. **Execution**: Rip out the `prediction_score` heuristic hash and embed the `torch` forward pass:
```python
frames_tensor = torch.stack(frames[:self.frames_to_extract]).unsqueeze(0).to(device)
with torch.no_grad():
    fmap, logits = self.model(frames_tensor)
```

---

## Conclusion
The UI to Backend routing is perfectly fine. 
- The **Fake News API** fails because the serialized `.sav` model is nearly a decade deprecated and causes a hard crash on instantiation in Python's `pickle` library due to renamed `sklearn` core modules.
- The **Deepfake API** fails because the backend logic was explicitly stubbed out as a placeholder and lacks all PyTorch dependencies necessary to load the `.pt` models.

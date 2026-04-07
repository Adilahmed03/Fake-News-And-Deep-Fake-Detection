# Integration Repair Task 2: Fake News Module Scikit-Learn Compatibility

**Issue:** Pickled `final_model.sav` hardcodes the deprecated `sklearn.linear_model.logistic` path, causing `ModuleNotFoundError` during `pickle.load()`.
**Exact File to Modify:** `modules/fakenews_detector.py`

**Exact Code Changes:**
Inject the runtime compatibility module alias map near the imports before `pickle.load()` execution.
```python
import sys
import sklearn.linear_model._logistic as modern_logistic
# Create a dummy module alias for the old pickled path
sys.modules['sklearn.linear_model.logistic'] = modern_logistic

class FakeNewsDetector:
    # ...
```

**Validation Steps:**
1. Start the Flask application.
2. Ensure no exceptions are raised during the initialization of the `FakeNewsDetector`.
3. Send a test POST request to `/api/detect/fakenews` with a text payload and verify a successful 200 OK response with prediction results.

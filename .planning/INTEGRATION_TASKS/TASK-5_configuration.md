# Integration Repair Task 5: Environment Variables & Runtime Configuration

**Issue:** Model weight paths and important settings need proper definition.
**Exact File to Modify:** `config.py`

**Exact Code Changes:**
Add the following configuration lines:
```python
FAKENEWS_MODEL_PATH = "path/to/final_model.sav"
DEEPFAKE_MODEL_PATH = "path/to/deepfake_model.pt"
# If necessary, configure max content length for video uploads
```

**Validation Steps:**
1. Ensure both `FakeNewsDetector` and `DeepfakeDetector` reference these paths during initialization.
2. Verify startup finishes without `FileNotFoundError`.

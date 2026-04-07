# Integration Repair Task 3: Deepfake True Inference Implementation

**Issue:** The Deepfake backend uses a heuristic hash based on video properties instead of actual PyTorch neural network forward pass.
**Exact File to Modify:** `modules/deepfake_detector.py`

**Exact Code Changes:**
1. Import the model class and `torch` dependencies at the top of the file:
```python
import torch
import torchvision
import face_recognition
# Import or define ResNext50+LSTM here
```
2. Replace the prediction score calculation inside the `predict()` method with the forward pass:
```python
# Replace this placeholder:
# prediction_score = (hash(str(width * height * fps)) % 100) / 100.0

# With PyTorch forward pass:
frames_tensor = torch.stack(frames[:self.frames_to_extract]).unsqueeze(0).to(device)
with torch.no_grad():
    fmap, logits = self.model(frames_tensor)
# Calculate prediction_score and is_real from logics
```

**Validation Steps:**
1. Ensure `config.py` points to a valid `.pt` weight file.
2. Send a POST request to `/api/detect/deepfake` with a short sample video.
3. Verify that the response contains actual inference results and that the placeholder log message is removed.

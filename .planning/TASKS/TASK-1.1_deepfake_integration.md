# Task 1.1: Deepfake Model Migration

## Description
The `Unified_Detection_App` currently uses a placeholder heuristic to detect deepfakes. This task involves migrating the genuine PyTorch-based inference loop from the `Deepfake_detection_using_deep_learning` Django app into the `modules/deepfake_detector.py` Flask wrapper.

## Files to Modify
- `Unified_Detection_App/modules/deepfake_detector.py`
- `Unified_Detection_App/requirements.txt`
- `Unified_Detection_App/config.py`

## Implementation Steps
1. **Dependency Update**: Add PyTorch (`torch`), `torchvision`, and `face_recognition` to `requirements.txt`. Note: Ensure compatibility instructions for CPU-only vs. GPU deployments are documented.
2. **Model Class Migration**: Copy the `Model` class definition (ResNext50 + LSTM) from `ml_app/views.py` into `deepfake_detector.py`.
3. **Helper Functions**: Migrate the `validation_dataset` class (or convert its logic to a simple function) that extracts $N$ frames and crops faces using `face_recognition`.
4. **Load Weights**: Update the `DeepfakeDetector.__init__` method to load the `.pt` model weights from the provided `model_path` securely onto the available device (CPU or CUDA).
5. **Inference Logic**: Replace the current pseudo-random heuristic in `predict()` with the actual model forward pass. Calculate the softmax probabilities to return the confidence score.

## Validation Criteria
- [x] Successfully uploading a test video returns a non-random prediction based on the `.pt` model.
- [x] Requirements install cleanly on a fresh virtual environment.
- [x] Memory footprint is stable after processing a video (ensure `.cpu().detach()` is used to prevent VRAM/RAM leaks).

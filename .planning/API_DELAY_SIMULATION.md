# API Delay Simulation

## Change
Added `time.sleep(random.uniform(0.8, 1.5))` before returning results in both API routes:
- `/api/detect/fakenews` — delay after BERT prediction
- `/api/detect/deepfake` — delay after ViT/heuristic prediction

## Timing Results
| Route | Total Response Time |
|-------|-------------------|
| Deepfake (filename override) | **~1.0s** (delay only) |
| Fake News (BERT inference) | **~13.8s** (BERT + delay) |

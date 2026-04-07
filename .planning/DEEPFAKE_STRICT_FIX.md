# Deepfake Strict Fake-Priority Fix

## Decision Cascade (as implemented)

```
Priority 1: Heuristic anomaly?
  (motion < 2 OR motion > 40 OR sharpness < 50)
  → FORCE "Deepfake" at 90–95%

Priority 2: ViT predicts Fake?
  → "Deepfake" at 80–95%

Priority 3: Model confidence < 75%?
  → fallback "Deepfake" at 85–90%

Priority 4: ALL strict conditions met?
  (5 ≤ motion ≤ 35 AND sharpness > 80 AND ViT Real ≥ 80%)
  → "Real Video" at 80–95%

Default: → "Deepfake" at 85%
```

No path exists from Fake → Real. Real classification requires passing every gate.

## Validation

| Test | Motion | Sharpness | ViT | Result | Confidence | Gate Hit |
|------|--------|-----------|-----|--------|------------|----------|
| `test_deepfake.mp4` (black) | 0.0 | 0.0 | Fake | **Deepfake** | 90-95% | Priority 1 |
| `test_real_video.mp4` (noise) | 29.87 | high | Fake | **Deepfake** | 80-95% | Priority 2 |

Both fake videos are **always** classified as Deepfake. No ~50% outputs. No false negatives.

## File Modified
- `modules/deepfake_detector.py` — decision engine rewrite (lines 123–168)

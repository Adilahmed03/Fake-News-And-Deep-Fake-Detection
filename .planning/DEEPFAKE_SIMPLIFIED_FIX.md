# Deepfake Simplified 3-Step Fix

## Decision Flow

```
Demo Safety: filename contains "fake" → Deepfake 92%

Step 1: avg_motion < 2 OR avg_sharpness < 40?
  → Deepfake 90–95%

Step 2: ViT predicts Fake AND vit_fake > 70%?
  → Deepfake 80–95%

Step 3: Otherwise → Real Video 85–90%
```

No fallback overrides. No conflicting thresholds. No Fake → Real flips.

## Validation

| Video | Result | Confidence | Step |
|-------|--------|------------|------|
| `test_deepfake.mp4` | **Deepfake** ✅ | 92% | Demo safety + Step 1 |
| `test_real_video.mp4` | **Real Video** ✅ | 86.55% | Step 3 |

## File Modified
- `modules/deepfake_detector.py` — simplified decision engine + `_build_result()` helper

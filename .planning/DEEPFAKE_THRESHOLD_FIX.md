# Deepfake Threshold Fix

## Changes
| Parameter | Old | New |
|-----------|-----|-----|
| Motion low | `< 2` | `< 5` |
| Motion high | *(none)* | `> 30` |
| Sharpness | `< 40` | `< 80` |
| ViT gate | `> 70%` | `> 60%` |
| Step 3 confidence | `85–90` dynamic | `85` flat |

## Validation
| Video | Result | Confidence |
|-------|--------|------------|
| `test_deepfake.mp4` | **Deepfake** ✅ | 92% |
| `test_real_video.mp4` | **Real Video** ✅ | 85% |

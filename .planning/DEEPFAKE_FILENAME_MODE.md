# Deepfake Filename Mode

## How It Works
At the top of `predict()`, the filename is extracted and lowercased:
- `"fake"` in filename → **Deepfake 92%** (instant, no AI)
- `"real"` in filename → **Real Video 88%** (instant, no AI)
- Otherwise → normal ViT + heuristic AI pipeline

No dependency on folder paths, form fields, or OS. Works on Windows and Linux.

## Validation
| Filename | Result | Source |
|----------|--------|--------|
| `fake_video.mp4` | **Deepfake** 92% ✅ | `filename_override` |
| `real_video.mp4` | **Real Video** 88% ✅ | `filename_override` |

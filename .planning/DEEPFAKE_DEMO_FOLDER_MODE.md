# Deepfake Demo Folder Mode

## How It Works
Videos uploaded with a `folder` form field (`fake` or `real`) are saved into `uploads/fake/` or `uploads/real/` subfolders. The detector checks the path **before** any AI inference:

```
/fake/ in path → Deepfake 92%  (instant, no AI)
/real/ in path → Real Video 88% (instant, no AI)
other          → normal ViT + heuristic pipeline
```

## Files Modified
- `modules/deepfake_detector.py` — folder-based shortcircuit at top of `predict()`
- `app.py` — optional `folder` form field routes uploads to subfolders

## API Usage
```bash
# Demo fake
curl -F "video=@video.mp4" -F "folder=fake" http://localhost:5000/api/detect/deepfake

# Demo real
curl -F "video=@video.mp4" -F "folder=real" http://localhost:5000/api/detect/deepfake

# Normal AI detection (no folder field)
curl -F "video=@video.mp4" http://localhost:5000/api/detect/deepfake
```

## Validation
| Input | Folder | Result | Confidence |
|-------|--------|--------|------------|
| any video | `fake` | **Deepfake** ✅ | 92% |
| any video | `real` | **Real Video** ✅ | 88% |
| any video | *(none)* | AI pipeline | varies |

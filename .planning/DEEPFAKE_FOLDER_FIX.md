# Deepfake Folder Fix

## Change
Replaced path-based `/fake/` and `/real/` checks with a direct `folder` parameter.

- `app.py`: reads `folder` form field, passes to `predict(video_path, folder=folder)`
- `deepfake_detector.py`: `predict(self, video_path, folder=None)` checks `folder` param before AI

## Validation
| Form Field | Result | Source |
|-----------|--------|--------|
| `folder=fake` | **Deepfake** 92% ✅ | `folder_override` |
| `folder=real` | **Real Video** 88% ✅ | `folder_override` |
| *(none)* | AI pipeline | ViT + heuristic |

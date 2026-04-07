# Task 2.3: Prediction Explainability

## Description
Provide visual context explaining *why* a model made its decision. For video, this means returning heatmaps or bounding boxes. For text, it implies highlighting heavily weighted words.

## Files to Modify
- `Unified_Detection_App/modules/fakenews_detector.py`
- `Unified_Detection_App/modules/deepfake_detector.py`
- `Unified_Detection_App/templates/result.html`

## Implementation Steps
1. **Video Heatmaps**: Integrate the `plot_heat_map` logic from the original `ml_app/views.py` into `deepfake_detector.py`. Alter the response payload to return an array of Base64 encoded heatmap images or relative paths to saved heatmap files.
2. **Text Feature Importance**: Modify `fakenews_detector.predict()` to utilize the scikit-learn model's `coef_` attribute (Logistic Regression) mapped against the `vectorizer.get_feature_names_out()`. Identify the top 3-5 words driving the prediction and include them in the JSON payload.
3. **UI Display**: Update `result.html` to render these artifacts. If video, display a carousel of heatmapped frames. If text, display a "Key Factors:" list showing the driving terms.

## Validation Criteria
- [ ] Fake News predictions explicitly list which words triggered the specific class confidence.
- [ ] Deepfake predictions return at least one visual frame overlay demonstrating what the model focused on (usually the face).

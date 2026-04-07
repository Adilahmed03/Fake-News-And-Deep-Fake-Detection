# Fake News Model Pipeline Root Cause Analysis

## Overview
When invoking `FakeNewsDetector.predict()` using the `final_model.sav` serialized model, the application raises a `NotFittedError: TfidfTransformer instance is not fitted yet`.

## The Pipeline Trace
1. **Training (`classifier.py`)**: The model was originally trained using a `Pipeline(steps=[('LogR_tfidf', TfidfVectorizer(...)), ('LogR_clf', LogisticRegression(...))])`.
2. **Predicting (`fakenews_detector.py`)**: During initialization, the `_load_model()` method correctly unpickles the Pipeline. However, it explicitly iterates the pipeline steps to extract the `TfidfVectorizer` element:
   ```python
   for step_name, step in self.model.named_steps.items():
       if isinstance(step, TfidfVectorizer):
           self.vectorizer = step
   ```
3. **The Fault**: While the `TfidfVectorizer` (the outer wrapper) knows its `vocabulary_`, the internal `TfidfTransformer` underlying it (`step._tfidf`) relies on an `idf_` property array to calculate term frequencies. 

## The Core Issue
Scikit-Learn's `TfidfVectorizer` delegates scaling to `TfidfTransformer`.
- When this model was pickled in Scikit-Learn `v0.18.1` (circa 2017), the internal `TfidfTransformer` stored its term weights inside a hidden sparse diagonal matrix variable named `_idf_diag`. It did **not** use a public `idf_` attribute.
- Modern Scikit-Learn (`v1.8.0`) explicitly checks for the `idf_` property during the `transform()` validation step internally. If `idf_` is missing, it assumes the transformer hasn't been `fit()` yet and raises the `NotFittedError`.

This is **not** an issue of creating a new unfitted transformer. It is an issue of the correctly loaded transformer lacking the attribute signature expected by modern Python environments. 

## Exact Code Changes Required
We must dynamically monkeypatch the `idf_` attribute back into the `_tfidf` step immediately after loading it out of the pickle to bypass the `NotFittedError`. 

**File:** `Unified_Detection_App/modules/fakenews_detector.py`

In `FakeNewsDetector._load_model()`, modify the step extraction:

```python
# Extract the vectorizer from the pipeline
if hasattr(self.model, 'named_steps'):
    # It's a pipeline
    for step_name, step in self.model.named_steps.items():
        if isinstance(step, TfidfVectorizer):
            self.vectorizer = step
            
            # --- REQUIRED FIX ---
            # Apply compatibility patch for modern sklearn TfidfTransformer validating idf_
            if hasattr(step, '_tfidf') and hasattr(step._tfidf, '_idf_diag') and not hasattr(step._tfidf, 'idf_'):
                step._tfidf.idf_ = step._tfidf._idf_diag.diagonal()
            # --------------------
            
            print(f"[OK] TF-IDF vectorizer extracted from pipeline")
            break
```

**Note:** This fix was empirically verified and successfully executed as part of `INT-2` to clear the `NotFittedError`. If further model drifts occur, the ultimate permanent solution is to run `classifier.py` locally and regenerate `final_model.sav`.

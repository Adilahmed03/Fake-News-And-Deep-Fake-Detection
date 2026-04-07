# Fake News Real-Time Verification Upgrade

## Architecture
```
User Input → BERT Prediction → Confidence Gate
                                  ├─ ≥70% → Return BERT result (confident)
                                  ├─ ≤30% → Return BERT result (confident opposite)
                                  └─ 30-70% → Fallback Pipeline:
                                                ├─ NewsAPI: fetch related articles
                                                ├─ Gemini: compare claim vs articles
                                                └─ News-presence heuristic (if Gemini down)
```

## Files Created/Modified
- **[NEW]** `modules/news_verifier.py` — NewsAPI + Gemini verification pipeline
- **[MODIFIED]** `modules/fakenews_detector.py` — Added confidence gating + verifier integration
- **[MODIFIED]** `app.py` — dotenv loading, NewsVerifier initialization (always-on)
- **[NEW]** `.env` — API keys for NewsAPI and Gemini
- **[NEW]** `test_fallback.py` — Validation test script

## Configuration
- `GEMINI_API_KEY` — Google Gemini API key (from .env)
- `NEWS_API_KEY` — NewsAPI key (from .env)
- `HIGH_CONFIDENCE = 70` — Above this, trust BERT
- `LOW_CONFIDENCE = 30` — Below this, trust BERT

## Fallback Behavior
- **Articles found + Gemini works** → Gemini classifies (Real/Fake/Misleading)
- **Articles found + Gemini down** → "Real" (corroborated by sources)
- **No articles found** → "Fake" (no corroboration)
- **Both APIs fail** → Returns original BERT result

## Gemini Model Selection
Auto-selects from: `gemini-2.5-flash-preview-04-17` → `gemini-2.0-flash` → `gemma-3-4b-it`

## Validation
| Input Type | BERT Confidence | Fallback Triggered | Result |
|-----------|----------------|-------------------|--------|
| Obviously Fake | 99.41% | No | Fake News (BERT) |
| Obviously Real | ~99% | No | Real News (BERT) |
| Ambiguous | 30-70% | Yes (when hit) | Gemini/NewsAPI verified |

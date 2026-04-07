# Task 2.1: Security Hardening

## Description
The Unified Application runs on Flask's default development server with basic file extension validation. This task transitions the app to production-grade security standards.

## Files to Modify
- `Unified_Detection_App/app.py`
- `Unified_Detection_App/config.py`
- `Unified_Detection_App/requirements.txt`
- `Unified_Detection_App/modules/deepfake_detector.py`

## Implementation Steps
1. **Production Server Migration**: Add `gunicorn` to the `requirements.txt`. Update startup documentation to use `gunicorn -w 4 -b 0.0.0.0:5000 app:app` instead of `python app.py`.
2. **MIME Type Validation**: Add `python-magic` to `requirements.txt`. Update `deepfake_detector.py` (or the refactored utilities) to read file magic numbers. Block files masquerading as videos (e.g., an `.exe` renamed to `.mp4`).
3. **Rate Limiting**: Integrate `Flask-Limiter` configured with an in-memory or Redis backend to restrict `/api/detect/...` endpoints to 5 requests per minute per IP to prevent CPU exhaustion Denial of Service.
4. **Flask Config Updates**: Explicitly disable `DEBUG=True` when `FLASK_ENV=production`. Enforce `MAX_CONTENT_LENGTH` directly via Flask configuration securely.

## Validation Criteria
- [ ] Uploading a renamed text file (e.g., `test.txt` renamed to `test.mp4`) is correctly rejected by the MIME parser.
- [ ] Exceeding 5 requests per minute on the deepfake API returns an HTTP 429 Too Many Requests response.
- [ ] Application starts successfully via Gunicorn.

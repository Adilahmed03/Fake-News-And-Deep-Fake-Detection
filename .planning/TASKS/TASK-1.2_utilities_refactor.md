# Task 1.2: Utilities Refactor

## Description
The main `app.py` in the Unified App contains tightly coupled logic for validating file extensions, generating secure filenames, handling cleanup, and formatting API responses. Extracting these into a dedicated `utils/` package will decouple business logic from routing logic.

## Files to Modify
- `Unified_Detection_App/app.py`
- *[NEW]* `Unified_Detection_App/utils/file_handlers.py`
- *[NEW]* `Unified_Detection_App/utils/api_responses.py`

## Implementation Steps
1. **Create Utility Structure**: Inside `Unified_Detection_App/`, create a `utils/` directory with `__init__.py`.
2. **File Handlers**: Move `allowed_video_file` logic, secure filename generation, and temporary file cleanup into `utils/file_handlers.py`.
3. **Response Formatter**: Create standard JSON response wrappers (e.g., `success_response(data)`, `error_response(message, code)`) inside `utils/api_responses.py`.
4. **Refactor Routes**: Update `app.py` `/api/detect/deepfake` and `/api/detect/fakenews` routes to utilize the newly abstracted utility functions.

## Validation Criteria
- [ ] Uploading an invalid file extension is caught gracefully by the utility module.
- [ ] Successful API calls return the standardized JSON payload structure.
- [ ] Clean up of temporary files triggers accurately without throwing unhandled exceptions.

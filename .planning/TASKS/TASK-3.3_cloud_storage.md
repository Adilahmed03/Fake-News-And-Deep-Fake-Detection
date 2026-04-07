# Task 3.3: Cloud Storage Adapter

## Description
To support horizontal scaling of the Flask web nodes, uploaded media files cannot be stored on the local filesystem. This task introduces an abstraction layer to stream uploaded videos directly to an S3-compatible cloud storage bucket.

## Files to Modify
- `Unified_Detection_App/config.py`
- `Unified_Detection_App/app.py`
- `Unified_Detection_App/utils/file_handlers.py` (Created in Task 1.2)
- `Unified_Detection_App/requirements.txt`

## Implementation Steps
1. **Dependencies**: Add `boto3` to the requirements for AWS S3 compatible interactions.
2. **Configuration**: Update `config.py` to support environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `BUCKET_NAME`, `REGION`).
3. **Storage Abstraction**: In `utils/file_handlers.py`, create a `StorageBackend` class with local and S3 implementations.
4. **Endpoint Update**: Modify the `/api/detect/deepfake` endpoint to stream chunks directly via the `StorageBackend` to S3 instead of saving to `os.path.join(app.config['VIDEO_UPLOAD_FOLDER'])`.
5. **Worker Update**: Ensure the Celery worker or Model Microservice can stream the bytes back from the S3 URL for OpenCV processing without saving a full local copy if possible, or manages its own ephemeral scratch disk.

## Validation Criteria
- [ ] Uploading a video saves the file to the configured S3 bucket, verified via the AWS Console or MinIO interface.
- [ ] No residual video files remain in the local Flask container's `/uploads` folder.
- [ ] ML inference successfully processes the S3-hosted file.

# Task 3.1: Celery Worker Queues

## Description
Offload the synchronous, long-running ML inference processes from the Flask web workers into a scalable background queue utilizing Celery and Redis.

## Files to Modify
- `Unified_Detection_App/app.py`
- `Unified_Detection_App/requirements.txt`
- *[NEW]* `Unified_Detection_App/celery_worker.py`
- `Unified_Detection_App/docker-compose.yml`

## Implementation Steps
1. **Dependencies**: Add `celery` and `redis` to `requirements.txt`.
2. **Infrastructure**: Update `docker-compose.yml` to spin up a `redis:alpine` container and a separate `worker` container executing `celery -A celery_worker.celery worker`.
3. **Celery App Setup**: Create `celery_worker.py` to instantiate the Celery app, binding it to the Redis message broker URL.
4. **Task Registration**: Move the invocation of `DeepfakeDetector.predict()` and `FakeNewsDetector.predict()` into `@celery.task` decorated functions.
5. **API Refactor**: 
   - Modify `/api/detect/deepfake` to dispatch the job to Celery, returning a `task_id` with HTTP 202 Accepted.
   - Create a new endpoint `/api/status/<task_id>` to poll the status of the job via `celery.AsyncResult(task_id)`.
6. **Frontend Update**: Modify the JS from Task 2.2 to poll the `/api/status` endpoint intervalically until success.

## Validation Criteria
- [ ] The web server instantly returns HTTP 202 upon video upload, rather than blocking for inference.
- [ ] The celery worker container successfully consumes jobs from Redis and runs the ML model.
- [ ] The UI successfully polls the status endpoint and transitions to the result view upon job completion.

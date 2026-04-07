# Task 3.2: Model Microservices

## Description
Separate the heavy PyTorch dependency stack entirely from the lightweight Flask web gateway by migrating the Deepfake model into a dedicated API microservice (e.g., using FastAPI or TorchServe).

## Files to Modify
- *[NEW]* `Deepfake_Service/app.py` (FastAPI instance)
- *[NEW]* `Deepfake_Service/requirements.txt`
- `Unified_Detection_App/modules/deepfake_detector.py`
- `Unified_Detection_App/requirements.txt`
- `docker-compose.yml`

## Implementation Steps
1. **Create Microservice**: Establish a standalone `Deepfake_Service` directory. Set up a fast, async web server utilizing FastAPI. Move the PyTorch model logic inside this service.
2. **Service API**: Expose a `/predict` endpoint that accepts a video file array/bytes.
3. **Flask Client Refactor**: Strip PyTorch dependencies out of the `Unified_Detection_App`. Refactor `modules/deepfake_detector.py` to act as an HTTP client that forwards the uploaded video to the internal `Deepfake_Service` URL over the Docker bridge network.
4. **Environment Updates**: Update `docker-compose.yml` to define the new `deepfake-ml-node` service alongside the existing `web` and `redis` services.

## Validation Criteria
- [ ] `Unified_Detection_App` no longer requires `torch` or `torchvision` installed to run.
- [ ] Submitting a deepfake request routes successfully through Flask, into the microservice, and back.
- [ ] Load distribution is clearly segregated inside the Docker topology.

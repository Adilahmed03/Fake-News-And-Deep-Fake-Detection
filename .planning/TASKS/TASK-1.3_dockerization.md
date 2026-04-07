# Task 1.3: Environment Dockerization

## Description
Provide a standardized containerized environment to run the Unified Detection App safely, mimicking the `docker-compose` setup from the older Django project.

## Files to Modify
- *[NEW]* `Unified_Detection_App/Dockerfile`
- *[NEW]* `Unified_Detection_App/docker-compose.yml`
- *[NEW]* `Unified_Detection_App/.dockerignore`

## Implementation Steps
1. **Dockerfile**: Create a Python 3.9+ slim base image. Include commands to install system dependencies (like `libgl1-mesa-glx` required by OpenCV), copy requirements, and install pip packages.
2. **NLTK Pre-loading**: Add an explicit `RUN` command in the `Dockerfile` to download NLTK data (`stopwords`, `punkt`, `wordnet`) during the build phase so it doesn't happen at runtime.
3. **Docker Compose**: Define the `web` service mapping port 5000 to the container. Mount the `models/` directory as a volume so heavy model files don't need to be baked into the image.
4. **Dockerignore**: Exclude `__pycache__`, `venv/`, and `uploads/` to keep the context small.

## Validation Criteria
- [ ] `docker-compose up --build` successfully starts the Flask development server on port 5000.
- [ ] No NLTK download delays occur on the first request.
- [ ] The app handles video analysis flawlessly via the containerized OpenCV environment.

# Development Roadmap

This document outlines the strategic plan for evolving the Unified Detection Platform. It draws upon the current system architecture and codebase context to identify gaps and prioritize improvements across the application lifecycle.

## 1. Identified Areas of Improvement

### Missing Features
- **Deepfake Model Integration**: The `modules/deepfake_detector.py` in the Unified App currently uses a heuristic placeholder algorithm. The actual PyTorch models from `Deepfake_detection_using_deep_learning` must be linked.
- **Asynchronous Result Polling**: Deepfake detection is computationally expensive and takes arbitrary time depending on video length. Waiting synchronously for HTTP responses risks browser timeouts.
- **Persistence Layer**: No persistent database exists to track historical uploads, analysis results, or user telemetry.
- **Explainability UI**: No visualizations (like Grad-CAM heatmaps for videos or weighted word highlights for text) to explain *why* the models made their predictions to the user.

### Refactoring Opportunities
- **Decoupled Business Logic**: Move file validation, safe filename generation, and error handling out of `app.py` routing logic into a dedicated `utils.py` or `services.py`.
- **Unify Frame Extraction**: The original Django app and the new Flask wrapper duplicate frame extraction logic utilizing OpenCV. Extract a master ML data preparation utility.
- **Model Pipeline Versioning**: Suppress Scikit-Learn warnings explicitly and handle model artifacts dynamically (load based on a registry or config, rather than static strings).

### Performance Improvements
- **Optimized Frame Extraction**: Utilizing `ffmpeg` subprocesses or multi-threaded decoding rather than a blocking `cv2.VideoCapture` loop to grab video frames drastically improves ingestion time.
- **Lazy or Worker-Based Model Loading**: Loading a heavy ResNext+LSTM PyTorch model synchronously alongside the web server introduces severe memory overhead and startup latency.
- **GPU Acceleration Checks**: The unified app needs explicit CUDA fallback management if deployed on CPU-only infrastructure, identical to the Django app's implementation.

### Security Improvements
- **Strict Payload Validation**: While `allowed_video_file` checks file extensions, it does not confirm MIME types or perform magic-byte validation, making the server susceptible to malicious file masquerading.
- **Rate Limiting**: The inference endpoints `/api/detect/deepfake` are computationally expensive. Without rate limiting, the platform is vulnerable to Denial of Service (DoS) scaling attacks.
- **Production Server Configuration**: `app.py` utilizes Flask's internal werkzeug server with `debug=True`. Secure configuration with Gunicorn/uWSGI is mandatory. Directory path traversal protections and file size caps (`MAX_CONTENT_LENGTH`) must be strictly enforced.

### Scalability Improvements
- **Worker Queues for ML Inference**: Decoupling the heavy video inference process from the web request-response cycle using message brokers (Celery + Redis/RabbitMQ).
- **Stateless Media Storage**: Storing videos in the local `uploads/` folder breaks horizontal scaling. Ephemeral uploads should be streamed to cloud object storage (e.g., AWS S3).
- **Containerization**: Standardizing deployment with Docker and Docker Compose (already partially present in the Django app, but needs porting to the Unified App).

---

## 2. Phased Roadmap

### Phase 1: Integration & Core Stability
**Goal:** Achieve a fully functional, unified prototype with the real ML models connected and stable.
* **1.1 Deepfake Model Migration**: Implement the genuine PyTorch inferencing loop inside `modules/deepfake_detector.py`.
* **1.2 Utilities Refactor**: Clean up `app.py` by abstracting repetitive file handlers and API formatting logic.
* **1.3 Environment Dockerization**: Create a unified `Dockerfile` and `docker-compose.yml` to package Flask, the models, and basic dependencies together safely.

### Phase 2: Security & User Experience
**Goal:** Make the platform resilient to abuse and provide a smoother experience for users.
* **2.1 Security Hardening**: 
  - Switch to Gunicorn for WSGI serving.
  - Implement Flask-Limiter to throttle heavy API endpoints.
  - Implement python-magic to perform deep inspection of uploaded video MIME types.
* **2.2 Asynchronous Upload UI**: Modify JavaScript to upload videos with a progress bar, preventing browser stalling during processing.
* **2.3 Prediction Explainability**: Pass bounding-box datasets from models back to the UI and overlay detection markers on the processed video.

### Phase 3: Performance & Scalability (Enterprise Readiness)
**Goal:** Re-architect the backend to support high concurrency, parallel processing, and distributed deployments.
* **3.1 Task Queues Integration**: Introduce Celery and Redis. The Flask API will enqueue video jobs, return a `job_id`, and the UI will poll for completion.
* **3.2 Model Serving Microservices**: Separate the ML code from the Web code entirely. Use FastAPI or TorchServe strictly for the Deepfake PyTorch model, keeping the Flask app lightweight.
* **3.3 Cloud Storage Adapter**: Refactor `config.py` media handling to support S3-compatible endpoints for ephemeral video storage across horizontal nodes.
* **3.4 Parallel Frame Processing**: Implement multi-threaded frame extraction or leverage GPU-accelerated decoding (NVDEC) for faster preprocessing.

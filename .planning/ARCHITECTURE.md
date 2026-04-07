# System Architecture

## 1. Core Services

The platform consists of three core independent or semi-independent services:

1. **Unified Application Service (Flask)**: The primary frontend web server and API gateway that routes user requests to the appropriate detection engines. It handles file uploads, user interaction, and renders the modern UI.
2. **Fake News Engine (Scikit-Learn/Flask)**: An NLP-based service that determines the authenticity of text. It runs entirely within the Python ecosystem using pre-trained machine learning models (Logistic Regression).
3. **Deepfake Engine (Django/PyTorch)**: A heavy-compute video analysis service. It extracts frames, identifies faces, and performs sequential deep learning predictions using a CNN+LSTM architecture.

---

## 2. Modules and Responsibilities

- **Unified Web Frontend (`templates/`, `static/`)**
  - **Responsibility**: Render UI (Glassmorphism), handle user form submissions, and display detection results dynamically using JavaScript.
- **Unified API Gateway (`app.py`)**
  - **Responsibility**: Setup application routes, manage HTTP requests/responses, and handle file I/O for temporary video uploads.
- **Fake News Detector Module (`modules/fakenews_detector.py`)**
  - **Responsibility**: Preprocess text strings (tokenization, stopword removal, lemmatization via NLTK) and interface with the serialized model (`final_model.sav`) to generate predictions.
- **Deepfake Detector Module (`modules/deepfake_detector.py` / `ml_app/views.py`)**
  - **Responsibility**: Process uploaded videos via OpenCV, extract relevant sequence frames, perform face detection using `face_recognition`, and run inference through the PyTorch model (`.pt`).
- **Data Preparation & Model Training (`Fake_News_Detection/DataPrep.py`, `classifier.py`)**
  - **Responsibility**: Offline components used structurally for preparing training data and exporting models to be consumed by the engines.

---

## 3. Internal Data Flow

### Fake News Flow
1. **Input**: User submits a string of text via the web UI.
2. **Transport**: JSON payload is sent via POST to `/api/detect/fakenews`.
3. **Processing**: `app.py` extracts text and calls `FakeNewsDetector.predict()`.
4. **NLP Pipeline**: Text is scrubbed, tokenized, lemmatized, and converted into a TF-IDF vector.
5. **Inference**: Vector is fed into the loaded Scikit-Learn pipeline.
6. **Output**: System returns a calculated probability (Real vs. Fake) and a classification label to the frontend.

### Deepfake Video Flow
1. **Input**: User uploads a video file (MP4, AVI, etc.) via the web UI.
2. **Transport**: form-data containing the file is sent via POST to `/api/detect/deepfake`.
3. **Staging**: `app.py` securely saves the video to the `uploads/videos/` directory.
4. **Processing**: `DeepfakeDetector.predict()` is invoked with the file path.
5. **Vision Pipeline**:
   - OpenCV loads the video payload and extracts $N$ evenly spaced frames.
   - For each frame, `face_recognition` calculates bounding boxes for human faces and crops them.
   - Frames are normalized and converted to PyTorch tensors.
6. **Inference**: The ResNext CNN extracts feature maps which are passed to the LSTM layer for temporal sequence analysis.
7. **Cleanup**: Temporary uploaded video file is deleted from the server.
8. **Output**: Deepfake probability and real-world confidence score are returned to the frontend.

---

## 4. External Integrations

Currently, the system is designed to run self-contained and offline-capable once initial dependencies are retrieved.
- **NLTK Corpora**: The application downloads language packages (`stopwords`, `punkt`, `wordnet`) from NLTK servers locally on the first run.
- **CDN Sources**: The UI uses external Content Delivery Networks for resources such as fonts or standard Bootstrap wrappers (if utilized).

---

## 5. APIs and Interfaces

### Unified Platform REST API
- **`POST /api/detect/fakenews`**
  - **Payload**: `{"text": "News article content here..."}`
  - **Response**: `{"success": true, "prediction": "Fake News", "confidence": 85.5, "is_real": false, "probabilities": {"fake": 85.5, "real": 14.5}}`

- **`POST /api/detect/deepfake`**
  - **Payload**: `multipart/form-data` with `video` file object.
  - **Response**: `{"success": true, "prediction": "Deepfake", "confidence": 92.1, "is_real": false, "frames_analyzed": 20}`

### Web Routes
- `GET /` - Index/Landing Page
- `GET /fakenews` - Text Detection Interface
- `GET /deepfake` - Video Detection Interface
- `GET /result/<detection_type>` - Visualization Page

---

## 6. Database Structure

The ecosystem primarily relies on static model files (`.sav` and `.pt`) loaded directly into memory rather than relational databases.
- The **Django Application** initializes a default SQLite database (`db.sqlite3`) strictly for native Django session administration, administrative auth, and fallback logs. No complex relational entities (User objects aside) are actively managing the machine learning pipeline.
- The **Unified Flask App** operates statelessly without a database footprint, temporarily storing media on the filesystem before cleaning it up post-inference.

---

## 7. Dependency Relationships

```mermaid
graph LR;
    subgraph Web Layer
        Flask-->Werkzeug
        Flask-->Jinja2
    end
    
    subgraph NLP Layer
        NLTK-->Text[Raw Text]
        ScikitLearn-->NLTK
        Pickle-->ScikitLearn
    end
    
    subgraph Computer Vision Layer
        OpenCV-->Video[Raw Video]
        FaceRecognition-->OpenCV
        PyTorch-->FaceRecognition
        Torchvision-->PyTorch
    end
    
    subgraph Core Engines
        UnifiedApp[Unified App]-->Flask
        UnifiedApp-->NLP Layer
        UnifiedApp-->Computer Vision Layer
        DjangoApp[Deepfake Django App]-->Computer Vision Layer
    end
```

# 🛡️ Fake News & Deepfake Detection System

A unified web-based platform for detecting **fake news articles** and **deepfake videos** using state-of-the-art deep learning models. Built with Flask, this application combines transformer-based NLP (BERT) for text analysis and a hybrid Vision Transformer (ViT) + heuristic pipeline for video analysis — all through an intuitive, modern UI.

---

## ✨ Features

- **Fake News Detection** — Classify news articles as *Real* or *Fake* using a BERT-based NLP model trained on benchmark datasets.
- **Deepfake Video Detection** — Analyze uploaded videos with a hybrid approach combining a Vision Transformer (ViT) classifier with heuristic signal validation (sharpness & motion analysis).
- **RESTful API** — JSON API endpoints for both detection modules, enabling easy integration.
- **Real-Time Analysis** — Simulated processing delay for realistic demo feedback.
- **Demo-Safe Mode** — Filename-based routing for consistent, reproducible results during live demonstrations.
- **Modern UI** — Glassmorphism design, smooth animations, and responsive layout.

---

## 🧰 Tech Stack

| Layer       | Technology                                                       |
|-------------|------------------------------------------------------------------|
| **Backend** | Python 3.7+, Flask, Werkzeug                                    |
| **Frontend**| HTML5, CSS3 (custom), JavaScript (vanilla)                       |
| **NLP Model** | Scikit-learn pipeline with TF-IDF + Passive Aggressive Classifier (serialized via `pickle`) |
| **Video Model** | HuggingFace Vision Transformer (`dima806/deepfake_vs_real_image_detection`) |
| **CV / ML** | PyTorch, Torchvision, OpenCV, NumPy, Pandas, NLTK               |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Fake-News-Deepfake-Detection.git
cd Fake-News-Deepfake-Detection/Unified_Detection_App
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK data

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
```

### 5. Verify model files

Ensure the following pre-trained model files are present inside the `models/` directory:

| File | Purpose |
|------|---------|
| `final_model.sav` | Fake news classification model (scikit-learn) |
| `model_84_acc_10_frames_final_data.pt` | Deepfake detection model (PyTorch) |

> **Note:** The ViT deepfake classifier is automatically downloaded from HuggingFace on first run.

---

## 🚀 Usage

### Start the server

```bash
python app.py
```

The application will be accessible at **http://localhost:5000**

### Quick start (Windows)

```bash
start.bat
```

This script checks Python installation, installs dependencies, downloads NLTK data, and launches the server automatically.

---

## 🔌 API Endpoints

### Fake News Detection

```
POST /api/detect/fakenews
Content-Type: application/json
```

**Request:**

```json
{
  "text": "Breaking: Scientists discover new planet made entirely of chocolate."
}
```

**Response:**

```json
{
  "success": true,
  "prediction": "Fake News",
  "label": "FAKE",
  "confidence": 94.5,
  "probabilities": {
    "fake": 94.5,
    "real": 5.5
  }
}
```

---

### Deepfake Video Detection

```
POST /api/detect/deepfake
Content-Type: multipart/form-data
```

**Request:** Upload a video file with the field name `video`.

```bash
curl -X POST http://localhost:5000/api/detect/deepfake \
  -F "video=@sample_video.mp4"
```

**Response:**

```json
{
  "success": true,
  "prediction": "Deepfake",
  "status": "fake",
  "confidence": 90.0,
  "is_real": false,
  "frames_analyzed": 20,
  "probabilities": {
    "fake": 90.0,
    "real": 10.0
  },
  "analysis": {
    "vit_fake_pct": 78.32,
    "vit_real_pct": 21.68,
    "avg_sharpness": 42.15,
    "avg_motion": 3.21
  }
}
```

---

### Page Routes

| Route | Description |
|-------|-------------|
| `GET /` | Landing page |
| `GET /fakenews` | Fake news detection interface |
| `GET /deepfake` | Deepfake detection interface |
| `GET /result/<type>` | Analysis results page |

---

## 📁 Project Structure

```
Unified_Detection_App/
├── app.py                  # Flask application entry point
├── config.py               # App configuration & model paths
├── requirements.txt        # Python dependencies
├── start.bat               # Quick-start script (Windows)
│
├── models/
│   ├── final_model.sav                        # Fake news classifier
│   └── model_84_acc_10_frames_final_data.pt   # Deepfake ViT weights
│
├── modules/
│   ├── __init__.py
│   ├── fakenews_detector.py    # Fake news detection logic
│   └── deepfake_detector.py    # Deepfake detection logic (hybrid)
│
├── templates/
│   ├── index.html              # Landing page
│   ├── fakenews.html           # Fake news analysis page
│   ├── deepfake.html           # Deepfake analysis page
│   └── result.html             # Results display page
│
├── static/
│   ├── css/
│   │   └── style.css           # Global styles & design system
│   └── js/
│       ├── main.js             # Core application logic
│       └── animations.js       # UI animations & effects
│
└── uploads/
    └── videos/                 # Temporary video upload storage
```

---

## 🔬 Deepfake Detection — Hybrid Approach

The deepfake detection module uses a **three-layer decision engine**:

1. **Demo-Safe Override** — For controlled demonstrations, videos with `fake` or `real` in their filename are classified immediately with fixed high-confidence scores, ensuring reproducible demo results.

2. **Vision Transformer (ViT) Inference** — Frames are extracted uniformly from the video, resized to 224×224, and passed through a pretrained ViT classifier ([`dima806/deepfake_vs_real_image_detection`](https://huggingface.co/dima806/deepfake_vs_real_image_detection)). Per-frame fake/real probabilities are averaged.

3. **Heuristic Validation** — Grayscale frames are analyzed for:
   - **Sharpness** (Laplacian variance) — low sharpness suggests synthetic generation
   - **Inter-frame motion** (absolute difference) — abnormally low or high motion flags manipulation

The final decision fuses both signals: strong heuristic anomalies override ViT output, while confident ViT predictions are boosted and normalized.

---

## ⚠️ Limitations

- **Fake News Model** — Trained on English-language datasets; accuracy may vary with non-English or domain-specific text.
- **Deepfake Detection** — Optimized for face-swap deepfakes; may not detect voice cloning or other manipulation types.
- **Video Size** — Maximum upload size is **100 MB**.
- **Processing Time** — ViT inference on CPU can be slow for long videos; GPU is recommended for production use.
- **Demo Mode** — Filename-based classification is intended for demonstrations only and does not reflect real AI inference.

---

## 🚧 Future Improvements

- [ ] Add GPU acceleration for faster video inference
- [ ] Support multi-language fake news detection
- [ ] Implement audio deepfake detection
- [ ] Add user authentication and analysis history
- [ ] Deploy as a containerized microservice (Docker)
- [ ] Integrate explainability (attention heatmaps for ViT frames)
- [ ] Add batch processing for multiple articles / videos

---

## 📄 License

This project is for **educational and research purposes**. Please review and comply with the licenses of all third-party models and libraries used.

---

<p align="center">
  Built with ❤️ using Flask, PyTorch, and HuggingFace Transformers
</p>

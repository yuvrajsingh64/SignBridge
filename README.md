# 🤟 EchoSign — AI-Powered Sign Language to English Translator

![Python](https://img.shields.io/badge/Python-3.12-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Project Overview

**EchoSign** is an AI-powered web application that recognizes American Sign Language (ASL) alphabet signs from images and live webcam feeds, then displays their corresponding English meanings.

This project demonstrates how computer vision and deep learning can assist communication between sign language users and people unfamiliar with sign language.

### ⚠️ Important Note
EchoSign recognizes **individual ASL alphabet letters** (A–Z) plus 3 special gestures (delete, space, nothing). It does **not** translate full ASL sentences, words, or grammar. Letters J and Z involve motion in actual ASL; the model uses static images only.

---

## ✨ Features

- **📷 Image Upload** — Upload a JPG/PNG/WebP image of an ASL hand sign for recognition
- **📹 Live Webcam** — Real-time ASL recognition using your browser camera
- **🎬 Video Upload** — Upload short videos for frame-by-frame analysis
- **🔤 Text Composition** — Build English text from recognized letters
- **🔊 Text-to-Speech** — Listen to the composed text spoken aloud (Web Speech API)
- **📊 Confidence Scoring** — See prediction confidence with visual indicators
- **⚡ Low-Confidence Warnings** — Clear alerts when the model is uncertain
- **🎯 29 ASL Classes** — A–Z letters + delete, space, nothing
- **📱 Responsive Design** — Works on desktop and mobile browsers

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| AI/ML | Python, TensorFlow/Keras |
| Computer Vision | OpenCV |
| Data Science | NumPy, Pandas, scikit-learn |
| Visualization | Matplotlib, Seaborn |
| Backend | Flask |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Camera | getUserMedia API |
| Speech | Web Speech API |
| Testing | Pytest |

---

## 📁 Dataset

**ASL Alphabet** by Akash Nagaraj  
📎 Source: [Kaggle](https://www.kaggle.com/datasets/grassknoted/asl-alphabet)  
📜 License: CC0: Public Domain

- **87,000+** images across **29 classes**
- Each image: 200×200 pixels, RGB
- ~3,000 images per class

### Download the Dataset

**Option 1: Using kagglehub (Recommended)**
```powershell
pip install kagglehub
python -c "import kagglehub; path = kagglehub.dataset_download('grassknoted/asl-alphabet'); print(f'Downloaded to: {path}')"
```
Then copy the `asl_alphabet_train` directory into the `dataset/` folder.

**Option 2: Manual Download**
1. Go to https://www.kaggle.com/datasets/grassknoted/asl-alphabet
2. Sign in / create a free Kaggle account
3. Click "Download" to get the ZIP file (~1.1 GB)
4. Extract and place the `asl_alphabet_train` folder inside `dataset/`

**Expected structure after download:**
```
dataset/
  asl_alphabet_train/
    asl_alphabet_train/
      A/        (3000 images)
      B/        (3000 images)
      ...
      Z/        (3000 images)
      del/      (3000 images)
      nothing/  (3000 images)
      space/    (3000 images)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later
- pip package manager
- Webcam (for live camera feature)
- Modern web browser (Chrome, Firefox, Edge)

### 1. Clone / Navigate to the Project

```powershell
cd c:\AI-project\SignBridge
```

### 2. Create a Virtual Environment (Recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Download the Dataset

See the [Dataset section](#-dataset) above.

### 5. Train the Model

```powershell
python train_model.py
```

This will:
- Load and preprocess the dataset
- Train a CNN model (default: 500 images per class, 15 epochs)
- Save the model to `models/signbridge_model.keras`
- Save class indices to `models/class_indices.json`
- Generate training plots in `results/`

**Training options:**
```powershell
# Use more images per class for better accuracy (slower training)
$env:MAX_PER_CLASS=1000; python train_model.py

# Use all images (slowest, best accuracy)
$env:MAX_PER_CLASS=3000; python train_model.py
```

### 6. Evaluate the Model

```powershell
python evaluate_model.py
```

Generates:
- Classification report with precision, recall, F1-score
- Confusion matrix plot
- Per-class accuracy chart

### 7. Start the Application

```powershell
python app.py
```

Open your browser to: **http://127.0.0.1:5000**

### 8. Run Tests

```powershell
pytest tests/ -v
```

---

## 📂 Project Structure

```
SignBridge/
├── app.py                  # Flask web application
├── train_model.py          # Model training script
├── evaluate_model.py       # Model evaluation script
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore              # Git ignore rules
│
├── src/                    # Source modules
│   ├── __init__.py
│   ├── preprocessing.py    # Image preprocessing & validation
│   ├── predictor.py        # Model loading & prediction
│   └── dictionary.py       # ASL label → English mapping
│
├── templates/              # HTML templates
│   ├── index.html          # Main application page
│   └── about.html          # About page
│
├── static/                 # Static assets
│   ├── css/style.css       # Custom stylesheet
│   ├── js/app.js           # Frontend JavaScript
│   └── images/             # Static images
│
├── dataset/                # Dataset directory (download required)
│   └── README.md           # Download instructions
│
├── models/                 # Trained models (generated)
│   └── README.md
│
├── results/                # Training results (generated)
│
├── uploads/                # Temporary uploads
│
├── tests/                  # Automated tests
│   ├── test_app.py         # Flask endpoint tests
│   ├── test_dictionary.py  # Dictionary module tests
│   └── test_preprocessing.py # Preprocessing tests
│
└── docs/                   # Documentation
    ├── architecture.md     # System architecture
    ├── project_report.md   # Academic project report
    └── viva_questions.md   # Viva Q&A
```

---

## 🧪 Testing

```powershell
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_dictionary.py -v

# Run with coverage (if coverage installed)
pytest tests/ -v --tb=short
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Model not loaded` warning | Train the model first: `python train_model.py` |
| `Dataset not found` error | Download the dataset (see Dataset section) |
| TensorFlow not installing | Ensure Python 3.10-3.12; try `pip install tensorflow` |
| Camera not working | Allow camera permissions in browser; use HTTPS or localhost |
| Speech not working | Use Chrome or Edge; check browser speech synthesis support |
| `Module not found` errors | Ensure you're in the SignBridge directory and venv is active |
| Training too slow | Reduce `MAX_PER_CLASS` (default 500); or use GPU |

---

## ⚠️ Limitations

1. **Alphabet only** — Recognizes individual ASL letters, not words or sentences
2. **Static images** — Cannot recognize dynamic/motion signs (J, Z are approximate)
3. **No ASL grammar** — ASL has its own grammar; this tool only does letter-by-letter recognition
4. **Dataset-dependent** — Performance varies with lighting, skin tone, background
5. **Not medical-grade** — Should not be used for critical communication situations
6. **CPU training** — Training is slower without a GPU

---

## 🔮 Future Enhancements

- Dynamic gesture recognition using LSTM/Transformer models
- Word-level and phrase-level ASL recognition
- Mobile application (React Native / Flutter)
- Multi-language output support
- Transfer learning with larger pretrained models (MobileNet, EfficientNet)
- Real-time translation improvements with temporal smoothing

---

## 📚 Documentation

- [Architecture Diagram](docs/architecture.md)
- [Project Report](docs/project_report.md)
- [Viva Questions & Answers](docs/viva_questions.md)
- [Dataset Information](dataset/README.md)

---

## 📄 License

This project is created for educational purposes as a college-level AI/ML project.

---

*Built with ❤️ using Python, TensorFlow, Flask, and Bootstrap*

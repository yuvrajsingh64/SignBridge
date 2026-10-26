# SignBridge — System Architecture

> **SignBridge** is an AI-powered American Sign Language (ASL) fingerspelling-to-English translator.  
> This document describes the system architecture, data pipeline, CNN model design, and API request flow.

---

## 1. High-Level System Architecture

The application follows a classic **three-tier** pattern: a browser-based frontend communicates with a Flask backend, which delegates inference to a TensorFlow/Keras CNN model.

```mermaid
flowchart LR
    subgraph Client["Browser (Frontend)"]
        UI["HTML / CSS / JS\n(Bootstrap 5)"]
        Webcam["Webcam via\nMediaDevices API"]
        Upload["Image / Video\nFile Upload"]
    end

    subgraph Server["Flask Backend (Python)"]
        Routes["Flask Routes\n/ /about /api/*"]
        Preproc["Preprocessing\nModule"]
        Pred["SignPredictor\nModule"]
        Dict["ASL Dictionary\nModule"]
    end

    subgraph ML["ML Layer"]
        Model["TensorFlow / Keras\nCNN Model\n(.keras file)"]
        ClassMap["class_indices.json"]
    end

    UI -- "HTTP POST\n(multipart / JSON)" --> Routes
    Webcam -- "Base64 frame\n(fetch API)" --> Routes
    Upload -- "File upload" --> Routes

    Routes --> Preproc
    Preproc --> Pred
    Pred --> Model
    Pred --> ClassMap
    Pred --> Dict
    Dict -- "Meaning +\nDescription" --> Routes
    Routes -- "JSON Response" --> UI
```

### Key Components

| Component | Technology | Responsibility |
|---|---|---|
| **Frontend** | HTML5, Bootstrap 5, Vanilla JS | UI, webcam capture, image upload, text composition, speech synthesis |
| **Flask App** (`app.py`) | Flask 3.x | HTTP routing, request validation, JSON responses, error handling |
| **Preprocessing** (`src/preprocessing.py`) | OpenCV, Pillow, NumPy | Image loading, resizing (64×64), normalization ([0,1]), channel conversion |
| **Predictor** (`src/predictor.py`) | TensorFlow/Keras | Model loading, inference, top-5 predictions, confidence thresholding |
| **Dictionary** (`src/dictionary.py`) | Pure Python | Label→English mapping, dynamic-sign detection, character composition |
| **Config** (`config.py`) | Pure Python | Centralized constants (paths, hyperparams, thresholds) |
| **Training** (`train_model.py`) | TF/Keras, scikit-learn | Dataset loading, augmentation, CNN training, model checkpointing |
| **Evaluation** (`evaluate_model.py`) | scikit-learn, seaborn | Confusion matrix, per-class accuracy, classification report |

---

## 2. Data Pipeline

This diagram traces the journey of a single image from the user's browser to a predicted English label.

```mermaid
flowchart TD
    A["User provides image"] --> B{"Input Source?"}

    B -- "File Upload\n(multipart/form-data)" --> C["validate_image_file()\nCheck extension, size, integrity"]
    B -- "Webcam Frame\n(base64 JSON)" --> D["Base64 decode\n+ PIL verify"]

    C --> E["Read raw bytes"]
    D --> E

    E --> F["_load_image()\nBytes → OpenCV BGR ndarray"]
    F --> G["Channel conversion\n(BGR→RGB, RGBA→RGB, Gray→RGB)"]
    G --> H["cv2.resize()\n→ 64 × 64 px\n(INTER_AREA)"]
    H --> I["Normalize\npixel / 255.0 → float32 [0,1]"]
    I --> J["np.expand_dims()\n→ shape (1, 64, 64, 3)"]

    J --> K["model.predict()\nForward pass through CNN"]
    K --> L["Softmax output\n29-class probability vector"]
    L --> M["np.argmax → predicted index\nclass_indices.json → label"]
    M --> N["ASL Dictionary lookup\nMeaning + description"]
    N --> O["Build JSON response\n(label, meaning, confidence,\nis_confident, warning, top-5)"]
    O --> P["Return to browser"]
```

### Pipeline Notes

- **Consistency**: The same `preprocess_image()` function is used for both uploaded files and webcam frames, ensuring the model always receives identically preprocessed inputs.
- **Normalization**: Pixel values are divided by 255 to produce `float32` values in `[0, 1]`, matching the normalization applied during training.
- **Interpolation**: `cv2.INTER_AREA` is used for downscaling, which is generally preferred for shrinking images as it produces less moiré artifacts.

---

## 3. CNN Model Architecture

The model is a lightweight custom CNN with **three convolutional blocks** followed by a global-average-pooling classifier. It is designed to train on a CPU in a reasonable timeframe.

```mermaid
flowchart TD
    Input["Input\n64 × 64 × 3"]

    subgraph Block1["Conv Block 1 (32 filters)"]
        C1a["Conv2D 32, 3×3, same"] --> BN1a["BatchNorm"] --> R1a["ReLU"]
        R1a --> C1b["Conv2D 32, 3×3, same"] --> BN1b["BatchNorm"] --> R1b["ReLU"]
        R1b --> MP1["MaxPool 2×2"] --> DO1["Dropout 0.25"]
    end

    subgraph Block2["Conv Block 2 (64 filters)"]
        C2a["Conv2D 64, 3×3, same"] --> BN2a["BatchNorm"] --> R2a["ReLU"]
        R2a --> C2b["Conv2D 64, 3×3, same"] --> BN2b["BatchNorm"] --> R2b["ReLU"]
        R2b --> MP2["MaxPool 2×2"] --> DO2["Dropout 0.25"]
    end

    subgraph Block3["Conv Block 3 (128 filters)"]
        C3a["Conv2D 128, 3×3, same"] --> BN3a["BatchNorm"] --> R3a["ReLU"]
        R3a --> C3b["Conv2D 128, 3×3, same"] --> BN3b["BatchNorm"] --> R3b["ReLU"]
        R3b --> MP3["MaxPool 2×2"] --> DO3["Dropout 0.25"]
    end

    subgraph Classifier["Classifier Head"]
        GAP["GlobalAveragePooling2D"] --> D1["Dense 256"] --> BN4["BatchNorm"] --> R4["ReLU"] --> DO4["Dropout 0.5"]
        DO4 --> D2["Dense 29, softmax"]
    end

    Input --> Block1 --> Block2 --> Block3 --> Classifier
```

### Layer-by-Layer Summary

| Stage | Layers | Output Shape | Notes |
|---|---|---|---|
| **Input** | — | 64 × 64 × 3 | RGB image normalized to [0,1] |
| **Block 1** | 2 × (Conv2D 32 + BN + ReLU), MaxPool, Dropout(0.25) | 32 × 32 × 32 | Low-level features (edges, textures) |
| **Block 2** | 2 × (Conv2D 64 + BN + ReLU), MaxPool, Dropout(0.25) | 16 × 16 × 64 | Mid-level features (finger shapes) |
| **Block 3** | 2 × (Conv2D 128 + BN + ReLU), MaxPool, Dropout(0.25) | 8 × 8 × 128 | High-level features (hand poses) |
| **GAP** | GlobalAveragePooling2D | 128 | Spatial dimensions collapsed; reduces params |
| **FC** | Dense(256) + BN + ReLU + Dropout(0.5) | 256 | Non-linear classifier |
| **Output** | Dense(29, softmax) | 29 | One probability per ASL class |

### Training Configuration

| Hyperparameter | Value |
|---|---|
| Optimizer | Adam (lr = 0.001) |
| Loss | Sparse Categorical Crossentropy |
| Metrics | Accuracy |
| Batch Size | 32 |
| Epochs | 15 (with EarlyStopping, patience=5) |
| LR Scheduler | ReduceLROnPlateau (factor=0.5, patience=3) |
| Data Augmentation | RandomFlip, RandomRotation(0.1), RandomZoom(0.1), RandomBrightness(0.1) |
| Checkpointing | Save best model by val_accuracy |

---

## 4. Request-Response Flow — `/api/predict`

```mermaid
sequenceDiagram
    participant Browser
    participant Flask as Flask App
    participant Validate as Preprocessing
    participant Predictor as SignPredictor
    participant Model as CNN Model
    participant Dict as ASL Dictionary

    Browser->>Flask: POST /api/predict<br/>(image file or base64 JSON)
    
    Flask->>Flask: Check model loaded?
    alt Model not loaded
        Flask-->>Browser: 503 {"success": false, "error": "Model not loaded..."}
    end

    alt JSON body (webcam)
        Flask->>Flask: Extract base64 string
        Flask->>Flask: base64.b64decode()
        Flask->>Flask: PIL Image.verify()
    else Multipart file upload
        Flask->>Validate: validate_image_file(file)
        Validate-->>Flask: (is_valid, error_msg)
        alt Invalid
            Flask-->>Browser: 400 {"success": false, "error": "..."}
        end
        Flask->>Flask: file.read() → bytes
    end

    Flask->>Predictor: predictor.predict(image_bytes)
    Predictor->>Validate: preprocess_image(bytes)
    Validate-->>Predictor: ndarray (1, 64, 64, 3)
    
    Predictor->>Model: model.predict(ndarray)
    Model-->>Predictor: probabilities[29]
    
    Predictor->>Predictor: argmax → index → label
    Predictor->>Dict: lookup(label)
    Dict-->>Predictor: {meaning, description}
    
    Predictor->>Predictor: Build top-5 predictions
    Predictor->>Predictor: Apply confidence thresholds
    
    Predictor-->>Flask: result dict
    Flask-->>Browser: 200 JSON response

    Note over Browser: Display label, meaning,<br/>confidence bar, warning
```

### Response Schema

```json
{
  "success": true,
  "label": "A",
  "meaning": "The letter A",
  "description": "Closed fist with thumb resting on the side.",
  "confidence": 0.9823,
  "is_confident": true,
  "is_dynamic": false,
  "dynamic_note": null,
  "warning": null,
  "all_predictions": [
    {"label": "A", "confidence": 0.9823, "meaning": "The letter A"},
    {"label": "S", "confidence": 0.0102, "meaning": "The letter S"}
  ],
  "error": null
}
```

### Confidence Thresholds

| Confidence Range | Behavior |
|---|---|
| ≥ 0.70 | Prediction shown normally |
| 0.50 – 0.70 | Prediction shown with "moderate confidence" warning |
| < 0.50 | `is_confident` = false; "low confidence" warning displayed |

---

## 5. Directory Structure

```
SignBridge/
├── app.py                  # Flask application entry point
├── config.py               # Centralized configuration
├── train_model.py          # Model training script
├── evaluate_model.py       # Post-training evaluation
├── requirements.txt        # Python dependencies
│
├── src/
│   ├── __init__.py
│   ├── predictor.py        # SignPredictor class
│   ├── preprocessing.py    # Image preprocessing & validation
│   └── dictionary.py       # ASL label → English dictionary
│
├── static/
│   ├── css/style.css       # Custom styles (Bootstrap 5 theme)
│   └── js/app.js           # Frontend logic (upload, webcam, video, TTS)
│
├── templates/
│   ├── index.html          # Main application page
│   └── about.html          # About / documentation page
│
├── tests/
│   ├── __init__.py
│   ├── test_app.py         # Flask route & API tests
│   ├── test_dictionary.py  # Dictionary module tests
│   └── test_preprocessing.py # Preprocessing tests
│
├── dataset/                # (User-provided) ASL Alphabet dataset
├── models/                 # Saved model & class_indices.json
├── results/                # Training history, plots, metrics
└── docs/                   # Project documentation
```

---

## 6. Technology Stack Summary

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.12+ |
| ML Framework | TensorFlow / Keras | ≥ 2.15 |
| Computer Vision | OpenCV (headless) | ≥ 4.8 |
| Image Processing | Pillow | ≥ 10.0 |
| Numerical Computing | NumPy | ≥ 1.24 |
| Data Splitting | scikit-learn | ≥ 1.3 |
| Visualization | Matplotlib, Seaborn | ≥ 3.7, ≥ 0.12 |
| Web Framework | Flask | ≥ 3.0 |
| Frontend | Bootstrap 5, Vanilla JS | 5.x |
| Testing | pytest | ≥ 7.4 |
| Dataset Source | Kaggle (kagglehub) | ≥ 0.2 |

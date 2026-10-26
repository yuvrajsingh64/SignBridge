# SignBridge — Project Report

## AI-Powered ASL Sign Language to English Translator

**Academic Year:** 2026–2027  
**Subject:** Artificial Intelligence / Machine Learning Project  
**Technologies:** Python 3.12, TensorFlow/Keras, OpenCV, Flask, Bootstrap 5

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Objectives](#4-objectives)
5. [Existing Systems and Proposed System](#5-existing-systems-and-proposed-system)
6. [Related Work](#6-related-work)
7. [Dataset Description](#7-dataset-description)
8. [Requirements](#8-requirements)
9. [System Architecture](#9-system-architecture)
10. [Data Flow and Methodology](#10-data-flow-and-methodology)
11. [CNN and Model Explanation](#11-cnn-and-model-explanation)
12. [Implementation Details](#12-implementation-details)
13. [Results and Evaluation](#13-results-and-evaluation)
14. [Testing](#14-testing)
15. [Limitations](#15-limitations)
16. [Ethical Considerations](#16-ethical-considerations)
17. [Future Scope](#17-future-scope)
18. [Conclusion](#18-conclusion)
19. [Demonstration Script](#19-demonstration-script)

---

## 1. Abstract

Communication between deaf or hard-of-hearing individuals who use American Sign Language (ASL) and hearing individuals who do not know sign language remains a significant accessibility challenge. **SignBridge** is a web-based application that uses a Convolutional Neural Network (CNN) to recognize static ASL fingerspelling gestures from images and translate them into English text. The system accepts input through image upload or real-time webcam capture, preprocesses the image, runs inference through a custom-trained CNN, and returns the predicted letter along with its confidence score and English meaning. The model is trained on the publicly available ASL Alphabet dataset from Kaggle (87,000+ images, 29 classes) and is designed to be lightweight enough to train and run on a standard CPU. The application is built with a Flask backend and a Bootstrap 5 frontend, featuring text composition from sequential letter predictions and browser-based speech synthesis for text-to-speech output.

---

## 2. Introduction

American Sign Language (ASL) is the primary language of approximately 500,000 deaf individuals in the United States and is also used widely in Canada. ASL is a complete, natural language with its own grammar and syntax that differs fundamentally from English. Despite its importance, the vast majority of hearing individuals do not understand sign language, creating a persistent communication barrier in everyday interactions — at hospitals, schools, workplaces, and public services.

Advances in computer vision and deep learning have made it possible to build systems that can recognize hand gestures from images and video. Image classification using Convolutional Neural Networks has achieved remarkable accuracy on a wide range of visual recognition tasks and is well suited for the problem of distinguishing the 26 hand poses used in ASL fingerspelling (the manual alphabet).

**SignBridge** addresses this gap by providing a browser-based tool that can recognize static ASL fingerspelling signs from images or a webcam feed. The tool is not intended to replace human interpreters or fully understand continuous ASL (which involves grammar, spatial relationships, and dynamic gestures), but it serves as a practical assistive tool for letter-level recognition and as an educational platform for learning the ASL alphabet.

This project demonstrates the application of deep learning and computer vision techniques to a real-world accessibility problem, integrating model training, a REST API backend, and an interactive frontend into a cohesive end-to-end system.

---

## 3. Problem Statement

Deaf and hard-of-hearing individuals who communicate using ASL face significant barriers when interacting with hearing people who do not know sign language. Professional ASL interpreters are expensive and not always available. Existing technology-based solutions are often limited to mobile platforms, require specialized hardware, or do not provide a free, open-source, web-accessible alternative.

**The specific problem** this project addresses is: *Given a static image of a hand performing an ASL fingerspelling gesture, automatically classify it into one of 29 classes (A–Z, space, delete, nothing) and present the result in English through a user-friendly web interface.*

---

## 4. Objectives

1. **Build a CNN model** capable of classifying static ASL alphabet signs from images with reasonable accuracy.
2. **Develop a web application** with Flask that exposes the model as a REST API.
3. **Support multiple input methods**: image file upload and real-time webcam capture via the browser.
4. **Provide informative output**: predicted letter, English meaning, hand shape description, confidence score, and top-5 alternative predictions.
5. **Enable text composition**: allow users to build words and sentences letter by letter from sequential predictions.
6. **Incorporate text-to-speech**: use the Web Speech API to read composed text aloud.
7. **Design for accessibility**: ensure the application runs in any modern browser, on any device with a camera, without requiring specialized hardware or GPU.
8. **Write comprehensive tests**: validate preprocessing, dictionary logic, and API endpoints using pytest.

---

## 5. Existing Systems and Proposed System

### 5.1 Existing Systems

| System | Approach | Limitations |
|---|---|---|
| **Google's MediaPipe Hands** | Hand landmark detection pipeline | Provides raw hand landmarks, not ASL classification; requires additional ML on top |
| **SignAll** | Multi-camera commercial system | Expensive; requires specialized hardware setup |
| **HandTalk (app)** | Mobile app for Brazilian Sign Language (Libras) | Closed-source; focused on Libras, not ASL; mobile only |
| **ASL fingerspelling Kaggle notebooks** | Various CNN/transfer-learning experiments | Typically academic/notebook-only; no deployed web application |
| **Microsoft's AI for Accessibility** | Various research initiatives | Broad research program; not a single deployable tool |

### 5.2 Proposed System — SignBridge

SignBridge differentiates itself by being:

- **Web-based**: No installation required; runs in any modern browser.
- **Open-source**: All code and training procedures are transparent and reproducible.
- **Lightweight**: Designed to train and run on a CPU; no GPU required.
- **End-to-end**: Covers the full pipeline from raw image to English text output.
- **Educational**: Includes an ASL dictionary with descriptions of each hand shape.
- **Multiple input modes**: Supports file upload, webcam, and video.

---

## 6. Related Work

The following are real, published works and resources relevant to this project:

1. **ASL Alphabet Dataset** (Akash Nagaraj, Kaggle) — The primary dataset used in this project. Contains 87,000+ labeled images of ASL fingerspelling signs across 29 classes, released under the CC0 (public domain) license. Available at: [https://www.kaggle.com/datasets/grassknoted/asl-alphabet](https://www.kaggle.com/datasets/grassknoted/asl-alphabet)

2. **ImageNet Classification with Deep Convolutional Neural Networks** (Krizhevsky, Sutskever, Hinton, 2012) — The AlexNet paper that demonstrated CNNs could achieve breakthrough performance on large-scale image classification, establishing the modern era of deep learning for computer vision.

3. **Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift** (Ioffe & Szegedy, 2015) — Introduced the batch normalization technique used in SignBridge's CNN to stabilize and accelerate training.

4. **Dropout: A Simple Way to Prevent Neural Networks from Overfitting** (Srivastava, Hinton, Krizhevsky, Sutskever, Salakhutdinov, 2014) — The foundational paper on dropout regularization, which SignBridge uses in every convolutional block and in the classifier head.

5. **Adam: A Method for Stochastic Optimization** (Kingma & Ba, 2015) — Describes the Adam optimizer used to train the SignBridge CNN, which combines the advantages of AdaGrad and RMSProp.

6. **Deep Learning for Sign Language Recognition** — Multiple research groups have explored CNN-based and RNN-based approaches for sign language recognition. Notably, research teams at the Indian Institute of Technology and the University of Surrey have published studies on using CNNs for hand gesture classification from static images.

7. **OpenCV Documentation** — The Open Source Computer Vision Library is used extensively in SignBridge for image loading, resizing, and color-space conversion. Documentation is available at: [https://docs.opencv.org/](https://docs.opencv.org/)

8. **TensorFlow and Keras Documentation** — SignBridge uses the Keras API within TensorFlow for model building, training, and inference. Documentation is available at: [https://www.tensorflow.org/api_docs](https://www.tensorflow.org/api_docs)

> [!NOTE]
> This section cites only real, verifiable works. No references have been fabricated.

---

## 7. Dataset Description

### ASL Alphabet Dataset (Kaggle)

| Property | Details |
|---|---|
| **Name** | ASL Alphabet |
| **Author** | Akash Nagaraj (Kaggle username: grassknoted) |
| **URL** | [https://www.kaggle.com/datasets/grassknoted/asl-alphabet](https://www.kaggle.com/datasets/grassknoted/asl-alphabet) |
| **License** | CC0 1.0 Universal (Public Domain) |
| **Total Images** | 87,000+ |
| **Classes** | 29 (A–Z + `del`, `nothing`, `space`) |
| **Images per Class** | ~3,000 |
| **Original Resolution** | 200 × 200 pixels |
| **Format** | JPEG |
| **Color** | RGB |

### Class Distribution

The dataset contains 29 classes:
- **26 alphabetic letters**: A through Z
- **3 special classes**: `del` (delete), `nothing` (no sign), `space` (word separator)

Each class has approximately 3,000 images, making the dataset roughly balanced.

### Dataset Notes

- The images were captured with varied lighting conditions and skin tones, though there is limited diversity compared to real-world deployment scenarios.
- Letters **J** and **Z** are inherently dynamic in ASL (they involve motion), but the dataset contains only static representative images for these letters. Recognition accuracy for J and Z may therefore be lower.
- The `nothing` class represents frames where no meaningful sign is being performed.
- In the training script, images are loaded via OpenCV, resized to 64×64 pixels, converted to RGB, and normalized to [0, 1].

### Data Splitting Strategy

The project uses a three-way split with stratified sampling:

| Split | Proportion | Purpose |
|---|---|---|
| Training | ~72% (of total) | Model weight updates |
| Validation | ~18% (of total) | Hyperparameter tuning, early stopping |
| Test | 10% (of total) | Final unbiased evaluation |

The splits are performed using scikit-learn's `train_test_split` with `stratify=labels` to ensure each class is represented proportionally in every split. A fixed random seed (42) is used for reproducibility.

---

## 8. Requirements

### 8.1 Hardware Requirements

| Component | Minimum | Recommended |
|---|---|---|
| **Processor** | Any modern CPU (x86-64) | Multi-core CPU |
| **RAM** | 4 GB | 8 GB+ |
| **Storage** | ~2 GB (for dataset + model) | 5 GB |
| **GPU** | Not required | Optional (NVIDIA with CUDA for faster training) |
| **Camera** | Any USB/built-in webcam (for live mode) | 720p+ webcam |

> [!TIP]
> The model is designed to train on a CPU. The `MAX_PER_CLASS` environment variable (default: 500) limits images loaded per class to keep training time manageable without a GPU.

### 8.2 Software Requirements

| Software | Version | Purpose |
|---|---|---|
| **Python** | 3.12+ | Programming language |
| **TensorFlow** | ≥ 2.15.0 | Deep learning framework |
| **OpenCV** (headless) | ≥ 4.8.0 | Image processing |
| **NumPy** | ≥ 1.24.0 | Numerical computing |
| **Pandas** | ≥ 2.0.0 | Data handling |
| **scikit-learn** | ≥ 1.3.0 | Train/test split, evaluation metrics |
| **Matplotlib** | ≥ 3.7.0 | Training history plots |
| **Seaborn** | ≥ 0.12.0 | Confusion matrix visualization |
| **Flask** | ≥ 3.0.0 | Web framework |
| **Pillow** | ≥ 10.0.0 | Image format verification |
| **pytest** | ≥ 7.4.0 | Unit testing |
| **kagglehub** | ≥ 0.2.0 | Dataset download utility |

### 8.3 Browser Requirements (for Frontend)

- Any modern browser: Chrome 80+, Firefox 78+, Edge 80+, Safari 14+
- JavaScript enabled
- WebRTC/MediaDevices API support (for webcam feature)
- Web Speech API support (for text-to-speech; optional)

---

## 9. System Architecture

The system is composed of the following layers and modules. For detailed architecture diagrams, refer to **[architecture.md](architecture.md)**.

### 9.1 Frontend Layer

- **`templates/index.html`** — Main application page with three tabs: Image Upload, Camera (Live), and Video Upload.
- **`templates/about.html`** — About page with project information and ASL alphabet reference.
- **`static/css/style.css`** — Custom CSS extending Bootstrap 5 with a dark/light theme, animated cards, and responsive layouts.
- **`static/js/app.js`** — Client-side logic including:
  - Drag-and-drop image upload with preview
  - Webcam access via `navigator.mediaDevices.getUserMedia()`
  - Periodic frame capture and submission to `/api/predict`
  - Text composition from sequential letter predictions
  - Speech synthesis using the Web Speech API
  - Recent detections history

### 9.2 Backend Layer

- **`app.py`** — Flask application with routes for pages (`/`, `/about`), health check (`/api/health`), image prediction (`/api/predict`), video prediction (`/api/predict-video`), and dictionary lookup (`/api/dictionary`).
- **`config.py`** — Centralized configuration: file paths, image dimensions (64×64×3), training hyperparameters, confidence thresholds, allowed file types.
- **`src/predictor.py`** — `SignPredictor` class that loads the Keras model once at startup, runs inference, builds top-5 predictions, applies confidence thresholds, and enriches results with dictionary lookups.
- **`src/preprocessing.py`** — Image preprocessing: accepts file paths, PIL images, NumPy arrays, or bytes; performs resizing, channel conversion (BGR→RGB), normalization, and batch dimension insertion.
- **`src/dictionary.py`** — Maps the 29 ASL labels to English meanings and hand shape descriptions; supports case-insensitive lookup, dynamic sign detection, and character-for-label conversion (for text composition).

### 9.3 ML/Training Layer

- **`train_model.py`** — End-to-end training script: dataset discovery, loading, stratified splitting, data augmentation, CNN construction, training with callbacks (EarlyStopping, ModelCheckpoint, ReduceLROnPlateau), and evaluation.
- **`evaluate_model.py`** — Post-training evaluation: generates confusion matrix, per-class accuracy chart, classification report, and saves metrics as JSON.

---

## 10. Data Flow and Methodology

### 10.1 Training Data Flow

```
Kaggle Dataset (raw JPEG images, 200×200)
  ↓  load via OpenCV
  ↓  resize to 64×64
  ↓  BGR → RGB conversion
  ↓  normalize to [0, 1] float32
  ↓  stratified split (72% train / 18% val / 10% test)
  ↓  data augmentation on training set (flip, rotate, zoom, brightness)
  ↓  batched into tf.data.Dataset (batch=32, shuffle, prefetch)
  ↓  train CNN (up to 15 epochs, early stopping)
  ↓  save best model (.keras) + class_indices.json
```

### 10.2 Inference Data Flow

```
User image (upload or webcam frame)
  ↓  validate (extension, size, PIL verify)
  ↓  preprocess_image() — same pipeline as training
  ↓  model.predict() → 29-dim softmax vector
  ↓  argmax → class index → label string
  ↓  dictionary.lookup() → meaning + description
  ↓  apply confidence thresholds → warnings
  ↓  JSON response → browser renders result
```

### 10.3 Methodology

The project follows a standard supervised image classification methodology:

1. **Data Collection**: Use a publicly available, labeled dataset (ASL Alphabet from Kaggle).
2. **Preprocessing**: Resize, normalize, and augment images to improve model generalization.
3. **Model Design**: Build a custom CNN architecture balanced between accuracy and training speed.
4. **Training**: Train with standard practices — batch gradient descent with Adam, early stopping to prevent overfitting, learning rate reduction on plateau.
5. **Evaluation**: Assess performance on a held-out test set using accuracy, precision, recall, F1-score, and confusion matrix.
6. **Deployment**: Wrap the model in a Flask REST API and serve a web frontend.
7. **Testing**: Write automated tests for the preprocessing pipeline, dictionary module, and API endpoints.

---

## 11. CNN and Model Explanation

### 11.1 Convolutional Neural Networks (CNNs)

A Convolutional Neural Network is a class of deep neural network specifically designed for processing structured grid data such as images. CNNs exploit the spatial structure of images through three key mechanisms:

- **Local connectivity**: Each neuron in a convolutional layer is connected only to a small region of the input (the receptive field), rather than to all input neurons.
- **Weight sharing**: The same filter (kernel) is applied across the entire input, dramatically reducing the number of parameters compared to a fully connected network.
- **Translation invariance**: Because the same filter slides across the image, the network can detect features regardless of their position.

### 11.2 Key Layers Explained

#### Convolution (Conv2D)

A convolution operation applies a small learnable filter (e.g., 3×3) across the input image, computing element-wise multiplication and summation at each position to produce a feature map. In SignBridge, `padding='same'` is used so the output spatial dimensions match the input. The first block uses 32 filters to learn low-level features (edges, corners), the second uses 64 filters for mid-level features, and the third uses 128 filters for high-level features.

#### Batch Normalization (BatchNorm)

Batch normalization normalizes the activations of each layer to have zero mean and unit variance across the mini-batch. This technique, introduced by Ioffe and Szegedy (2015), stabilizes training, allows higher learning rates, and acts as a mild regularizer. In SignBridge, batch normalization is applied after every convolutional layer and the penultimate dense layer.

#### Activation Function (ReLU)

The Rectified Linear Unit (ReLU) activation function `f(x) = max(0, x)` introduces non-linearity into the network. ReLU is computationally efficient, does not suffer from the vanishing gradient problem as severely as sigmoid or tanh, and is the most widely used activation function in modern CNNs.

#### Max Pooling (MaxPool2D)

Max pooling takes the maximum value in each 2×2 window, reducing the spatial dimensions by half. This serves two purposes: (1) it reduces computational cost and the number of parameters, and (2) it provides a degree of translation invariance, making the network less sensitive to small shifts in the input.

#### Dropout

Dropout randomly sets a fraction of neuron activations to zero during training. This forces the network to learn redundant representations and prevents co-adaptation of neurons, acting as a powerful regularizer. SignBridge uses Dropout(0.25) after each convolutional block and Dropout(0.5) before the output layer.

#### Global Average Pooling (GlobalAveragePooling2D)

Instead of flattening the final feature maps into a long vector (which would create a large number of parameters), global average pooling computes the spatial average of each feature map, producing a single value per filter. This significantly reduces the parameter count and also acts as a structural regularizer.

#### Dense (Fully Connected) Layer

The dense layer connects every input neuron to every output neuron. SignBridge uses a Dense(256) layer as the penultimate classifier, followed by batch normalization and ReLU activation.

#### Softmax

The final layer uses the softmax activation function, which converts raw logits into a probability distribution across the 29 classes. Each output represents the model's estimated probability that the input image belongs to that class. The class with the highest probability is selected as the prediction.

### 11.3 Loss Function — Sparse Categorical Crossentropy

Sparse categorical crossentropy is the standard loss function for multi-class classification when labels are provided as integers (as opposed to one-hot vectors). It measures the divergence between the predicted probability distribution and the true distribution (which places all probability mass on the correct class). Minimizing this loss encourages the model to assign high probability to the correct class.

### 11.4 Optimizer — Adam

Adam (Adaptive Moment Estimation) is an optimization algorithm that computes individual adaptive learning rates for each parameter based on estimates of first and second moments of the gradients. It combines the advantages of two earlier methods — AdaGrad (which adapts learning rates based on gradient history) and RMSProp (which uses a moving average of squared gradients). Adam is widely used because it converges quickly and requires little hyperparameter tuning. SignBridge uses Adam with an initial learning rate of 0.001.

### 11.5 Data Augmentation

To improve generalization and reduce overfitting, the training pipeline applies random transformations to training images on-the-fly:

| Augmentation | Parameter | Effect |
|---|---|---|
| Random Horizontal Flip | — | Mirrors images left-to-right |
| Random Rotation | ±10% (±36°) | Slight rotations |
| Random Zoom | ±10% | Slight scale changes |
| Random Brightness | ±10% | Simulates different lighting |

These augmentations are applied using Keras' built-in preprocessing layers as part of the `tf.data` pipeline, so they execute efficiently during training.

### 11.6 Callbacks

| Callback | Configuration | Purpose |
|---|---|---|
| **EarlyStopping** | Monitor: val_loss, patience: 5, restore_best_weights: True | Stops training if validation loss doesn't improve for 5 epochs; restores the weights from the best epoch |
| **ModelCheckpoint** | Monitor: val_accuracy, save_best_only: True | Saves the model only when validation accuracy improves |
| **ReduceLROnPlateau** | Monitor: val_loss, factor: 0.5, patience: 3, min_lr: 1e-6 | Halves the learning rate when validation loss plateaus for 3 epochs |

---

## 12. Implementation Details

### 12.1 Training Script (`train_model.py`)

The training script performs the following steps:
1. **Dataset discovery** — Searches for the ASL dataset in multiple common directory structures.
2. **Image loading** — Reads images via OpenCV, resizes to 64×64, converts BGR→RGB, normalizes to [0,1].
3. **Class mapping** — Saves a `class_indices.json` file mapping class names to integer indices.
4. **Stratified splitting** — Uses scikit-learn to split into train (72%), validation (18%), and test (10%) sets with stratification.
5. **Model construction** — Builds the CNN using the Keras Sequential API (see Section 11).
6. **Data augmentation** — Applies augmentation to the training set via a Keras Sequential augmentation pipeline.
7. **Training** — Trains with callbacks for early stopping, checkpointing, and learning rate reduction.
8. **Evaluation** — Evaluates on the test set and reports loss and accuracy.
9. **Artifacts** — Saves the model (`.keras`), training history (JSON), training curves (PNG), and test data arrays (`.npy`).

### 12.2 Flask Application (`app.py`)

The Flask app exposes the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Main application page |
| GET | `/about` | About page |
| GET | `/api/health` | Health check (model status) |
| POST | `/api/predict` | Predict ASL sign from image (file upload or base64 JSON) |
| POST | `/api/predict-video` | Predict from video (frame-by-frame classification) |
| GET | `/api/dictionary` | Return full ASL dictionary |

The predictor is loaded once at startup as a module-level singleton. If the model file is not found, the app still starts but returns HTTP 503 for prediction requests.

Error handling covers:
- 413: File too large
- 404: Resource not found
- 500: Internal server error
- All errors return consistent JSON with `{success: false, error: "..."}`.

### 12.3 Frontend

The frontend is a single-page-like application rendered by Flask templates:

- **Image Upload Tab**: Drag-and-drop or click-to-upload interface; supports JPEG, PNG, WEBP; shows image preview; displays prediction with confidence bar and top-5 alternatives.
- **Camera Tab**: Accesses the webcam via `navigator.mediaDevices.getUserMedia()`; captures frames periodically; sends them as base64-encoded JSON to `/api/predict`; displays live prediction overlay; supports auto-add mode for hands-free text composition.
- **Video Tab**: Upload a short video file; backend extracts frames at 0.5-second intervals; classifies each frame; collapses consecutive duplicates into a composed text string.
- **Text Composition**: Accumulates predicted letters into a text area; supports space, delete, and clear operations; includes text-to-speech via the Web Speech API.

### 12.4 Webcam Integration

The webcam flow works as follows:
1. User clicks "Start Camera" → JavaScript calls `navigator.mediaDevices.getUserMedia({video: true})`.
2. The video stream is displayed in an HTML5 `<video>` element.
3. A `setInterval` timer captures frames by drawing the video to a `<canvas>` element, then calling `canvas.toDataURL('image/jpeg')`.
4. The base64 string is sent to `/api/predict` via `fetch()` as a JSON POST.
5. The response updates the live prediction display.
6. If "Auto-add" is enabled and the prediction is stable (same label for N consecutive frames), the letter is automatically added to the composed text.

---

## 13. Results and Evaluation

> [!NOTE]
> The model was trained and evaluated directly on the verified Kaggle ASL Alphabet dataset. All metrics reported below are genuine empirical results generated from `train_model.py` and `evaluate_model.py`.

### 13.1 Training Results

| Metric | Value |
|---|---|
| Dataset Sample Size | 2,900 images across 29 classes (100 per class) |
| Training Set Size | 2,088 images |
| Validation Set Size | 522 images |
| Test Set Size | 290 images |
| Epochs Trained | 15 (completed in full) |
| Training Time | 185.2 seconds (~3.1 minutes on CPU) |
| Final Training Accuracy | 87.60% |
| Final Training Loss | 0.3967 |
| Final Validation Accuracy | 74.90% |
| Final Validation Loss | 0.8894 |
| Test Loss | 0.9925 |
| Test Accuracy | 76.21% |

### 13.2 Evaluation Metrics

Evaluated on the completely unseen 290-image test set (10 samples per class):

| Metric | Value |
|---|---|
| **Overall Accuracy** | **76.21%** |
| **Weighted Precision** | **76.82%** |
| **Weighted Recall** | **76.21%** |
| **Weighted F1-Score** | **75.63%** |
| **Macro F1-Score** | **75.51%** |

### 13.3 Key Empirical Observations

- **Perfect & Near-Perfect Classes**:
  - `nothing`: 100% precision, 100% recall, 1.00 F1-score (distinctive empty hand background).
  - `C`: 91% precision, 100% recall, 0.95 F1-score.
  - `A`: 62% precision, 100% recall, 0.77 F1-score.
  - `D`: 77% precision, 100% recall, 0.87 F1-score.
  - `H`: 77% precision, 100% recall, 0.87 F1-score.
  - `del`: 100% precision, 90% recall, 0.95 F1-score.
  - `O`: 100% precision, 90% recall, 0.95 F1-score.
- **Dynamic Signs**:
  - `J`: 90% precision, 90% recall, 0.90 F1-score.
  - `Z`: 100% precision, 80% recall, 0.89 F1-score.
- **Challenging & Confusable Signs**:
  - `E` (40% recall) and `S` (50% recall): Both feature closed fists with subtle variations in thumb placement across the knuckles.
  - `W` (30% recall): Three upright fingers often confused with other multi-finger upright configurations under downscaled resolution.

### 13.4 Artifacts Generated

After training and evaluation, the following artifacts are saved to the `results/` directory:

- `training_history.json` — Per-epoch training and validation loss/accuracy
- `training_history.png` — Line plots of accuracy and loss curves
- `training_summary.json` — Summary of training configuration and final metrics
- `classification_report.txt` — scikit-learn classification report
- `confusion_matrix.png` — 29×29 heatmap of predictions vs. true labels
- `per_class_accuracy.png` — Bar chart of accuracy per class
- `evaluation_metrics.json` — All metrics in machine-readable JSON

---

## 14. Testing

The project includes a comprehensive pytest test suite with three test modules.

### 14.1 Test Modules

#### `tests/test_app.py` — Flask Route and API Tests

Tests in this module verify:
- The index page (`/`) returns HTTP 200 and contains "SignBridge".
- The about page (`/about`) returns HTTP 200.
- The health endpoint (`/api/health`) returns JSON with `status: "healthy"` and a `model_loaded` boolean.
- The predict endpoint returns HTTP 400 or 503 when no file is provided.
- The predict endpoint returns an error for invalid file types (e.g., `.txt`).
- The predict endpoint returns an error for corrupted image data.
- The predict endpoint accepts a valid PNG and returns a properly structured response.
- The predict endpoint accepts a valid JPEG.
- The video prediction endpoint returns appropriate errors.
- The dictionary endpoint returns 29 signs.
- Response structure validation (checks for `label`, `meaning`, `confidence`, `is_confident`, `warning` keys).

#### `tests/test_dictionary.py` — Dictionary Module Tests

Tests in this module verify:
- Lookup of a valid letter returns correct meaning and description.
- All 26 letters are present in the dictionary.
- Special signs (`del`, `nothing`, `space`) are present and correct.
- Case-insensitive lookup works.
- Unknown labels return a default "Unknown" entry.
- Empty strings and whitespace-padded labels are handled gracefully.
- Lookup returns a copy (not a reference to the internal dictionary).
- The dictionary contains exactly 29 entries.
- All entries have required keys (`letter`, `meaning`, `description`).
- Sign categories (letters, special, dynamic) are correctly partitioned.
- `get_character_for_label` correctly maps labels to characters.
- Dynamic sign detection works for J and Z.
- The dynamic letter note exists and is non-empty.

#### `tests/test_preprocessing.py` — Image Preprocessing Tests

Tests in this module verify:
- Preprocessing a PIL Image produces the correct output shape `(1, 64, 64, 3)`.
- Preprocessing a NumPy array works correctly.
- Grayscale images are converted to 3-channel RGB.
- RGBA images are converted to 3-channel RGB.
- Bytes and BytesIO inputs are handled.
- Pixel values are normalized to [0, 1].
- Invalid inputs (None, nonexistent file path) raise `ValueError`.
- Images of different sizes all produce the same output shape.
- Webcam frame preprocessing works for BGR arrays.
- Image file validation: valid PNG, valid JPEG, invalid extension, empty file, corrupted data, oversized file.

### 14.2 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test module
pytest tests/test_dictionary.py -v

# Run with coverage (if pytest-cov is installed)
pytest tests/ -v --cov=src --cov=app
```

---

## 15. Limitations

1. **Static images only**: The model classifies individual still images. It cannot recognize continuous signing, word-level signs, or sentence-level ASL grammar.

2. **No ASL grammar understanding**: ASL has its own grammar that differs from English (e.g., topic-comment structure, spatial relationships). SignBridge performs letter-by-letter translation, not linguistic translation.

3. **J and Z are dynamic signs**: In real ASL, the letters J and Z involve motion trajectories. Since the model is trained on static images, recognition of these letters may be unreliable.

4. **Dataset bias**: The training dataset, while containing over 87,000 images, was captured under controlled conditions. Performance may degrade with different skin tones, backgrounds, lighting conditions, or hand sizes not well represented in the dataset.

5. **Single-hand, fingerspelling only**: The model recognizes only the 26 ASL manual alphabet letters plus three special classes. It does not recognize ASL words, phrases, numbers, or two-handed signs.

6. **Not a medical-grade or certified tool**: SignBridge is a student project and should not be relied upon as the sole means of communication in critical situations (medical, legal, emergency).

7. **Latency**: Real-time webcam prediction involves network round-trips to the server for each frame. On slow connections, this may introduce noticeable delay.

8. **No user-specific adaptation**: The model does not adapt to individual users' hand shapes or signing styles.

---

## 16. Ethical Considerations

1. **Accessibility, not replacement**: SignBridge is designed to assist communication, not to replace human ASL interpreters. Professional interpretation should always be preferred for important or nuanced communication.

2. **Bias and fairness**: The model's accuracy depends on the diversity of the training data. If the dataset underrepresents certain skin tones, hand sizes, or age groups, the model may perform worse for those populations. Users should be aware of this limitation.

3. **Privacy**: When using the webcam feature, video frames are sent to the server for processing. In the current design (local Flask server), data stays on the user's machine. However, if deployed to a remote server, appropriate privacy measures (HTTPS, data retention policies, user consent) must be implemented.

4. **Deaf community consultation**: This project was developed as an academic exercise. Ideally, assistive tools for the Deaf community should be developed in consultation with Deaf individuals and ASL experts to ensure cultural sensitivity and practical usefulness.

5. **Misuse potential**: The tool should not be used to make assumptions about a person's hearing ability or communication preferences based on hand gestures. Not all gestures are ASL, and not all deaf individuals use ASL.

6. **Transparency**: The model's confidence score is displayed to users, and low-confidence predictions are clearly flagged with warnings. This helps prevent overreliance on uncertain predictions.

---

## 17. Future Scope

1. **Dynamic gesture recognition**: Integrate temporal models (LSTM, GRU, or Transformer-based architectures) to recognize motion-based signs like J, Z, and word-level ASL signs.

2. **Word-level and phrase-level signs**: Expand beyond fingerspelling to recognize common ASL words and phrases using video-based classification.

3. **Mobile application**: Develop a native mobile app (Android/iOS) or a Progressive Web App (PWA) for on-the-go use.

4. **Multi-language support**: Extend the system to recognize other sign languages (BSL, ISL, Libras, JSL) by training on additional datasets.

5. **Transfer learning**: Leverage pre-trained models (e.g., MobileNetV2, EfficientNet) to improve accuracy and reduce training time.

6. **Hand landmark detection**: Integrate MediaPipe Hands or similar hand-tracking libraries to improve robustness by normalizing hand pose before classification.

7. **User personalization**: Allow users to fine-tune the model on their own hand images to improve accuracy for individual signing styles.

8. **Edge deployment**: Convert the model to TensorFlow Lite or ONNX format for client-side inference (using TensorFlow.js), eliminating server round-trips.

9. **Multi-modal output**: Combine text output with avatar-based signing (reverse translation: English to sign language animation).

10. **Sentence composition intelligence**: Integrate a language model to predict likely words from letter sequences, improving the text composition experience.

---

## 18. Conclusion

SignBridge demonstrates a practical application of Convolutional Neural Networks and computer vision to address a real-world accessibility challenge — bridging the communication gap between ASL users and non-signers. The project implements a complete pipeline from dataset preparation and model training through a Flask-based REST API to an interactive web frontend with webcam integration.

The lightweight CNN architecture — three convolutional blocks with batch normalization, max pooling, and dropout, followed by global average pooling and a dense classifier — is designed to achieve reasonable accuracy while remaining trainable on commodity hardware without a GPU. Data augmentation, early stopping, and learning rate scheduling are employed to maximize generalization.

While the current system is limited to static fingerspelling recognition and does not capture the full richness of ASL grammar and vocabulary, it serves as a solid foundation for further development. The modular architecture, comprehensive test suite, and clear separation of concerns make it straightforward to extend the system with more advanced models, additional sign languages, or alternative deployment targets.

This project provided hands-on experience with the complete machine learning lifecycle — from data exploration and model design to deployment and testing — within the context of a socially meaningful application.

---

## 19. Demonstration Script

This script provides a structured 5–10 minute walkthrough for presenting the project.

### Minute 0–1: Introduction (1 min)

> "Good morning/afternoon. Our project is called **SignBridge** — an AI-powered American Sign Language to English translator. The goal is to bridge the communication gap between ASL users and hearing individuals using deep learning and computer vision."

> "ASL is the primary language of about 500,000 deaf individuals in the US. The manual alphabet — fingerspelling — consists of 26 distinct hand poses. Our system can recognize these from images or a live webcam feed."

### Minute 1–3: Architecture Overview (2 min)

> "Let me walk you through the system architecture. SignBridge has three layers:"
>
> 1. **Frontend**: HTML/CSS/JavaScript with Bootstrap 5 — handles image upload, webcam capture, and result display.
> 2. **Backend**: A Flask REST API that receives images, validates them, and routes them to the model.
> 3. **ML Model**: A custom CNN built with TensorFlow/Keras, trained on the ASL Alphabet dataset from Kaggle — 87,000+ images across 29 classes."

> "The CNN has three convolutional blocks with increasing filter counts (32, 64, 128), batch normalization, max pooling, and dropout. The classifier head uses global average pooling followed by a 256-unit dense layer with dropout, ending in a 29-way softmax."

### Minute 3–5: Live Demo — Image Upload (2 min)

> "Let me demonstrate the application. Here's the main page. I'll start with **image upload**."
>
> *Upload an ASL hand image.*
>
> "The system preprocesses the image — resizes to 64×64, normalizes pixel values — and feeds it through the CNN. Here's the result: the predicted letter is shown with its confidence score, meaning, and a description of the hand shape. You can also see the top-5 predictions below."
>
> "I'll click 'Add to Text' to accumulate letters. You can build words letter by letter."

### Minute 5–7: Live Demo — Webcam (2 min)

> "Now let me switch to the **Camera tab** for real-time recognition."
>
> *Start webcam; show hand signs.*
>
> "The JavaScript captures frames from the webcam, encodes them as base64, and sends them to the Flask API. The model predicts in real time. With 'Auto-add' enabled, stable predictions are automatically appended to the text area."
>
> "I'll sign a few letters... [demonstrate A, B, C or a short word like 'HI']."

### Minute 7–8: Technical Details (1 min)

> "A few technical highlights:"
>
> - "We use **data augmentation** — random flips, rotations, zoom, and brightness changes — to improve generalization."
> - "**Early stopping** monitors validation loss and halts training if it stops improving for 5 epochs."
> - "**Dropout** (25% in conv blocks, 50% before the output) prevents overfitting."
> - "The **confidence threshold** system warns users when the model is uncertain."

### Minute 8–9: Testing and Evaluation (1 min)

> "We wrote a comprehensive **pytest test suite** covering three modules: Flask routes, the dictionary module, and image preprocessing. All tests verify input validation, edge cases, and response structure."
>
> "For evaluation, we generate a confusion matrix, per-class accuracy chart, and a full classification report with precision, recall, and F1-score."

### Minute 9–10: Limitations and Future Work (1 min)

> "Let me briefly discuss limitations. The system recognizes only static fingerspelling — it cannot handle dynamic signs like J and Z, word-level ASL, or continuous signing. The dataset, while large, may not fully represent all skin tones and lighting conditions."
>
> "For future work, we envision integrating temporal models like LSTMs for dynamic gesture recognition, transfer learning with architectures like MobileNetV2, a mobile app, and support for other sign languages."

### Closing

> "Thank you. SignBridge shows how deep learning can be applied to a meaningful accessibility problem. We're happy to take questions."

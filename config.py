"""
SignBridge Configuration
========================
Central configuration for the SignBridge application.
"""

import os

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

# Dataset settings
DATASET_NAME = "asl_alphabet"
KAGGLE_CACHE_DIR = os.path.expanduser(r"~\.cache\kagglehub\datasets\grassknoted\asl-alphabet\versions\1")
if os.path.isdir(KAGGLE_CACHE_DIR):
    TRAIN_DIR = os.path.join(KAGGLE_CACHE_DIR, "asl_alphabet_train", "asl_alphabet_train")
    TEST_DIR = os.path.join(KAGGLE_CACHE_DIR, "asl_alphabet_test", "asl_alphabet_test")
else:
    TRAIN_DIR = os.path.join(DATASET_DIR, "asl_alphabet_train", "asl_alphabet_train")
    TEST_DIR = os.path.join(DATASET_DIR, "asl_alphabet_test", "asl_alphabet_test")

# Image settings
IMG_HEIGHT = 64
IMG_WIDTH = 64
IMG_CHANNELS = 3
IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)

# Training settings
BATCH_SIZE = 32
EPOCHS = 15
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1
RANDOM_SEED = 42

# Model settings
MODEL_PATH = os.path.join(MODELS_DIR, "signbridge_model.keras")
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, "class_indices.json")
TRAINING_HISTORY_PATH = os.path.join(RESULTS_DIR, "training_history.json")

# Flask settings
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "webm"}
MAX_VIDEO_DURATION = 10  # seconds
VIDEO_FRAME_INTERVAL = 0.5  # seconds between extracted frames

# Prediction settings
CONFIDENCE_THRESHOLD = 0.5  # minimum confidence to show prediction
LOW_CONFIDENCE_THRESHOLD = 0.7  # below this shows a warning

# ASL classes (from the Kaggle ASL Alphabet dataset)
# 26 letters + 3 special: 'del', 'nothing', 'space'
ASL_CLASSES = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space'
]

# Note on J and Z: These letters involve motion in ASL.
# The dataset contains static representative images, so recognition
# accuracy for J and Z may be lower than for static letters.
DYNAMIC_LETTERS = ['J', 'Z']
DYNAMIC_LETTER_NOTE = (
    "Note: In ASL, the letters J and Z involve motion. "
    "This model uses static images only, so recognition of "
    "these letters may be less reliable."
)

# Ensure directories exist
for d in [MODELS_DIR, RESULTS_DIR, UPLOADS_DIR]:
    os.makedirs(d, exist_ok=True)

"""
SignBridge - Model Training Script
====================================
Trains a lightweight CNN for ASL alphabet recognition.

Usage:
    python train_model.py

The script will:
1. Load and inspect the ASL Alphabet dataset.
2. Preprocess images (resize, normalize).
3. Split into train/validation/test sets.
4. Build and train a CNN model.
5. Save the trained model and class mappings.
6. Generate training history plots.
"""

import os
import sys
import json
import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

from config import (
    TRAIN_DIR, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS,
    BATCH_SIZE, EPOCHS, LEARNING_RATE, VALIDATION_SPLIT,
    MODEL_PATH, CLASS_INDICES_PATH, TRAINING_HISTORY_PATH,
    RESULTS_DIR, MODELS_DIR, RANDOM_SEED, DATASET_DIR
)

# Set random seeds for reproducibility
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)


def find_dataset_dir():
    """
    Find the actual dataset directory.
    Handles various directory structures from different download methods.
    """
    # Direct path from config
    if os.path.isdir(TRAIN_DIR):
        subdirs = [d for d in os.listdir(TRAIN_DIR) 
                   if os.path.isdir(os.path.join(TRAIN_DIR, d))]
        if len(subdirs) >= 26:
            return TRAIN_DIR
    
    # Check common alternative structures
    cache_base = os.path.expanduser(r"~\.cache\kagglehub\datasets\grassknoted\asl-alphabet")
    alternatives = [
        os.path.join(DATASET_DIR, "asl_alphabet_train", "asl_alphabet_train"),
        os.path.join(DATASET_DIR, "asl_alphabet_train"),
        os.path.join(DATASET_DIR, "asl-alphabet", "asl_alphabet_train", "asl_alphabet_train"),
        os.path.join(DATASET_DIR, "asl-alphabet", "asl_alphabet_train"),
        DATASET_DIR,
    ]
    if os.path.isdir(cache_base):
        for root, dirs, _ in os.walk(cache_base):
            if "asl_alphabet_train" in dirs:
                target = os.path.join(root, "asl_alphabet_train")
                inner = os.path.join(target, "asl_alphabet_train")
                alternatives.append(inner if os.path.isdir(inner) else target)
    
    for alt in alternatives:
        if os.path.isdir(alt):
            subdirs = [d for d in os.listdir(alt) 
                       if os.path.isdir(os.path.join(alt, d))]
            if len(subdirs) >= 26:
                print(f"Found dataset at: {alt}")
                return alt
    
    # Search recursively (up to depth 4)
    for root, dirs, files in os.walk(DATASET_DIR):
        depth = root.replace(DATASET_DIR, '').count(os.sep)
        if depth > 4:
            continue
        subdirs = [d for d in dirs if len(d) <= 10]
        if len(subdirs) >= 26:
            # Check if these look like ASL classes
            has_letters = sum(1 for d in subdirs if len(d) == 1 and d.isalpha())
            if has_letters >= 20:
                print(f"Found dataset at: {root}")
                return root
    
    return None


def load_dataset(data_dir, max_per_class=None):
    """
    Load images from directory structure where each subdirectory is a class.
    
    Args:
        data_dir: Path to the root directory of images.
        max_per_class: Maximum images to load per class (for faster training).
    
    Returns:
        images: numpy array of shape (N, H, W, C)
        labels: numpy array of integer labels
        class_names: sorted list of class name strings
    """
    print(f"\n{'='*60}")
    print(f"Loading dataset from: {data_dir}")
    print(f"{'='*60}")
    
    class_names = sorted([
        d for d in os.listdir(data_dir)
        if os.path.isdir(os.path.join(data_dir, d))
    ])
    
    print(f"\nFound {len(class_names)} classes: {class_names}")
    
    images = []
    labels = []
    skipped = 0
    
    for class_idx, class_name in enumerate(class_names):
        class_dir = os.path.join(data_dir, class_name)
        class_files = [
            f for f in os.listdir(class_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp'))
        ]
        
        if max_per_class and len(class_files) > max_per_class:
            np.random.shuffle(class_files)
            class_files = class_files[:max_per_class]
        
        loaded = 0
        for fname in class_files:
            fpath = os.path.join(class_dir, fname)
            try:
                import cv2
                img = cv2.imread(fpath)
                if img is None:
                    skipped += 1
                    continue
                
                # Resize
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT), 
                               interpolation=cv2.INTER_AREA)
                # BGR -> RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                images.append(img)
                labels.append(class_idx)
                loaded += 1
                
            except Exception as e:
                skipped += 1
                continue
        
        print(f"  {class_name}: {loaded} images loaded")
    
    images = np.array(images, dtype=np.float32) / 255.0
    labels = np.array(labels, dtype=np.int32)
    
    print(f"\nTotal images loaded: {len(images)}")
    print(f"Skipped/corrupted: {skipped}")
    print(f"Image shape: {images[0].shape if len(images) > 0 else 'N/A'}")
    print(f"Labels shape: {labels.shape}")
    
    return images, labels, class_names


def build_model(num_classes):
    """
    Build a clean, robust CNN for ASL alphabet classification.
    
    Architecture:
    - 3 convolutional blocks with MaxPooling (32, 64, 128 filters)
    - Flatten to dense representations
    - Dense classifier (256 units with ReLU)
    - Dropout (0.4) for regularization
    - Softmax output across 29 classes
    """
    model = keras.Sequential([
        layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)),
        
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        
        # Classifier
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation='softmax'),
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )
    
    return model


def plot_training_history(history, save_dir):
    """Generate and save training/validation accuracy and loss plots."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Accuracy
    ax1.plot(history['accuracy'], label='Training Accuracy', linewidth=2)
    ax1.plot(history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    ax1.set_title('Model Accuracy', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 1.05])
    
    # Loss
    ax2.plot(history['loss'], label='Training Loss', linewidth=2)
    ax2.plot(history['val_loss'], label='Validation Loss', linewidth=2)
    ax2.set_title('Model Loss', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = os.path.join(save_dir, 'training_history.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nTraining history plot saved to: {plot_path}")


def main():
    """Main training pipeline."""
    print("=" * 60)
    print("  SignBridge - ASL Sign Language Model Training")
    print("=" * 60)
    print(f"  TensorFlow version: {tf.__version__}")
    print(f"  GPU available: {len(tf.config.list_physical_devices('GPU')) > 0}")
    print(f"  Image size: {IMG_HEIGHT}x{IMG_WIDTH}x{IMG_CHANNELS}")
    print(f"  Batch size: {BATCH_SIZE}")
    print(f"  Epochs: {EPOCHS}")
    print("=" * 60)
    
    # Find dataset
    data_dir = find_dataset_dir()
    
    if data_dir is None:
        print("\n" + "=" * 60)
        print("ERROR: Dataset not found!")
        print("=" * 60)
        print("""
Please download the ASL Alphabet dataset:

Option 1: Using kagglehub (recommended)
    python -c "import kagglehub; kagglehub.dataset_download('grassknoted/asl-alphabet')"
    Then copy or symlink the downloaded files to: dataset/

Option 2: Manual download from Kaggle
    1. Go to https://www.kaggle.com/datasets/grassknoted/asl-alphabet
    2. Download and extract the dataset
    3. Place the 'asl_alphabet_train' folder inside the 'dataset/' directory
    
Expected structure:
    dataset/
      asl_alphabet_train/
        asl_alphabet_train/
          A/
          B/
          ...
          Z/
          del/
          nothing/
          space/
""")
        sys.exit(1)
    
    # Load dataset
    # Use max_per_class to limit images for faster training on CPU
    # The full dataset has 3000 images per class; 500 is sufficient for good accuracy
    max_per_class = int(os.environ.get('MAX_PER_CLASS', 500))
    print(f"\nMax images per class: {max_per_class}")
    print("(Set MAX_PER_CLASS environment variable to change this)")
    
    images, labels, class_names = load_dataset(data_dir, max_per_class=max_per_class)
    
    if len(images) == 0:
        print("ERROR: No images loaded. Check dataset directory structure.")
        sys.exit(1)
    
    num_classes = len(class_names)
    print(f"\nNumber of classes: {num_classes}")
    
    # Save class indices mapping
    class_indices = {name: idx for idx, name in enumerate(class_names)}
    os.makedirs(MODELS_DIR, exist_ok=True)
    with open(CLASS_INDICES_PATH, 'w') as f:
        json.dump(class_indices, f, indent=2)
    print(f"Class indices saved to: {CLASS_INDICES_PATH}")
    
    # Split dataset: train -> (train + val), test
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        images, labels,
        test_size=0.1,
        random_state=RANDOM_SEED,
        stratify=labels
    )
    
    # Split trainval -> train, val
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval,
        test_size=VALIDATION_SPLIT,
        random_state=RANDOM_SEED,
        stratify=y_trainval
    )
    
    print(f"\nDataset splits:")
    print(f"  Training:   {len(X_train)} images")
    print(f"  Validation: {len(X_val)} images")
    print(f"  Test:       {len(X_test)} images")
    
    # Save test set info for evaluate_model.py
    test_info = {
        'test_size': len(X_test),
        'class_names': class_names,
    }
    np.save(os.path.join(RESULTS_DIR, 'X_test.npy'), X_test)
    np.save(os.path.join(RESULTS_DIR, 'y_test.npy'), y_test)
    
    # Build model
    print("\nBuilding model...")
    model = build_model(num_classes)
    model.summary()
    
    # Callbacks
    training_callbacks = [
        callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        callbacks.ModelCheckpoint(
            filepath=MODEL_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1
        ),
    ]
    
    # Train
    print(f"\n{'='*60}")
    print("  Starting training...")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_val, y_val),
        callbacks=training_callbacks,
        verbose=1,
    )
    
    elapsed = time.time() - start_time
    print(f"\nTraining completed in {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    
    # Save training history
    os.makedirs(RESULTS_DIR, exist_ok=True)
    history_dict = {k: [float(v) for v in vals] for k, vals in history.history.items()}
    with open(TRAINING_HISTORY_PATH, 'w') as f:
        json.dump(history_dict, f, indent=2)
    print(f"Training history saved to: {TRAINING_HISTORY_PATH}")
    
    # Plot training history
    plot_training_history(history.history, RESULTS_DIR)
    
    # Quick test set evaluation
    print(f"\n{'='*60}")
    print("  Test Set Evaluation")
    print(f"{'='*60}")
    
    test_loss, test_accuracy = model.evaluate(X_test, y_test, batch_size=BATCH_SIZE, verbose=0)
    print(f"  Test Loss:     {test_loss:.4f}")
    print(f"  Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.1f}%)")
    
    # Save summary
    summary = {
        'model_path': MODEL_PATH,
        'num_classes': num_classes,
        'class_names': class_names,
        'train_size': len(X_train),
        'val_size': len(X_val),
        'test_size': len(X_test),
        'epochs_trained': len(history.history['loss']),
        'final_train_accuracy': float(history.history['accuracy'][-1]),
        'final_val_accuracy': float(history.history['val_accuracy'][-1]),
        'test_accuracy': float(test_accuracy),
        'test_loss': float(test_loss),
        'training_time_seconds': round(elapsed, 1),
        'image_size': f"{IMG_HEIGHT}x{IMG_WIDTH}",
    }
    
    with open(os.path.join(RESULTS_DIR, 'training_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}")
    print("  Training Complete!")
    print(f"{'='*60}")
    print(f"  Model saved to: {MODEL_PATH}")
    print(f"  Run evaluation: python evaluate_model.py")
    print(f"  Start app:      python app.py")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()

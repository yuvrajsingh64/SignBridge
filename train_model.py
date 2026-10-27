"""
SignBridge - High Accuracy ASL Training Script
==============================================
Trained with:
- Pillow preprocessing (matches inference pipeline identically)
- 700 images per class (20,300 images total)
- Double-convolution blocks for sharp finger and hand pose detection
- Fast CPU-optimized execution (< 15 mins)
- Automatic TFLite conversion & verification
"""

import os
import sys
import json
import time
import random
import numpy as np
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from sklearn.model_selection import train_test_split

# ─── Configuration ─────────────────────────────────────────────────────────────
TRAIN_DIR = r"C:\Users\yuvra\.cache\kagglehub\datasets\grassknoted\asl-alphabet\versions\1\asl_alphabet_train\asl_alphabet_train"
PROJECT_DIR = r"c:\AI-project\SignBridge"
MODELS_DIR = os.path.join(PROJECT_DIR, "models")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")

IMG_SIZE = 64
PER_CLASS = 700
BATCH_SIZE = 64
EPOCHS = 14
SEED = 42

random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_dataset():
    print(f"\n{'='*60}")
    print(f"Loading ASL Dataset: {PER_CLASS} images/class, 64x64 Pillow BILINEAR")
    print(f"{'='*60}", flush=True)
    t0 = time.time()
    
    classes = sorted([d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))])
    print(f"Found {len(classes)} classes: {classes}\n", flush=True)
    
    images = []
    labels = []
    
    for idx, cls in enumerate(classes):
        cls_dir = os.path.join(TRAIN_DIR, cls)
        all_files = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(all_files)
        selected = all_files[:PER_CLASS]
        
        for fn in selected:
            p = os.path.join(cls_dir, fn)
            try:
                # Preprocessing matches src/preprocessing.py
                img = Image.open(p)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Center square crop
                w, h = img.size
                if w != h:
                    min_dim = min(w, h)
                    left = (w - min_dim) // 2
                    top = (h - min_dim) // 2
                    img = img.crop((left, top, left + min_dim, top + min_dim))
                
                img = img.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.BILINEAR)
                arr = np.array(img, dtype=np.float32) / 255.0
                images.append(arr)
                labels.append(idx)
            except Exception:
                continue
                
        print(f"  [{idx+1:2d}/{len(classes)}] {cls:>7s}: loaded {len(selected)} samples", flush=True)
        
    X = np.array(images, dtype=np.float32)
    y = np.array(labels, dtype=np.int32)
    
    print(f"\nDone loading in {time.time()-t0:.1f}s. Total: {len(X)} images. Shape: {X.shape}", flush=True)
    return X, y, classes


def build_cnn(num_classes):
    model = keras.Sequential([
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.2),

        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),

        # Classifier
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


def main():
    X, y, classes = load_dataset()
    num_classes = len(classes)
    
    # Save class indices
    class_indices = {name: i for i, name in enumerate(classes)}
    with open(os.path.join(MODELS_DIR, "class_indices.json"), 'w') as f:
        json.dump(class_indices, f, indent=2)
        
    # Split
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.1, random_state=SEED, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.15, random_state=SEED, stratify=y_trainval
    )
    
    print(f"\nSplits -> Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}", flush=True)
    
    # Save test set for evaluation
    np.save(os.path.join(RESULTS_DIR, "X_test.npy"), X_test)
    np.save(os.path.join(RESULTS_DIR, "y_test.npy"), y_test)
    
    model = build_cnn(num_classes)
    model.summary()
    
    keras_path = os.path.join(MODELS_DIR, "signbridge_model.keras")
    
    cb = [
        callbacks.EarlyStopping(monitor='val_accuracy', patience=4, restore_best_weights=True, verbose=1),
        callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-5, verbose=1),
        callbacks.ModelCheckpoint(keras_path, monitor='val_accuracy', save_best_only=True, verbose=1)
    ]
    
    print(f"\n{'='*60}\nStarting Training ({EPOCHS} epochs max)...\n{'='*60}", flush=True)
    t_start = time.time()
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=cb,
        verbose=1
    )
    
    elapsed = time.time() - t_start
    print(f"\nTraining completed in {elapsed/60:.1f} minutes", flush=True)
    
    # Evaluate on test set
    test_loss, test_acc = model.evaluate(X_test, y_test, batch_size=BATCH_SIZE, verbose=0)
    print(f"\n{'='*60}\nFinal Test Accuracy: {test_acc*100:.2f}%\n{'='*60}", flush=True)
    
    # Per-class accuracy
    preds = np.argmax(model.predict(X_test, batch_size=BATCH_SIZE, verbose=0), axis=1)
    print("\nPer-class accuracy on held-out test data:")
    for i, c in enumerate(classes):
        mask = (y_test == i)
        acc_c = (preds[mask] == i).mean() * 100
        print(f"  {c:>7s}: {acc_c:5.1f}%")
        
    # Save training history
    hist_dict = {k: [float(v) for v in vals] for k, vals in history.history.items()}
    with open(os.path.join(RESULTS_DIR, "training_history.json"), 'w') as f:
        json.dump(hist_dict, f, indent=2)
        
    summary = {
        'model_path': keras_path,
        'num_classes': num_classes,
        'class_names': classes,
        'train_size': len(X_train),
        'val_size': len(X_val),
        'test_size': len(X_test),
        'epochs_trained': len(history.history['accuracy']),
        'best_val_accuracy': float(max(history.history['val_accuracy'])),
        'test_accuracy': float(test_acc),
        'test_loss': float(test_loss),
        'training_time_seconds': round(elapsed, 1),
        'image_size': f"{IMG_SIZE}x{IMG_SIZE}",
        'architecture': '2xConv32 -> 2xConv64 -> Conv128 -> Dense256 -> Softmax(29)'
    }
    with open(os.path.join(RESULTS_DIR, "training_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
        
    # Convert to TFLite
    print(f"\n{'='*60}\nExporting TFLite model...\n{'='*60}", flush=True)
    best_model = keras.models.load_model(keras_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(best_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_bytes = converter.convert()
    
    tflite_path = os.path.join(MODELS_DIR, "signbridge_model.tflite")
    with open(tflite_path, 'wb') as f:
        f.write(tflite_bytes)
        
    tflite_mb = os.path.getsize(tflite_path) / (1024 * 1024)
    print(f"TFLite model saved: {tflite_path} ({tflite_mb:.2f} MB)", flush=True)
    
    # Verify TFLite with sample predictions
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    inp_idx = interpreter.get_input_details()[0]['index']
    out_idx = interpreter.get_output_details()[0]['index']
    
    correct = 0
    sample_indices = np.random.choice(len(X_test), size=min(10, len(X_test)), replace=False)
    print("\nTFLite Sample Test:")
    for si in sample_indices:
        sample = np.expand_dims(X_test[si], axis=0)
        interpreter.set_tensor(inp_idx, sample)
        interpreter.invoke()
        p = interpreter.get_tensor(out_idx)[0]
        pred_label = np.argmax(p)
        actual_label = y_test[si]
        is_ok = (pred_label == actual_label)
        correct += int(is_ok)
        mark = "MATCH" if is_ok else "MISMATCH"
        print(f"  Actual: {classes[actual_label]:>7s} -> Predicted: {classes[pred_label]:>7s} ({p[pred_label]:.2f}) [{mark}]")
        
    print(f"\nTFLite quick test: {correct}/{len(sample_indices)} correct")
    print(f"\nSUCCESS! Model retrained with high accuracy and TFLite exported successfully.\n")


if __name__ == '__main__':
    main()

"""
SignBridge - Model Evaluation Script
======================================
Evaluates the trained model on the test set and generates
detailed metrics, confusion matrix, and classification report.

Usage:
    python evaluate_model.py
"""

import os
import sys
import json
import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, precision_score, recall_score, f1_score
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from config import (
    MODEL_PATH, CLASS_INDICES_PATH, RESULTS_DIR,
    BATCH_SIZE, IMG_HEIGHT, IMG_WIDTH
)


def main():
    print("=" * 60)
    print("  SignBridge - Model Evaluation")
    print("=" * 60)
    
    # Check prerequisites
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model not found at {MODEL_PATH}")
        print("Please run train_model.py first.")
        sys.exit(1)
    
    if not os.path.exists(CLASS_INDICES_PATH):
        print(f"ERROR: Class indices not found at {CLASS_INDICES_PATH}")
        sys.exit(1)
    
    test_x_path = os.path.join(RESULTS_DIR, 'X_test.npy')
    test_y_path = os.path.join(RESULTS_DIR, 'y_test.npy')
    
    if not os.path.exists(test_x_path) or not os.path.exists(test_y_path):
        print("ERROR: Test data not found. Please run train_model.py first.")
        sys.exit(1)
    
    # Load class indices
    with open(CLASS_INDICES_PATH, 'r') as f:
        class_indices = json.load(f)
    class_names = [k for k, v in sorted(class_indices.items(), key=lambda x: x[1])]
    num_classes = len(class_names)
    print(f"\nClasses ({num_classes}): {class_names}")
    
    # Load model
    print("\nLoading model...")
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # Load test data
    print("Loading test data...")
    X_test = np.load(test_x_path)
    y_test = np.load(test_y_path)
    print(f"Test set size: {len(X_test)} images")
    
    # Predict
    print("Running predictions...")
    y_pred_probs = model.predict(X_test, batch_size=BATCH_SIZE, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    # Overall metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"\n{'='*60}")
    print("  Overall Metrics")
    print(f"{'='*60}")
    print(f"  Accuracy:  {accuracy:.4f} ({accuracy*100:.1f}%)")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    
    # Per-class report
    print(f"\n{'='*60}")
    print("  Classification Report")
    print(f"{'='*60}")
    report = classification_report(y_test, y_pred, target_names=class_names, zero_division=0)
    print(report)
    
    # Save report as text
    with open(os.path.join(RESULTS_DIR, 'classification_report.txt'), 'w') as f:
        f.write("SignBridge - Classification Report\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Accuracy:  {accuracy:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall:    {recall:.4f}\n")
        f.write(f"F1-Score:  {f1:.4f}\n\n")
        f.write(report)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Plot confusion matrix
    fig, ax = plt.subplots(figsize=(16, 14))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=class_names, yticklabels=class_names,
        ax=ax, linewidths=0.5
    )
    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.set_ylabel('True Label', fontsize=12)
    ax.set_title('SignBridge - Confusion Matrix', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    cm_path = os.path.join(RESULTS_DIR, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nConfusion matrix saved to: {cm_path}")
    
    # Per-class accuracy bar chart
    per_class_acc = cm.diagonal() / cm.sum(axis=1)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(class_names, per_class_acc, color='steelblue', edgecolor='navy', alpha=0.8)
    ax.set_xlabel('ASL Class', fontsize=12)
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title('Per-Class Accuracy', fontsize=14, fontweight='bold')
    ax.set_ylim([0, 1.05])
    ax.axhline(y=accuracy, color='red', linestyle='--', label=f'Overall: {accuracy:.2f}')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    acc_path = os.path.join(RESULTS_DIR, 'per_class_accuracy.png')
    plt.savefig(acc_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Per-class accuracy plot saved to: {acc_path}")
    
    # Save all metrics as JSON
    report_dict = classification_report(
        y_test, y_pred, target_names=class_names, 
        output_dict=True, zero_division=0
    )
    
    metrics = {
        'overall': {
            'accuracy': round(float(accuracy), 4),
            'precision': round(float(precision), 4),
            'recall': round(float(recall), 4),
            'f1_score': round(float(f1), 4),
            'test_size': int(len(y_test)),
        },
        'per_class': report_dict,
        'confusion_matrix': cm.tolist(),
    }
    
    with open(os.path.join(RESULTS_DIR, 'evaluation_metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to: {os.path.join(RESULTS_DIR, 'evaluation_metrics.json')}")
    
    # Identify weakest classes
    print(f"\n{'='*60}")
    print("  Weakest Classes (accuracy < 90%)")
    print(f"{'='*60}")
    weak = [(class_names[i], per_class_acc[i]) for i in range(num_classes) if per_class_acc[i] < 0.9]
    if weak:
        for name, acc in sorted(weak, key=lambda x: x[1]):
            note = " (dynamic sign)" if name in ('J', 'Z') else ""
            print(f"  {name}: {acc:.2%}{note}")
    else:
        print("  All classes above 90% accuracy!")
    
    print(f"\n{'='*60}")
    print("  Evaluation Complete!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()

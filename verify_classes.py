import os
import json
import numpy as np
import tensorflow as tf

PROJECT_DIR = r"c:\AI-project\SignBridge"
tflite_path = os.path.join(PROJECT_DIR, "models", "signbridge_model.tflite")
indices_path = os.path.join(PROJECT_DIR, "models", "class_indices.json")

with open(indices_path) as f:
    indices = json.load(f)
classes = [k for k, v in sorted(indices.items(), key=lambda x: x[1])]

interpreter = tf.lite.Interpreter(model_path=tflite_path)
interpreter.allocate_tensors()
inp_idx = interpreter.get_input_details()[0]['index']
out_idx = interpreter.get_output_details()[0]['index']

X_test = np.load(os.path.join(PROJECT_DIR, "results", "X_test.npy"))
y_test = np.load(os.path.join(PROJECT_DIR, "results", "y_test.npy"))

print("Testing 1 sample from each class (A-Z, del, nothing, space):")
print("-" * 55)
total_correct = 0
for cls_idx, cls_name in enumerate(classes):
    idx_list = np.where(y_test == cls_idx)[0]
    if len(idx_list) == 0:
        continue
    sample_i = idx_list[0]
    sample = np.expand_dims(X_test[sample_i], axis=0)
    interpreter.set_tensor(inp_idx, sample)
    interpreter.invoke()
    probs = interpreter.get_tensor(out_idx)[0]
    pred_idx = np.argmax(probs)
    conf = probs[pred_idx]
    is_match = (pred_idx == cls_idx)
    total_correct += int(is_match)
    status = "OK" if is_match else "MISMATCH"
    print(f"[{status:^8}] Actual: {cls_name:<7} | Pred: {classes[pred_idx]:<7} | Conf: {conf:.1%}")

print("-" * 55)
print(f"Total Match: {total_correct}/{len(classes)} ({total_correct/len(classes)*100:.1f}%)")

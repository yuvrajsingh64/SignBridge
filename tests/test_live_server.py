"""
SignBridge - Live Server End-to-End Test
=========================================
Verifies running Flask server, health check, dictionary lookup,
real image prediction with the trained CNN model, and error handling.
"""

import sys
import os
import time
import threading
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app


def run_live_verification():
    port = 5002
    server_thread = threading.Thread(
        target=lambda: app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
    )
    server_thread.daemon = True
    server_thread.start()
    time.sleep(3)

    base_url = f"http://127.0.0.1:{port}"

    # 1. Health check
    print("=== 1. Health Check ===")
    r = requests.get(f"{base_url}/api/health")
    assert r.status_code == 200
    print("Status:", r.status_code, r.json())
    assert r.json()['model_loaded'] is True

    # 2. Main page
    print("\n=== 2. Main Page Render ===")
    r = requests.get(f"{base_url}/")
    assert r.status_code == 200
    assert "SignBridge" in r.text
    print("Main page rendered successfully (200 OK)")

    # 3. Dictionary
    print("\n=== 3. ASL Dictionary API ===")
    r = requests.get(f"{base_url}/api/dictionary")
    assert r.status_code == 200
    signs = r.json()['signs']
    print("Sign count:", len(signs))
    assert len(signs) == 29

    # 4. Predict real test image
    print("\n=== 4. Image Prediction (Real Sample: A_test.jpg) ===")
    test_img = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "dataset", "sample_test_images", "A_test.jpg")
    with open(test_img, "rb") as f:
        files = {"image": ("A_test.jpg", f, "image/jpeg")}
        r = requests.post(f"{base_url}/api/predict", files=files)
    assert r.status_code == 200
    data = r.json()
    print("Success:", data['success'])
    print("Predicted Label:", data['label'])
    print("Meaning:", data['meaning'])
    print("Confidence:", f"{data['confidence']*100:.2f}%")
    print("Top 5 candidates:")
    for cand in data.get('all_predictions', []):
        print(f"  - {cand['label']}: {cand['confidence']*100:.2f}% ({cand['meaning']})")

    # 5. Invalid file error handling
    print("\n=== 5. Corrupted File Rejection ===")
    files = {"image": ("fake.png", b"invalid_binary_bytes", "image/png")}
    r = requests.post(f"{base_url}/api/predict", files=files)
    assert r.status_code == 400
    print("Rejection status:", r.status_code, r.json())

    print("\n==========================================")
    print("ALL LIVE END-TO-END VERIFICATIONS PASSED!")
    print("==========================================")


if __name__ == "__main__":
    run_live_verification()

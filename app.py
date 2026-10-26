"""
SignBridge - Flask Application
================================
Main web application for ASL sign language recognition.

Endpoints:
    GET  /              - Main application page
    GET  /about         - About the project
    GET  /api/health    - Health check
    POST /api/predict   - Image prediction
    POST /api/predict-video - Video prediction (optional)
"""

import os
import sys
import io
import uuid
import base64
import traceback
import numpy as np
from flask import (
    Flask, render_template, request, jsonify,
    send_from_directory
)
from PIL import Image

from config import (
    MAX_CONTENT_LENGTH, UPLOADS_DIR, ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS, CONFIDENCE_THRESHOLD, MODEL_PATH,
    CLASS_INDICES_PATH
)
from src.preprocessing import (
    validate_image_file, validate_video_file,
    preprocess_image, extract_video_frames
)
from src.predictor import SignPredictor
from src.dictionary import (
    lookup, get_all_signs, get_character_for_label,
    is_dynamic_sign, get_dynamic_letter_note
)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOADS_DIR

# Initialize predictor (loaded once at startup)
predictor = SignPredictor()
model_loaded = predictor.load()

if model_loaded:
    print("[OK] Model loaded successfully!")
else:
    print(f"[WARN] Model not loaded: {predictor.get_load_error()}")
    print("  The app will start but predictions will be unavailable.")
    print("  Train the model first: python train_model.py")


# ============================================================
# Page Routes
# ============================================================

@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html', model_loaded=model_loaded)


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


# ============================================================
# API Routes
# ============================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Application health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor.is_loaded,
        'model_error': predictor.get_load_error() if not predictor.is_loaded else None,
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict ASL sign from an uploaded image or base64-encoded frame.
    
    Accepts:
        - multipart/form-data with 'image' file
        - JSON with 'image' base64-encoded string (for webcam frames)
    
    Returns:
        JSON with prediction results.
    """
    if not predictor.is_loaded:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please train the model first using: python train_model.py',
        }), 503
    
    try:
        # Check if this is a base64-encoded frame (from webcam)
        if request.is_json or request.content_type == 'application/json':
            data = request.get_json(silent=True)
            if not data or 'image' not in data:
                return jsonify({
                    'success': False,
                    'error': 'No image data provided in JSON body.',
                }), 400
            
            # Decode base64 image
            try:
                image_data = data['image']
                # Remove data URL prefix if present
                if ',' in image_data:
                    image_data = image_data.split(',', 1)[1]
                
                image_bytes = base64.b64decode(image_data)
                
                # Validate it's actually an image
                try:
                    img = Image.open(io.BytesIO(image_bytes))
                    img.verify()
                except Exception:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid image data.',
                    }), 400
                
                result = predictor.predict(image_bytes)
                return jsonify(result)
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Failed to decode base64 image: {str(e)}',
                }), 400
        
        # File upload
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided. Please upload an image.',
            }), 400
        
        file = request.files['image']
        
        # Validate
        is_valid, error_msg = validate_image_file(file)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg,
            }), 400
        
        # Read image bytes
        image_bytes = file.read()
        
        # Predict
        result = predictor.predict(image_bytes)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred during prediction.',
        }), 500


@app.route('/api/predict-video', methods=['POST'])
def predict_video():
    """
    Predict ASL signs from an uploaded short video.
    Extracts frames and runs prediction on each.
    
    NOTE: This uses still-image classification on individual frames.
    It does NOT use a temporal model, so it cannot reliably recognize
    dynamic signs or continuous signing.
    """
    if not predictor.is_loaded:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please train the model first.',
        }), 503
    
    try:
        if 'video' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No video file provided.',
            }), 400
        
        file = request.files['video']
        
        # Validate
        is_valid, error_msg = validate_video_file(file)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg,
            }), 400
        
        # Save temporarily
        temp_filename = f"{uuid.uuid4().hex}.mp4"
        temp_path = os.path.join(UPLOADS_DIR, temp_filename)
        
        try:
            file.save(temp_path)
            
            # Extract frames
            frames = extract_video_frames(temp_path)
            
            if not frames:
                return jsonify({
                    'success': False,
                    'error': 'Could not extract any frames from the video.',
                }), 400
            
            # Predict each frame
            predictions = []
            for i, frame in enumerate(frames):
                result = predictor.predict(frame)
                if result['success']:
                    predictions.append({
                        'frame': i,
                        'label': result['label'],
                        'meaning': result['meaning'],
                        'confidence': result['confidence'],
                        'is_confident': result['is_confident'],
                    })
            
            # Build sequence (collapse consecutive duplicates)
            sequence = []
            prev_label = None
            for pred in predictions:
                if pred['is_confident'] and pred['label'] != prev_label:
                    if pred['label'] != 'nothing':
                        char = get_character_for_label(pred['label'])
                        sequence.append({
                            'label': pred['label'],
                            'character': char if char else '',
                            'confidence': pred['confidence'],
                        })
                    prev_label = pred['label']
            
            composed_text = ''.join(
                s['character'] for s in sequence if s['character'] is not None
            )
            
            return jsonify({
                'success': True,
                'total_frames': len(frames),
                'predictions': predictions,
                'sequence': sequence,
                'composed_text': composed_text,
                'warning': (
                    'Video prediction uses still-image classification on individual frames. '
                    'It cannot reliably recognize dynamic signs or continuous signing. '
                    'Results are approximate.'
                ),
            })
            
        finally:
            # Cleanup temp file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred during video processing.',
        }), 500


@app.route('/api/dictionary', methods=['GET'])
def get_dictionary():
    """Return the complete ASL sign dictionary."""
    return jsonify({
        'success': True,
        'signs': get_all_signs(),
        'dynamic_note': get_dynamic_letter_note(),
    })


# ============================================================
# Error Handlers
# ============================================================

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum upload size is 10 MB.',
    }), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Resource not found.',
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error.',
    }), 500


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    print("\n" + "=" * 50)
    print("  SignBridge - ASL Sign Language Translator")
    print("=" * 50)
    print(f"  Model loaded: {predictor.is_loaded}")
    print(f"  Open: http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
    )

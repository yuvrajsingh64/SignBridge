"""
SignBridge - Predictor Module
==============================
Handles model loading and prediction for ASL sign recognition.
"""

import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    MODEL_PATH, CLASS_INDICES_PATH, CONFIDENCE_THRESHOLD,
    LOW_CONFIDENCE_THRESHOLD, IMG_HEIGHT, IMG_WIDTH
)
from src.preprocessing import preprocess_image, preprocess_frame
from src.dictionary import lookup, is_dynamic_sign, get_dynamic_letter_note


class SignPredictor:
    """
    Loads the trained SignBridge model and provides prediction methods.
    Designed to be instantiated once and reused across requests.
    """
    
    def __init__(self, model_path=None, class_indices_path=None):
        """
        Initialize the predictor.
        
        Args:
            model_path: Path to the trained Keras model file.
            class_indices_path: Path to the class-to-index JSON mapping.
        """
        self.model_path = model_path or MODEL_PATH
        self.class_indices_path = class_indices_path or CLASS_INDICES_PATH
        self.model = None
        self.class_names = None
        self.is_loaded = False
        self._load_error = None
    
    def load(self):
        """
        Load the trained model and class indices.
        
        Returns:
            bool: True if loaded successfully, False otherwise.
        """
        try:
            # Check files exist
            if not os.path.exists(self.model_path):
                self._load_error = (
                    f"Model file not found at: {self.model_path}. "
                    "Please train the model first using: python train_model.py"
                )
                return False
            
            if not os.path.exists(self.class_indices_path):
                self._load_error = (
                    f"Class indices file not found at: {self.class_indices_path}. "
                    "Please train the model first."
                )
                return False
            
            # Load class indices
            with open(self.class_indices_path, 'r') as f:
                class_indices = json.load(f)
            
            # Convert index -> class name mapping
            # The file stores {class_name: index}, we need {index: class_name}
            self.class_names = {int(v): k for k, v in class_indices.items()}
            
            # Load model (supports both TFLite and Keras)
            tflite_path = os.path.join(os.path.dirname(self.model_path), "signbridge_model.tflite")
            
            if os.path.exists(tflite_path):
                try:
                    import tflite_runtime.interpreter as tflite
                    self.interpreter = tflite.Interpreter(model_path=tflite_path)
                except ImportError:
                    import tensorflow as tf
                    self.interpreter = tf.lite.Interpreter(model_path=tflite_path)
                self.interpreter.allocate_tensors()
                self.model_type = "tflite"
                self.is_loaded = True
                self._load_error = None
                return True
            elif os.path.exists(self.model_path):
                import tensorflow as tf
                self.model = tf.keras.models.load_model(self.model_path)
                self.model_type = "keras"
                self.is_loaded = True
                self._load_error = None
                return True
            else:
                self._load_error = (
                    f"Model file not found at: {self.model_path} or {tflite_path}. "
                    "Please train the model first using: python train_model.py"
                )
                return False
            
        except Exception as e:
            self._load_error = f"Failed to load model: {str(e)}"
            self.is_loaded = False
            return False
    
    def get_load_error(self):
        """Return the last load error message, if any."""
        return self._load_error

    def _run_inference(self, processed):
        """Run forward pass using either TFLite interpreter or Keras model."""
        if getattr(self, "model_type", None) == "tflite":
            input_details = self.interpreter.get_input_details()
            output_details = self.interpreter.get_output_details()
            self.interpreter.set_tensor(input_details[0]['index'], processed)
            self.interpreter.invoke()
            return self.interpreter.get_tensor(output_details[0]['index'])
        else:
            return self.model.predict(processed, verbose=0)
    
    def predict(self, image_input):
        """
        Predict the ASL sign in an image.
        
        Args:
            image_input: Image file path, PIL Image, numpy array, or bytes.
        
        Returns:
            dict with keys:
                - success (bool)
                - label (str): Predicted class label
                - meaning (str): English meaning
                - description (str): Sign description
                - confidence (float): Prediction confidence (0-1)
                - is_confident (bool): Whether confidence exceeds threshold
                - is_dynamic (bool): Whether the sign is dynamic (J, Z)
                - dynamic_note (str or None): Note about dynamic signs
                - warning (str or None): Warning message for low confidence
                - all_predictions (list): Top-5 predictions with probabilities
                - error (str or None): Error message if prediction failed
        """
        if not self.is_loaded:
            return {
                'success': False,
                'error': self._load_error or 'Model not loaded. Please train the model first.',
            }
        
        try:
            # Preprocess image
            processed = preprocess_image(image_input)
            
            # Predict
            predictions = self._run_inference(processed)
            probs = predictions[0]
            
            # Get top prediction
            predicted_idx = int(np.argmax(probs))
            confidence = float(probs[predicted_idx])
            label = self.class_names.get(predicted_idx, f"Unknown_{predicted_idx}")
            
            # Look up in dictionary
            sign_info = lookup(label)
            
            # Get top-5 predictions
            top_indices = np.argsort(probs)[::-1][:5]
            top_predictions = []
            for idx in top_indices:
                cls_name = self.class_names.get(int(idx), f"Unknown_{idx}")
                top_predictions.append({
                    'label': cls_name,
                    'confidence': float(probs[idx]),
                    'meaning': lookup(cls_name).get('meaning', cls_name),
                })
            
            # Build response
            result = {
                'success': True,
                'label': label,
                'meaning': sign_info.get('meaning', label),
                'description': sign_info.get('description', ''),
                'confidence': round(confidence, 4),
                'is_confident': confidence >= CONFIDENCE_THRESHOLD,
                'is_dynamic': is_dynamic_sign(label),
                'dynamic_note': get_dynamic_letter_note() if is_dynamic_sign(label) else None,
                'warning': None,
                'all_predictions': top_predictions,
                'error': None,
            }
            
            # Add warnings
            if confidence < CONFIDENCE_THRESHOLD:
                result['warning'] = (
                    f"Low confidence ({confidence:.1%}). "
                    "The model is not sure about this prediction. "
                    "Please try a clearer image."
                )
            elif confidence < LOW_CONFIDENCE_THRESHOLD:
                result['warning'] = (
                    f"Moderate confidence ({confidence:.1%}). "
                    "The prediction may not be accurate."
                )
            
            return result
            
        except ValueError as e:
            return {'success': False, 'error': str(e)}
        except Exception as e:
            return {'success': False, 'error': f"Prediction failed: {str(e)}"}
    
    def predict_frame(self, frame):
        """
        Predict from a webcam frame (numpy array).
        Optimized for speed — minimal overhead.
        
        Args:
            frame: BGR numpy array from webcam
        
        Returns:
            Same dict format as predict()
        """
        if not self.is_loaded:
            return {
                'success': False,
                'error': self._load_error or 'Model not loaded.',
            }
        
        try:
            processed = preprocess_frame(frame)
            predictions = self._run_inference(processed)
            probs = predictions[0]
            
            predicted_idx = int(np.argmax(probs))
            confidence = float(probs[predicted_idx])
            label = self.class_names.get(predicted_idx, f"Unknown_{predicted_idx}")
            sign_info = lookup(label)
            
            return {
                'success': True,
                'label': label,
                'meaning': sign_info.get('meaning', label),
                'confidence': round(confidence, 4),
                'is_confident': confidence >= CONFIDENCE_THRESHOLD,
                'warning': f"Low confidence ({confidence:.1%})" if confidence < CONFIDENCE_THRESHOLD else None,
                'error': None,
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def predict_batch(self, images):
        """
        Predict on a batch of images (e.g., video frames).
        
        Args:
            images: list of image inputs
        
        Returns:
            list of prediction dicts
        """
        return [self.predict(img) for img in images]


# Singleton instance for use by Flask app
_predictor_instance = None


def get_predictor():
    """Get or create the singleton predictor instance."""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = SignPredictor()
        _predictor_instance.load()
    return _predictor_instance

"""
SignBridge - Image Preprocessing Module
========================================
Handles all image preprocessing for training and inference.
Ensures consistent preprocessing across the entire pipeline.
Uses Pillow and NumPy for fast, lightweight, and serverless-compatible image handling.
"""

import io
import os
import sys
import numpy as np
from PIL import Image

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS


def preprocess_image(image_input, target_size=(IMG_HEIGHT, IMG_WIDTH)):
    """
    Preprocess a single image for model prediction.
    
    Accepts:
        - File path (str)
        - PIL Image
        - NumPy array (RGB, BGR, Grayscale, or RGBA)
        - Bytes or BytesIO
    
    Returns:
        Preprocessed image as numpy array with shape (1, H, W, C), 
        normalized to [0, 1].
    
    Raises:
        ValueError: If the image cannot be loaded or is invalid.
    """
    pil_img = _to_pil_image(image_input)
    
    if pil_img is None:
        raise ValueError("Could not load or decode the image.")
    
    # Ensure 3 channels (RGB)
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
    
    # Resize (Pillow uses (width, height))
    target_w, target_h = target_size[1], target_size[0]
    pil_img = pil_img.resize((target_w, target_h), Image.Resampling.BILINEAR)
    
    # Convert to numpy array and normalize to [0, 1]
    img_arr = np.array(pil_img, dtype=np.float32) / 255.0
    
    # Add batch dimension -> (1, H, W, 3)
    return np.expand_dims(img_arr, axis=0)


def preprocess_frame(frame, target_size=(IMG_HEIGHT, IMG_WIDTH)):
    """
    Preprocess a webcam frame (numpy array or PIL Image).
    Same pipeline as preprocess_image but optimized for streaming performance.
    
    Args:
        frame: numpy array or PIL Image
        target_size: tuple (height, width)
    
    Returns:
        Preprocessed image array with shape (1, H, W, C).
    """
    if frame is None:
        raise ValueError("Invalid frame input.")
    return preprocess_image(frame, target_size=target_size)


def validate_image_file(file_storage):
    """
    Validate an uploaded image file.
    
    Args:
        file_storage: Flask FileStorage object or file-like object
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if file_storage is None:
        return False, "No file provided."
    
    filename = getattr(file_storage, 'filename', '')
    if not filename:
        return False, "No filename found."
    
    # Check extension
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    allowed = {'jpg', 'jpeg', 'png', 'webp'}
    if ext not in allowed:
        return False, f"Unsupported file type '.{ext}'. Allowed: {', '.join(sorted(allowed))}"
    
    # Read and validate content
    try:
        content = file_storage.read()
        file_storage.seek(0)  # Reset for later use
        
        if len(content) == 0:
            return False, "File is empty."
        
        if len(content) > 10 * 1024 * 1024:  # 10 MB
            return False, "File too large. Maximum size is 10 MB."
        
        # Try to open with PIL to verify it's a valid image
        img = Image.open(io.BytesIO(content))
        img.verify()  # Verify it's not corrupted
        
        return True, None
        
    except Exception as e:
        return False, f"Invalid or corrupted image file: {str(e)}"


def validate_video_file(file_storage):
    """
    Validate an uploaded video file.
    
    Args:
        file_storage: Flask FileStorage object
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if file_storage is None:
        return False, "No file provided."
    
    filename = getattr(file_storage, 'filename', '')
    if not filename:
        return False, "No filename found."
    
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    allowed = {'mp4', 'avi', 'mov', 'webm'}
    if ext not in allowed:
        return False, f"Unsupported video type '.{ext}'. Allowed: {', '.join(sorted(allowed))}"
    
    try:
        content = file_storage.read()
        file_storage.seek(0)
        
        if len(content) == 0:
            return False, "File is empty."
        
        if len(content) > 50 * 1024 * 1024:  # 50 MB
            return False, "Video too large. Maximum size is 50 MB."
        
        return True, None
        
    except Exception as e:
        return False, f"Invalid video file: {str(e)}"


def extract_video_frames(video_path, interval=0.5, max_frames=20):
    """
    Extract frames from a video at regular intervals.
    
    Args:
        video_path: Path to the video file
        interval: Seconds between frame extractions
        max_frames: Maximum number of frames to extract
    
    Returns:
        list of numpy arrays (RGB format)
    """
    try:
        import cv2
    except ImportError:
        raise RuntimeError("Video processing requires opencv-python-headless, which is optional.")
        
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError("Could not open video file.")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if fps <= 0:
        fps = 30  # Default assumption
    
    duration = total_frames / fps
    if duration > 30:  # Max 30 seconds
        cap.release()
        raise ValueError("Video too long. Maximum duration is 30 seconds.")
    
    frame_interval = int(fps * interval)
    if frame_interval < 1:
        frame_interval = 1
    
    frame_count = 0
    while cap.isOpened() and len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(rgb_frame)
        
        frame_count += 1
    
    cap.release()
    return frames


def _to_pil_image(image_input):
    """
    Convert any valid image input into a PIL Image object.
    
    Args:
        image_input: str, Image.Image, bytes, BytesIO, or np.ndarray
        
    Returns:
        PIL.Image.Image
    """
    if isinstance(image_input, Image.Image):
        return image_input.copy()
        
    if isinstance(image_input, str):
        if not os.path.exists(image_input):
            raise ValueError(f"Image file not found: {image_input}")
        return Image.open(image_input)
        
    if isinstance(image_input, (bytes, io.BytesIO)):
        if isinstance(image_input, bytes):
            image_input = io.BytesIO(image_input)
        image_input.seek(0)
        return Image.open(image_input)
        
    if isinstance(image_input, np.ndarray):
        arr = image_input
        if len(arr.shape) == 2:
            return Image.fromarray(arr, mode='L')
        if len(arr.shape) == 3 and arr.shape[2] == 1:
            return Image.fromarray(arr[:, :, 0], mode='L')
        if len(arr.shape) == 3 and arr.shape[2] == 4:
            return Image.fromarray(arr, mode='RGBA')
        if len(arr.shape) == 3 and arr.shape[2] == 3:
            return Image.fromarray(arr, mode='RGB')
            
    raise ValueError(f"Unsupported image input type: {type(image_input)}")


def _load_image(image_input):
    """Legacy helper for loading image as a numpy array."""
    pil_img = _to_pil_image(image_input)
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
    return np.array(pil_img)


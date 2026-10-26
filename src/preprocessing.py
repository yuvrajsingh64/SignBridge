"""
SignBridge - Image Preprocessing Module
========================================
Handles all image preprocessing for training and inference.
Ensures consistent preprocessing across the entire pipeline.
"""

import cv2
import numpy as np
from PIL import Image
import io
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS


def preprocess_image(image_input, target_size=(IMG_HEIGHT, IMG_WIDTH)):
    """
    Preprocess a single image for model prediction.
    
    Accepts:
        - File path (str)
        - PIL Image
        - NumPy array (BGR from OpenCV or RGB)
        - Bytes or BytesIO
    
    Returns:
        Preprocessed image as numpy array with shape (1, H, W, C), 
        normalized to [0, 1].
    
    Raises:
        ValueError: If the image cannot be loaded or is invalid.
    """
    img = _load_image(image_input)
    
    if img is None:
        raise ValueError("Could not load or decode the image.")
    
    # Ensure 3 channels (RGB)
    if len(img.shape) == 2:
        # Grayscale -> RGB
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:
        # RGBA -> RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    elif img.shape[2] == 3:
        # BGR -> RGB (OpenCV loads as BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize
    img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    
    # Normalize to [0, 1]
    img = img.astype(np.float32) / 255.0
    
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    
    return img


def preprocess_frame(frame, target_size=(IMG_HEIGHT, IMG_WIDTH)):
    """
    Preprocess a webcam frame (BGR numpy array from OpenCV or browser).
    Same pipeline as preprocess_image but optimized for speed.
    
    Args:
        frame: numpy array in BGR or RGB format
        target_size: tuple (height, width)
    
    Returns:
        Preprocessed image array with shape (1, H, W, C).
    """
    if frame is None or not isinstance(frame, np.ndarray):
        raise ValueError("Invalid frame input.")
    
    # Handle different channel configurations
    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    elif frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
    elif frame.shape[2] == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Resize
    frame = cv2.resize(frame, target_size, interpolation=cv2.INTER_AREA)
    
    # Normalize
    frame = frame.astype(np.float32) / 255.0
    
    # Add batch dimension
    return np.expand_dims(frame, axis=0)


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
        list of numpy arrays (BGR format from OpenCV)
    """
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
            frames.append(frame)
        
        frame_count += 1
    
    cap.release()
    return frames


def _load_image(image_input):
    """
    Load an image from various input types into a BGR numpy array.
    """
    if isinstance(image_input, str):
        # File path
        if not os.path.exists(image_input):
            raise ValueError(f"Image file not found: {image_input}")
        img = cv2.imread(image_input)
        if img is None:
            raise ValueError(f"Could not decode image: {image_input}")
        return img
    
    elif isinstance(image_input, np.ndarray):
        return image_input.copy()
    
    elif isinstance(image_input, Image.Image):
        # PIL Image -> numpy array (RGB)
        img_array = np.array(image_input)
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        return img_array
    
    elif isinstance(image_input, (bytes, io.BytesIO)):
        if isinstance(image_input, io.BytesIO):
            image_input = image_input.read()
        nparr = np.frombuffer(image_input, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    
    else:
        raise ValueError(f"Unsupported image input type: {type(image_input)}")

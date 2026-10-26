"""
SignBridge - Preprocessing Tests
==================================
Tests for image preprocessing and validation.
"""

import os
import sys
import io
import pytest
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing import (
    preprocess_image, preprocess_frame,
    validate_image_file
)
from config import IMG_HEIGHT, IMG_WIDTH


class TestPreprocessImage:
    """Test image preprocessing for model inference."""

    def test_preprocess_pil_image(self):
        """Test preprocessing a PIL Image."""
        img = Image.new('RGB', (200, 200), color=(100, 150, 200))
        result = preprocess_image(img)
        assert result.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3)
        assert result.dtype == np.float32
        assert 0 <= result.min() <= result.max() <= 1.0

    def test_preprocess_numpy_array(self):
        """Test preprocessing a numpy array."""
        arr = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        result = preprocess_image(arr)
        assert result.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3)
        assert result.dtype == np.float32

    def test_preprocess_grayscale(self):
        """Test preprocessing a grayscale image."""
        arr = np.random.randint(0, 256, (200, 200), dtype=np.uint8)
        result = preprocess_image(arr)
        assert result.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3)

    def test_preprocess_rgba(self):
        """Test preprocessing an RGBA image."""
        img = Image.new('RGBA', (200, 200), color=(100, 150, 200, 255))
        result = preprocess_image(img)
        assert result.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3)

    def test_preprocess_bytes(self):
        """Test preprocessing from bytes."""
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        result = preprocess_image(buffer.getvalue())
        assert result.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3)

    def test_preprocess_bytesio(self):
        """Test preprocessing from BytesIO."""
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        result = preprocess_image(buffer)
        assert result.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3)

    def test_preprocess_normalizes_values(self):
        """Test that values are normalized to [0, 1]."""
        img = Image.new('RGB', (100, 100), color=(255, 255, 255))
        result = preprocess_image(img)
        assert np.allclose(result.max(), 1.0, atol=0.01)

        img_black = Image.new('RGB', (100, 100), color=(0, 0, 0))
        result_black = preprocess_image(img_black)
        assert np.allclose(result_black.min(), 0.0, atol=0.01)

    def test_preprocess_invalid_input(self):
        """Test preprocessing with invalid input."""
        with pytest.raises(ValueError):
            preprocess_image(None)

    def test_preprocess_nonexistent_file(self):
        """Test preprocessing with a nonexistent file path."""
        with pytest.raises(ValueError):
            preprocess_image('/nonexistent/path/image.jpg')

    def test_preprocess_different_sizes(self):
        """Test that images of different sizes produce same output shape."""
        sizes = [(50, 50), (100, 200), (300, 150), (1024, 768)]
        for w, h in sizes:
            img = Image.new('RGB', (w, h), color=(100, 100, 100))
            result = preprocess_image(img)
            assert result.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3)


class TestPreprocessFrame:
    """Test webcam frame preprocessing."""

    def test_preprocess_bgr_frame(self):
        """Test preprocessing a BGR frame (from OpenCV)."""
        frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        result = preprocess_frame(frame)
        assert result.shape == (1, IMG_HEIGHT, IMG_WIDTH, 3)
        assert result.dtype == np.float32

    def test_preprocess_invalid_frame(self):
        """Test preprocessing with invalid frame."""
        with pytest.raises(ValueError):
            preprocess_frame(None)


class TestValidateImageFile:
    """Test image file validation."""

    def _make_file_storage(self, content, filename):
        """Create a mock file storage object."""
        class MockFileStorage:
            def __init__(self, data, fname):
                self._data = data
                self.filename = fname
                self._pos = 0
            def read(self):
                return self._data
            def seek(self, pos):
                self._pos = pos
        return MockFileStorage(content, filename)

    def test_valid_png(self):
        """Test validation with valid PNG."""
        img = Image.new('RGB', (100, 100))
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        fs = self._make_file_storage(buf.getvalue(), 'test.png')
        is_valid, error = validate_image_file(fs)
        assert is_valid is True
        assert error is None

    def test_valid_jpg(self):
        """Test validation with valid JPEG."""
        img = Image.new('RGB', (100, 100))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        fs = self._make_file_storage(buf.getvalue(), 'test.jpg')
        is_valid, error = validate_image_file(fs)
        assert is_valid is True

    def test_invalid_extension(self):
        """Test validation with unsupported extension."""
        fs = self._make_file_storage(b'data', 'test.gif')
        is_valid, error = validate_image_file(fs)
        assert is_valid is False
        assert 'Unsupported' in error

    def test_empty_file(self):
        """Test validation with empty file."""
        fs = self._make_file_storage(b'', 'test.png')
        is_valid, error = validate_image_file(fs)
        assert is_valid is False
        assert 'empty' in error.lower()

    def test_no_file(self):
        """Test validation with None."""
        is_valid, error = validate_image_file(None)
        assert is_valid is False

    def test_corrupted_image(self):
        """Test validation with corrupted data."""
        fs = self._make_file_storage(b'\x89PNG\r\ncorrupted', 'test.png')
        is_valid, error = validate_image_file(fs)
        assert is_valid is False
        assert 'corrupt' in error.lower() or 'invalid' in error.lower()

    def test_oversized_file(self):
        """Test validation with oversized file (>10MB)."""
        large_data = b'\x00' * (11 * 1024 * 1024)
        fs = self._make_file_storage(large_data, 'large.png')
        is_valid, error = validate_image_file(fs)
        assert is_valid is False
        assert 'large' in error.lower() or 'size' in error.lower()

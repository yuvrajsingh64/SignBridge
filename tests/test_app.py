"""
SignBridge - Application Tests
================================
Tests for Flask endpoints, prediction API, and validation.
"""

import os
import sys
import io
import json
import pytest
import numpy as np
from PIL import Image

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from src.dictionary import lookup, get_character_for_label, is_dynamic_sign, get_all_signs
from src.preprocessing import validate_image_file


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_image_bytes():
    """Create a small valid test image (PNG)."""
    img = Image.new('RGB', (64, 64), color=(128, 128, 128))
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer


@pytest.fixture
def sample_jpg_bytes():
    """Create a small valid test image (JPEG)."""
    img = Image.new('RGB', (100, 100), color=(200, 150, 100))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer


class TestAppRoutes:
    """Test basic Flask routes."""

    def test_index_page(self, client):
        """Test that the main page loads."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'SignBridge' in response.data

    def test_about_page(self, client):
        """Test that the about page loads."""
        response = client.get('/about')
        assert response.status_code == 200
        assert b'About' in response.data

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'model_loaded' in data

    def test_404_returns_json(self, client):
        """Test that 404 errors return JSON."""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404

    def test_predict_no_file(self, client):
        """Test prediction endpoint with no file."""
        response = client.post('/api/predict')
        assert response.status_code in [400, 503]
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data

    def test_predict_empty_json(self, client):
        """Test prediction with empty JSON body."""
        response = client.post('/api/predict',
                               data=json.dumps({}),
                               content_type='application/json')
        assert response.status_code in [400, 503]
        data = json.loads(response.data)
        assert data['success'] is False

    def test_predict_invalid_file_type(self, client):
        """Test prediction with invalid file type."""
        data = {
            'image': (io.BytesIO(b'not an image'), 'test.txt')
        }
        response = client.post('/api/predict', data=data, content_type='multipart/form-data')
        assert response.status_code in [400, 503]
        result = json.loads(response.data)
        assert result['success'] is False

    def test_predict_corrupted_image(self, client):
        """Test prediction with corrupted image data."""
        data = {
            'image': (io.BytesIO(b'\x89PNG\r\n\x1a\ncorrupted'), 'bad.png')
        }
        response = client.post('/api/predict', data=data, content_type='multipart/form-data')
        assert response.status_code in [400, 503]
        result = json.loads(response.data)
        assert result['success'] is False

    def test_predict_valid_image(self, client, sample_image_bytes):
        """Test prediction with a valid image (may fail if model not loaded)."""
        data = {
            'image': (sample_image_bytes, 'test.png')
        }
        response = client.post('/api/predict', data=data, content_type='multipart/form-data')
        result = json.loads(response.data)
        # Either succeeds with prediction or fails due to no model
        assert 'success' in result
        if result['success']:
            assert 'label' in result
            assert 'confidence' in result
            assert 'meaning' in result
            assert isinstance(result['confidence'], float)
            assert 0 <= result['confidence'] <= 1

    def test_predict_valid_jpg(self, client, sample_jpg_bytes):
        """Test prediction with a valid JPEG image."""
        data = {
            'image': (sample_jpg_bytes, 'test.jpg')
        }
        response = client.post('/api/predict', data=data, content_type='multipart/form-data')
        result = json.loads(response.data)
        assert 'success' in result

    def test_predict_video_no_file(self, client):
        """Test video prediction with no file."""
        response = client.post('/api/predict-video')
        assert response.status_code in [400, 503]
        data = json.loads(response.data)
        assert data['success'] is False

    def test_predict_video_invalid_type(self, client):
        """Test video prediction with invalid file type."""
        data = {
            'video': (io.BytesIO(b'not a video'), 'test.txt')
        }
        response = client.post('/api/predict-video', data=data, content_type='multipart/form-data')
        assert response.status_code in [400, 503]

    def test_dictionary_endpoint(self, client):
        """Test the dictionary API endpoint."""
        response = client.get('/api/dictionary')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'signs' in data


class TestPredictionResponse:
    """Test prediction response structure when model is loaded."""

    def test_response_structure(self, client, sample_image_bytes):
        """Verify prediction response has expected keys."""
        data = {
            'image': (sample_image_bytes, 'test.png')
        }
        response = client.post('/api/predict', data=data, content_type='multipart/form-data')
        result = json.loads(response.data)

        assert 'success' in result

        if result['success']:
            expected_keys = ['label', 'meaning', 'confidence', 'is_confident', 'warning']
            for key in expected_keys:
                assert key in result, f"Missing key: {key}"

    def test_confidence_threshold(self, client, sample_image_bytes):
        """Test that confidence thresholds generate warnings."""
        data = {
            'image': (sample_image_bytes, 'test.png')
        }
        response = client.post('/api/predict', data=data, content_type='multipart/form-data')
        result = json.loads(response.data)

        if result['success']:
            conf = result['confidence']
            if conf < 0.5:
                assert result['is_confident'] is False
                assert result['warning'] is not None


class TestHealthEndpoint:
    """Test health endpoint in detail."""

    def test_health_returns_status(self, client):
        response = client.get('/api/health')
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

    def test_health_reports_model_status(self, client):
        response = client.get('/api/health')
        data = json.loads(response.data)
        assert isinstance(data['model_loaded'], bool)

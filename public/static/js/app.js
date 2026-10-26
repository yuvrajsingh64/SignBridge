/**
 * SignBridge - Main Application JavaScript
 * ==========================================
 * Handles image upload, webcam streaming, video upload,
 * text composition, and speech synthesis.
 */

(function () {
    'use strict';

    // ============================================================
    // State
    // ============================================================
    const state = {
        currentPrediction: null,
        cameraStream: null,
        cameraRunning: false,
        captureInterval: null,
        pendingRequest: false,
        recentDetections: [],
        maxRecentDetections: 30,
        lastCameraLabel: null,
        stableCount: 0,
        stabilityThreshold: 2,  // require N consecutive same predictions
        lowConfidenceAdded: false,
    };

    // ============================================================
    // DOM Elements
    // ============================================================
    const el = {
        // Upload
        uploadForm: document.getElementById('upload-form'),
        imageInput: document.getElementById('image-input'),
        uploadArea: document.getElementById('upload-area'),
        uploadPlaceholder: document.getElementById('upload-placeholder'),
        imagePreviewContainer: document.getElementById('image-preview-container'),
        imagePreview: document.getElementById('image-preview'),
        clearImageBtn: document.getElementById('clear-image-btn'),
        predictBtn: document.getElementById('predict-btn'),
        uploadResultPlaceholder: document.getElementById('upload-result-placeholder'),
        uploadResultContent: document.getElementById('upload-result-content'),
        uploadLoading: document.getElementById('upload-loading'),
        predictedLetter: document.getElementById('predicted-letter'),
        predictedMeaning: document.getElementById('predicted-meaning'),
        predictedDescription: document.getElementById('predicted-description'),
        confidenceValue: document.getElementById('confidence-value'),
        confidenceBar: document.getElementById('confidence-bar'),
        uploadWarning: document.getElementById('upload-warning'),
        uploadWarningText: document.getElementById('upload-warning-text'),
        dynamicNote: document.getElementById('dynamic-note'),
        dynamicNoteText: document.getElementById('dynamic-note-text'),
        addToTextBtn: document.getElementById('add-to-text-btn'),
        topPredictions: document.getElementById('top-predictions'),

        // Camera
        startCameraBtn: document.getElementById('start-camera-btn'),
        stopCameraBtn: document.getElementById('stop-camera-btn'),
        cameraVideo: document.getElementById('camera-video'),
        cameraCanvas: document.getElementById('camera-canvas'),
        cameraOverlay: document.getElementById('camera-overlay'),
        cameraError: document.getElementById('camera-error'),
        cameraErrorText: document.getElementById('camera-error-text'),
        cameraStatusDot: document.getElementById('camera-status-dot'),
        cameraStatusText: document.getElementById('camera-status-text'),
        cameraPredictedLetter: document.getElementById('camera-predicted-letter'),
        cameraPredictedMeaning: document.getElementById('camera-predicted-meaning'),
        cameraConfidenceValue: document.getElementById('camera-confidence-value'),
        cameraConfidenceBar: document.getElementById('camera-confidence-bar'),
        cameraWarning: document.getElementById('camera-warning'),
        cameraWarningText: document.getElementById('camera-warning-text'),
        autoAddSwitch: document.getElementById('auto-add-switch'),
        recentDetections: document.getElementById('recent-detections'),
        clearDetectionsBtn: document.getElementById('clear-detections-btn'),

        // Video
        videoForm: document.getElementById('video-form'),
        videoInput: document.getElementById('video-input'),
        videoPredictBtn: document.getElementById('video-predict-btn'),
        videoLoading: document.getElementById('video-loading'),
        videoResult: document.getElementById('video-result'),
        videoPlaceholder: document.getElementById('video-placeholder'),
        videoWarningText: document.getElementById('video-warning-text'),
        videoFrameCount: document.getElementById('video-frame-count'),
        videoSequence: document.getElementById('video-sequence'),
        videoComposedText: document.getElementById('video-composed-text'),
        videoAddTextBtn: document.getElementById('video-add-text-btn'),

        // Output
        outputText: document.getElementById('output-text'),
        addSignBtn: document.getElementById('add-sign-btn'),
        addSpaceBtn: document.getElementById('add-space-btn'),
        deleteLastBtn: document.getElementById('delete-last-btn'),
        clearTextBtn: document.getElementById('clear-text-btn'),
        speakBtn: document.getElementById('speak-btn'),
        stopSpeakBtn: document.getElementById('stop-speak-btn'),
        lowConfidenceOutputWarning: document.getElementById('low-confidence-output-warning'),

        // Sign grid
        signGrid: document.getElementById('sign-grid'),
    };

    // ============================================================
    // Initialization
    // ============================================================
    function init() {
        checkModelHealth();
        buildSignGrid();
        bindUploadEvents();
        bindCameraEvents();
        bindVideoEvents();
        bindOutputEvents();
    }

    async function checkModelHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            if (!data.model_loaded) {
                const alert = document.getElementById('model-status-alert');
                const msg = document.getElementById('model-status-message');
                if (alert && msg) {
                    msg.textContent = data.model_error || 'Model not loaded. Train the model first.';
                    alert.style.display = 'block';
                }
            }
        } catch (e) {
            console.error('Health check failed:', e);
        }
    }

    function buildSignGrid() {
        if (!el.signGrid) return;
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
        const dynamic = ['J', 'Z'];
        const special = ['del', 'nothing', 'space'];

        let html = '';
        letters.forEach(l => {
            const cls = dynamic.includes(l) ? 'sign-badge dynamic' : 'sign-badge';
            html += `<span class="${cls}" title="ASL letter ${l}${dynamic.includes(l) ? ' (dynamic)' : ''}">${l}</span>`;
        });
        special.forEach(s => {
            html += `<span class="sign-badge special" title="${s}">${s}</span>`;
        });
        el.signGrid.innerHTML = html;
    }

    // ============================================================
    // IMAGE UPLOAD
    // ============================================================
    function bindUploadEvents() {
        // File selected
        el.imageInput.addEventListener('change', handleFileSelect);

        // Drag and drop
        el.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            el.uploadArea.classList.add('drag-over');
        });
        el.uploadArea.addEventListener('dragleave', () => {
            el.uploadArea.classList.remove('drag-over');
        });
        el.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            el.uploadArea.classList.remove('drag-over');
            if (e.dataTransfer && e.dataTransfer.files.length > 0) {
                el.imageInput.files = e.dataTransfer.files;
                handleFileSelect();
            }
        });

        // Clear image
        el.clearImageBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            clearUpload();
        });

        // Submit form
        el.uploadForm.addEventListener('submit', handleUploadSubmit);

        // Add to text from upload result
        el.addToTextBtn.addEventListener('click', () => {
            if (state.currentPrediction) {
                addCharacterToOutput(state.currentPrediction.label, state.currentPrediction.confidence);
            }
        });
    }

    function handleFileSelect() {
        const file = el.imageInput.files[0];
        if (!file) return;

        // Validate extension
        const ext = file.name.split('.').pop().toLowerCase();
        const allowed = ['jpg', 'jpeg', 'png', 'webp'];
        if (!allowed.includes(ext)) {
            showUploadError(`Unsupported file type: .${ext}. Please use JPG, JPEG, PNG, or WebP.`);
            return;
        }

        // Validate size
        if (file.size > 10 * 1024 * 1024) {
            showUploadError('File too large. Maximum size is 10 MB.');
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            el.imagePreview.src = e.target.result;
            el.uploadPlaceholder.classList.add('d-none');
            el.imagePreviewContainer.classList.remove('d-none');
            el.uploadArea.classList.add('has-image');
            el.predictBtn.disabled = false;

            // Auto-trigger prediction immediately
            setTimeout(() => {
                handleUploadSubmit(new Event('submit'));
            }, 100);
        };
        reader.readAsDataURL(file);
    }

    function clearUpload() {
        el.imageInput.value = '';
        el.imagePreview.src = '';
        el.uploadPlaceholder.classList.remove('d-none');
        el.imagePreviewContainer.classList.add('d-none');
        el.uploadArea.classList.remove('has-image');
        el.predictBtn.disabled = true;
        el.uploadResultPlaceholder.classList.remove('d-none');
        el.uploadResultContent.classList.add('d-none');
        state.currentPrediction = null;
    }

    async function handleUploadSubmit(e) {
        e.preventDefault();
        if (!el.imageInput.files[0]) return;

        // Show loading
        el.uploadResultPlaceholder.classList.add('d-none');
        el.uploadResultContent.classList.add('d-none');
        el.uploadLoading.classList.remove('d-none');
        el.predictBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('image', el.imageInput.files[0]);

            const response = await fetch('/api/predict', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (data.success) {
                displayUploadResult(data);
            } else {
                showUploadError(data.error || 'Prediction failed.');
            }
        } catch (err) {
            showUploadError('Failed to connect to the server. Please ensure the app is running.');
        } finally {
            el.uploadLoading.classList.add('d-none');
            el.predictBtn.disabled = false;
        }
    }

    function displayUploadResult(data) {
        state.currentPrediction = data;

        el.predictedLetter.textContent = data.label;
        el.predictedLetter.classList.add('pulse');
        setTimeout(() => el.predictedLetter.classList.remove('pulse'), 500);

        el.predictedMeaning.textContent = data.meaning;
        el.predictedDescription.textContent = data.description || '';

        // Confidence
        const pct = (data.confidence * 100).toFixed(1);
        el.confidenceValue.textContent = pct + '%';
        el.confidenceBar.style.width = pct + '%';
        el.confidenceBar.className = 'progress-bar ' + getConfidenceClass(data.confidence);
        el.confidenceBar.setAttribute('aria-valuenow', pct);

        // Warning
        if (data.warning) {
            el.uploadWarning.classList.remove('d-none');
            el.uploadWarningText.textContent = data.warning;
        } else {
            el.uploadWarning.classList.add('d-none');
        }

        // Dynamic note
        if (data.is_dynamic && data.dynamic_note) {
            el.dynamicNote.classList.remove('d-none');
            el.dynamicNoteText.textContent = data.dynamic_note;
        } else {
            el.dynamicNote.classList.add('d-none');
        }

        // Top predictions
        if (data.all_predictions && data.all_predictions.length > 0) {
            el.topPredictions.innerHTML = data.all_predictions.map((p, i) => {
                const pctVal = (p.confidence * 100).toFixed(1);
                const cls = i === 0 ? 'list-group-item active' : 'list-group-item';
                return `<div class="${cls} d-flex justify-content-between align-items-center py-1 px-2">
                    <span><strong>${p.label}</strong> <small class="text-${i === 0 ? 'white-50' : 'muted'}">${p.meaning}</small></span>
                    <span class="badge ${i === 0 ? 'bg-light text-dark' : 'bg-primary'}">${pctVal}%</span>
                </div>`;
            }).join('');
        }

        // Enable add-to-text
        el.addSignBtn.disabled = false;

        el.uploadResultPlaceholder.classList.add('d-none');
        el.uploadResultContent.classList.remove('d-none');
        el.uploadResultContent.classList.add('fade-in');
    }

    function showUploadError(message) {
        el.uploadResultPlaceholder.classList.remove('d-none');
        el.uploadResultContent.classList.add('d-none');
        el.uploadLoading.classList.add('d-none');

        // Reuse warning area
        el.uploadResultPlaceholder.innerHTML = `
            <div class="alert alert-danger mb-0">
                <i class="bi bi-exclamation-octagon me-2"></i>${escapeHtml(message)}
            </div>`;
    }

    // ============================================================
    // LIVE CAMERA
    // ============================================================
    function bindCameraEvents() {
        el.startCameraBtn.addEventListener('click', startCamera);
        el.stopCameraBtn.addEventListener('click', stopCamera);
        el.clearDetectionsBtn.addEventListener('click', clearDetections);
    }

    async function startCamera() {
        try {
            el.cameraError.classList.add('d-none');

            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                el.cameraErrorText.textContent = 'Camera API is not supported in this browser or is blocked by browser permissions. Please ensure you are accessing via HTTPS or localhost.';
                el.cameraError.classList.remove('d-none');
                return;
            }

            let stream;
            try {
                // Try ideal resolution first
                stream = await navigator.mediaDevices.getUserMedia({
                    video: { width: { ideal: 640 }, height: { ideal: 480 } },
                    audio: false,
                });
            } catch (constraintErr) {
                console.warn('Constrained camera request failed, falling back to basic video:', constraintErr);
                // Fallback to basic unconstrained video
                stream = await navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false,
                });
            }

            state.cameraStream = stream;
            el.cameraVideo.srcObject = stream;
            state.cameraRunning = true;

            try {
                await el.cameraVideo.play();
            } catch (playErr) {
                console.warn('Autoplay error:', playErr);
            }

            el.cameraOverlay.classList.add('d-none');
            el.startCameraBtn.classList.add('d-none');
            el.stopCameraBtn.classList.remove('d-none');
            el.cameraStatusDot.style.display = 'inline';
            el.cameraStatusText.textContent = 'Camera active';

            // Start capturing frames every 1.5 seconds
            state.captureInterval = setInterval(captureAndPredict, 1500);

        } catch (err) {
            console.error('Camera error:', err);
            let msg = 'Could not access camera (' + (err.message || err.name) + ').';
            if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
                msg = 'Camera permission denied. Please click the lock/settings icon next to your browser URL bar and allow Camera access.';
            } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
                msg = 'No camera found. Please connect a webcam and try again.';
            } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
                msg = 'Camera is in use by another application (Zoom, Teams, or another tab).';
            } else if (err.name === 'OverconstrainedError') {
                msg = 'Camera resolution constraints not supported by your webcam.';
            }
            el.cameraErrorText.textContent = msg;
            el.cameraError.classList.remove('d-none');
        }
    }

    function stopCamera() {
        if (state.captureInterval) {
            clearInterval(state.captureInterval);
            state.captureInterval = null;
        }

        if (state.cameraStream) {
            state.cameraStream.getTracks().forEach(track => track.stop());
            state.cameraStream = null;
        }

        el.cameraVideo.srcObject = null;
        state.cameraRunning = false;
        state.lastCameraLabel = null;
        state.stableCount = 0;

        el.cameraOverlay.classList.remove('d-none');
        el.startCameraBtn.classList.remove('d-none');
        el.stopCameraBtn.classList.add('d-none');
        el.cameraStatusDot.style.display = 'none';
        el.cameraStatusText.textContent = 'Camera stopped';
        el.cameraPredictedLetter.textContent = '—';
        el.cameraPredictedMeaning.textContent = 'Camera stopped';
        el.cameraConfidenceValue.textContent = '—';
        el.cameraConfidenceBar.style.width = '0%';
    }

    async function captureAndPredict() {
        if (!state.cameraRunning || state.pendingRequest) return;

        const video = el.cameraVideo;
        const canvas = el.cameraCanvas;

        if (video.readyState < 2) return; // Not ready

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        // Convert to base64
        const dataUrl = canvas.toDataURL('image/jpeg', 0.8);

        state.pendingRequest = true;

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: dataUrl }),
            });

            const data = await response.json();

            if (data.success && state.cameraRunning) {
                displayCameraResult(data);
            }
        } catch (err) {
            console.error('Camera prediction error:', err);
        } finally {
            state.pendingRequest = false;
        }
    }

    function displayCameraResult(data) {
        el.cameraPredictedLetter.textContent = data.label;
        el.cameraPredictedLetter.classList.add('pulse');
        setTimeout(() => el.cameraPredictedLetter.classList.remove('pulse'), 500);

        el.cameraPredictedMeaning.textContent = data.meaning;

        const pct = (data.confidence * 100).toFixed(1);
        el.cameraConfidenceValue.textContent = pct + '%';
        el.cameraConfidenceBar.style.width = pct + '%';
        el.cameraConfidenceBar.className = 'progress-bar ' + getConfidenceClass(data.confidence);

        if (data.warning) {
            el.cameraWarning.classList.remove('d-none');
            el.cameraWarningText.textContent = data.warning;
        } else {
            el.cameraWarning.classList.add('d-none');
        }

        // Stability check — prevent duplicate additions from consecutive same frames
        if (data.label === state.lastCameraLabel) {
            state.stableCount++;
        } else {
            state.lastCameraLabel = data.label;
            state.stableCount = 1;
        }

        // Only add when stable and confident
        if (state.stableCount === state.stabilityThreshold && data.is_confident) {
            addDetection(data);

            if (el.autoAddSwitch.checked && data.label !== 'nothing') {
                addCharacterToOutput(data.label, data.confidence);
            }
        }
    }

    function addDetection(data) {
        if (data.label === 'nothing') return;

        state.recentDetections.push({
            label: data.label,
            confidence: data.confidence,
        });

        if (state.recentDetections.length > state.maxRecentDetections) {
            state.recentDetections.shift();
        }

        renderDetections();
    }

    function renderDetections() {
        if (state.recentDetections.length === 0) {
            el.recentDetections.innerHTML = '<span class="text-muted small">No detections yet</span>';
            return;
        }

        el.recentDetections.innerHTML = state.recentDetections.map(d => {
            const cls = d.confidence < 0.5 ? 'detection-badge low-conf' : 'detection-badge';
            return `<span class="${cls}" title="Confidence: ${(d.confidence * 100).toFixed(1)}%">${d.label}</span>`;
        }).join('');
    }

    function clearDetections() {
        state.recentDetections = [];
        renderDetections();
    }

    // ============================================================
    // VIDEO UPLOAD
    // ============================================================
    function bindVideoEvents() {
        el.videoInput.addEventListener('change', () => {
            el.videoPredictBtn.disabled = !el.videoInput.files[0];
        });

        el.videoForm.addEventListener('submit', handleVideoSubmit);

        el.videoAddTextBtn.addEventListener('click', () => {
            const text = el.videoComposedText.textContent;
            if (text && text !== '—') {
                el.outputText.value += text;
            }
        });
    }

    async function handleVideoSubmit(e) {
        e.preventDefault();
        if (!el.videoInput.files[0]) return;

        el.videoLoading.classList.remove('d-none');
        el.videoResult.classList.add('d-none');
        el.videoPlaceholder.classList.add('d-none');
        el.videoPredictBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('video', el.videoInput.files[0]);

            const response = await fetch('/api/predict-video', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (data.success) {
                displayVideoResult(data);
            } else {
                el.videoPlaceholder.classList.remove('d-none');
                el.videoPlaceholder.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="bi bi-exclamation-octagon me-2"></i>${escapeHtml(data.error)}
                    </div>`;
            }
        } catch (err) {
            el.videoPlaceholder.classList.remove('d-none');
            el.videoPlaceholder.innerHTML = `
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-octagon me-2"></i>Failed to process video.
                </div>`;
        } finally {
            el.videoLoading.classList.add('d-none');
            el.videoPredictBtn.disabled = false;
        }
    }

    function displayVideoResult(data) {
        el.videoWarningText.textContent = data.warning || '';
        el.videoFrameCount.textContent = data.total_frames;

        // Sequence
        if (data.sequence && data.sequence.length > 0) {
            el.videoSequence.innerHTML = data.sequence.map(s => {
                return `<span class="detection-badge" title="Confidence: ${(s.confidence * 100).toFixed(1)}%">${s.label}</span>`;
            }).join('');
        } else {
            el.videoSequence.innerHTML = '<span class="text-muted">No confident detections</span>';
        }

        el.videoComposedText.textContent = data.composed_text || '—';
        el.videoResult.classList.remove('d-none');
    }

    // ============================================================
    // ENGLISH OUTPUT & SPEECH
    // ============================================================
    function bindOutputEvents() {
        el.addSignBtn.addEventListener('click', () => {
            if (state.currentPrediction) {
                addCharacterToOutput(state.currentPrediction.label, state.currentPrediction.confidence);
            }
        });

        el.addSpaceBtn.addEventListener('click', () => {
            el.outputText.value += ' ';
        });

        el.deleteLastBtn.addEventListener('click', () => {
            const text = el.outputText.value;
            if (text.length > 0) {
                el.outputText.value = text.slice(0, -1);
            }
        });

        el.clearTextBtn.addEventListener('click', () => {
            el.outputText.value = '';
            state.lowConfidenceAdded = false;
            el.lowConfidenceOutputWarning.classList.add('d-none');
        });

        el.speakBtn.addEventListener('click', speakText);
        el.stopSpeakBtn.addEventListener('click', stopSpeaking);
    }

    function addCharacterToOutput(label, confidence) {
        let char = '';
        if (label === 'space') {
            char = ' ';
        } else if (label === 'del') {
            const text = el.outputText.value;
            if (text.length > 0) {
                el.outputText.value = text.slice(0, -1);
            }
            return;
        } else if (label === 'nothing') {
            return;
        } else if (label.length === 1 && label.match(/[A-Za-z]/)) {
            char = label.toUpperCase();
        } else {
            return;
        }

        el.outputText.value += char;

        // Low confidence warning
        if (confidence !== undefined && confidence < 0.7) {
            state.lowConfidenceAdded = true;
            el.lowConfidenceOutputWarning.classList.remove('d-none');
        }
    }

    function speakText() {
        const text = el.outputText.value.trim();
        if (!text) return;

        if (!('speechSynthesis' in window)) {
            alert('Text-to-speech is not supported in your browser.');
            return;
        }

        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        utterance.pitch = 1.0;

        utterance.onstart = () => {
            el.speakBtn.classList.add('d-none');
            el.stopSpeakBtn.classList.remove('d-none');
        };

        utterance.onend = () => {
            el.speakBtn.classList.remove('d-none');
            el.stopSpeakBtn.classList.add('d-none');
        };

        utterance.onerror = () => {
            el.speakBtn.classList.remove('d-none');
            el.stopSpeakBtn.classList.add('d-none');
        };

        window.speechSynthesis.speak(utterance);
    }

    function stopSpeaking() {
        window.speechSynthesis.cancel();
        el.speakBtn.classList.remove('d-none');
        el.stopSpeakBtn.classList.add('d-none');
    }

    // ============================================================
    // UTILITIES
    // ============================================================
    function getConfidenceClass(confidence) {
        if (confidence >= 0.7) return 'bg-success';
        if (confidence >= 0.5) return 'bg-warning';
        return 'bg-danger';
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    // ============================================================
    // Cleanup on page unload
    // ============================================================
    window.addEventListener('beforeunload', () => {
        stopCamera();
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
    });

    // ============================================================
    // Start
    // ============================================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();

// Form Handler and API Communication

// Show loading overlay
function showLoading(message = 'Analyzing...') {
    const overlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    if (overlay) {
        if (loadingText) loadingText.textContent = message;
        overlay.classList.add('active');
    }
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

// Show error message
function showError(message) {
    // Create error toast
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-toast';
    errorDiv.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(239, 68, 68, 0.3);
            z-index: 10000;
            font-weight: 600;
            max-width: 400px;
            animation: slideIn 0.3s ease-out;
        ">
            ⚠️ ${message}
        </div>
    `;
    document.body.appendChild(errorDiv);

    // Auto remove after 5 seconds
    setTimeout(() => {
        errorDiv.style.opacity = '0';
        errorDiv.style.transition = 'opacity 0.3s';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

// Show success message
function showSuccess(message) {
    console.log('Success:', message);
}

// Fake News Detection Handler
if (document.getElementById('fakenews-form')) {
    const form = document.getElementById('fakenews-form');
    const textarea = document.getElementById('news-text');
    const charCount = document.getElementById('char-count');

    // Character counter
    if (textarea && charCount) {
        textarea.addEventListener('input', () => {
            const count = textarea.value.length;
            charCount.textContent = `${count} characters`;
        });
    }

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const newsText = textarea.value.trim();

        if (!newsText) {
            showError('Please enter news text to analyze');
            return;
        }

        if (newsText.length < 10) {
            showError('Please enter at least 10 characters');
            return;
        }

        showLoading('Analyzing news article...');

        try {
            const response = await fetch('/api/detect/fakenews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: newsText })
            });

            const data = await response.json();

            hideLoading();

            if (data.success) {
                // Store result in sessionStorage
                sessionStorage.setItem('detectionResult', JSON.stringify(data));
                sessionStorage.setItem('detectionType', 'fakenews');
                sessionStorage.setItem('inputText', newsText);

                // Redirect to result page
                window.location.href = '/result/fakenews';
            } else {
                showError(data.error || 'An error occurred during analysis');
            }
        } catch (error) {
            hideLoading();
            showError('Network error. Please try again.');
            console.error('Error:', error);
        }
    });
}

// Deepfake Detection Handler
if (document.getElementById('deepfake-form')) {
    const form = document.getElementById('deepfake-form');
    const fileInput = document.getElementById('video-file');
    const uploadArea = document.getElementById('upload-area');
    const fileName = document.getElementById('file-name');

    // Drag and drop handlers
    if (uploadArea) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('dragover');
            });
        });

        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                updateFileName(files[0].name);
            }
        });

        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
    }

    // File input change
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                updateFileName(e.target.files[0].name);
            }
        });
    }

    function updateFileName(name) {
        if (fileName) {
            fileName.textContent = name;
            fileName.style.display = 'block';
        }
    }

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!fileInput.files || fileInput.files.length === 0) {
            showError('Please select a video file');
            return;
        }

        const file = fileInput.files[0];
        const maxSize = 100 * 1024 * 1024; // 100MB

        if (file.size > maxSize) {
            showError('File size exceeds 100MB limit');
            return;
        }

        showLoading('Uploading and analyzing video...');

        const formData = new FormData();
        formData.append('video', file);

        try {
            const response = await fetch('/api/detect/deepfake', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            hideLoading();

            if (data.success) {
                // Store result in sessionStorage
                sessionStorage.setItem('detectionResult', JSON.stringify(data));
                sessionStorage.setItem('detectionType', 'deepfake');
                sessionStorage.setItem('fileName', file.name);

                // Redirect to result page
                window.location.href = '/result/deepfake';
            } else {
                showError(data.error || 'An error occurred during analysis');
            }
        } catch (error) {
            hideLoading();
            showError('Network error. Please try again.');
            console.error('Error:', error);
        }
    });
}

// Result Page Handler
if (window.location.pathname.includes('/result/')) {
    document.addEventListener('DOMContentLoaded', () => {
        const resultData = sessionStorage.getItem('detectionResult');
        const detectionType = sessionStorage.getItem('detectionType');

        if (resultData && detectionType) {
            const data = JSON.parse(resultData);
            displayResult(data, detectionType);
        } else {
            // No result data, redirect to home
            window.location.href = '/';
        }
    });
}

function displayResult(data, type) {
    const resultIcon = document.getElementById('result-icon');
    const resultLabel = document.getElementById('result-label');
    const resultDescription = document.getElementById('result-description');
    const confidenceFill = document.getElementById('confidence-fill');
    const confidenceText = document.getElementById('confidence-text');
    const detailsContainer = document.getElementById('details-container');

    // Set icon and label
    const isReal = data.status === 'authentic';

    if (resultIcon) {
        resultIcon.textContent = isReal ? '✓' : '⚠';
        resultIcon.style.color = isReal ? '#10b981' : '#ef4444';
    }

    if (resultLabel) {
        resultLabel.textContent = data.prediction;
        resultLabel.className = `result-label ${isReal ? 'real' : 'fake'}`;
    }

    if (resultDescription) {
        const typeText = type === 'fakenews' ? 'news article' : 'video';
        resultDescription.textContent = isReal
            ? `This ${typeText} appears to be authentic.`
            : `This ${typeText} appears to be ${type === 'fakenews' ? 'fake news' : 'a deepfake'}.`;
    }

    // Set confidence meter
    if (confidenceFill && confidenceText) {
        const confidence = data.confidence;
        confidenceFill.style.width = confidence + '%';
        confidenceFill.style.background = isReal
            ? 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)'
            : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
        confidenceText.textContent = confidence.toFixed(1) + '%';
    }

    // Add additional details
    if (detailsContainer) {
        let detailsHTML = '<div class="glass-card mt-3">';
        detailsHTML += '<h3>Analysis Details</h3>';

        if (type === 'fakenews' && data.probabilities) {
            detailsHTML += `
                <p><strong>Fake Probability:</strong> ${data.probabilities.fake}%</p>
                <p><strong>Real Probability:</strong> ${data.probabilities.real}%</p>
            `;
        }

        if (type === 'deepfake' && data.video_info) {
            detailsHTML += `
                <p><strong>Frames Analyzed:</strong> ${data.frames_analyzed}</p>
                <p><strong>Video Resolution:</strong> ${data.video_info.resolution}</p>
                <p><strong>FPS:</strong> ${data.video_info.fps}</p>
            `;
            if (data.note) {
                detailsHTML += `<p class="text-muted mt-2"><em>${data.note}</em></p>`;
            }
        }

        detailsHTML += '</div>';
        detailsContainer.innerHTML = detailsHTML;
    }
}

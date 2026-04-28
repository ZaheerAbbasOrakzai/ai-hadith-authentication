/**
 * AI Hadith Authenticator - Main JavaScript Application
 * Complete frontend functionality for the hadith authentication system
 */

// ======== GLOBAL VARIABLES ========
const APP_CONFIG = {
    apiBaseUrl: window.location.origin,
    maxFileSize: 16 * 1024 * 1024, // 16MB
    supportedFormats: ['text', 'image', 'audio'],
    debounceDelay: 300,
    animationDuration: 300
};

// ======== UTILITY FUNCTIONS ========

/**
 * Debounce function to limit API calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Show loading state
 */
function showLoading(element, show = true) {
    const loadingEl = element.querySelector('.loading-indicator') || 
                   element.querySelector('.btn-loading');
    
    if (show) {
        if (!loadingEl) {
            const spinner = document.createElement('div');
            spinner.className = 'loading-indicator';
            spinner.innerHTML = '<div class="loading"></div>';
            element.appendChild(spinner);
        }
        element.classList.add('opacity-50');
        element.disabled = true;
    } else {
        if (loadingEl) {
            loadingEl.remove();
        }
        element.classList.remove('opacity-50');
        element.disabled = false;
    }
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.getElementById('alertContainer') || 
                        createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} fade-in`;
    alert.innerHTML = `
        <div class="flex items-center gap-sm">
            <i class="icon-${type}"></i>
            <span>${message}</span>
        </div>
        <button class="alert-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (alert.parentElement) {
            alert.remove();
        }
    }, duration);
}

/**
 * Create alert container if it doesn't exist
 */
function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alertContainer';
    container.className = 'alert-container fixed top-4 right-4 z-50';
    document.body.appendChild(container);
    return container;
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copied to clipboard!', 'success');
        }).catch(err => {
            showAlert('Failed to copy', 'error');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showAlert('Copied to clipboard!', 'success');
    }
}

// ======== API FUNCTIONS ========

/**
 * Make API request with error handling
 */
async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(`${APP_CONFIG.apiBaseUrl}${endpoint}`, finalOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        showAlert(error.message, 'error');
        throw error;
    }
}

/**
 * Analyze hadith using AI
 */
async function analyzeHadith(formData) {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsContainer = document.getElementById('analysisResults');
    
    showLoading(analyzeBtn, true);
    
    try {
        const result = await apiRequest('/analyze-hadith', {
            method: 'POST',
            body: formData
        });
        
        if (result.success) {
            displayAnalysisResults(result.data);
        } else {
            showAlert(result.error || 'Analysis failed', 'error');
        }
    } catch (error) {
        showAlert('Analysis failed. Please try again.', 'error');
    } finally {
        showLoading(analyzeBtn, false);
    }
}

/**
 * Display analysis results
 */
function displayAnalysisResults(data) {
    const resultsContainer = document.getElementById('analysisResults');
    
    const confidence = parseFloat(data.confidence) || 0;
    const confidenceColor = confidence >= 80 ? 'success' : 
                        confidence >= 60 ? 'warning' : 'error';
    
    resultsContainer.innerHTML = `
        <div class="card fade-in">
            <div class="card-header">
                <h3 class="card-title">Analysis Results</h3>
            </div>
            <div class="grid grid-cols-2 gap-md">
                <div class="form-group">
                    <label class="form-label">Grade</label>
                    <div class="badge badge-${confidenceColor === 'success' ? 'success' : confidenceColor === 'warning' ? 'warning' : 'error'}">
                        ${escapeHtml(data.grade || 'Unknown')}
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">Confidence</label>
                    <div class="text-primary font-bold">${escapeHtml(data.confidence || '0%')}</div>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Warnings</label>
                <p class="text-gray">${escapeHtml(data.warning || 'No warnings')}</p>
            </div>
            <div class="form-group">
                <label class="form-label">Chain of Narrators (Isnad)</label>
                <p class="text-gray">${escapeHtml(data.isnad || 'Not available')}</p>
            </div>
            <div class="form-group">
                <label class="form-label">Source</label>
                <p class="text-gray">${escapeHtml(data.source || 'Not available')}</p>
            </div>
            <div class="flex gap-sm">
                <button class="btn btn-secondary btn-sm" onclick="copyResults('${JSON.stringify(data, null, 2)}')">
                    Copy Results
                </button>
                <button class="btn btn-primary btn-sm" onclick="shareResults()">
                    Share
                </button>
            </div>
        </div>
    `;
    
    resultsContainer.classList.remove('hidden');
    resultsContainer.classList.add('fade-in');
}

/**
 * Copy analysis results
 */
function copyResults(resultsJson) {
    copyToClipboard(resultsJson);
}

/**
 * Share analysis results
 */
function shareResults() {
    const url = window.location.href;
    if (navigator.share) {
        navigator.share({
            title: 'Hadith Analysis Results',
            text: 'Check out this hadith analysis',
            url: url
        });
    } else {
        copyToClipboard(url);
        showAlert('Link copied to clipboard!', 'success');
    }
}

/**
 * Search hadith database
 */
async function searchHadith(query) {
    if (!query.trim()) {
        return;
    }
    
    const searchInput = document.getElementById('searchInput');
    const resultsContainer = document.getElementById('searchResults');
    
    showLoading(searchInput, true);
    
    try {
        const result = await apiRequest(`/search?q=${encodeURIComponent(query)}`);
        displaySearchResults(result.results || []);
    } catch (error) {
        showAlert('Search failed. Please try again.', 'error');
    } finally {
        showLoading(searchInput, false);
    }
}

/**
 * Display search results
 */
function displaySearchResults(results) {
    const resultsContainer = document.getElementById('searchResults');
    
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="text-center p-lg">
                <p class="text-gray">No hadith found matching your search.</p>
            </div>
        `;
        return;
    }
    
    const resultsHtml = results.map(hadith => `
        <div class="card mb-md">
            <div class="card-header">
                <h4 class="text-primary">${escapeHtml(hadith.english || 'Unknown')}</h4>
                <div class="flex gap-sm">
                    <span class="badge badge-${hadith.grade === 'Sahih' ? 'success' : hadith.grade === 'Hasan' ? 'warning' : 'error'}">
                        ${escapeHtml(hadith.grade || 'Unknown')}
                    </span>
                    <span class="text-gray text-sm">${escapeHtml(hadith.source || 'Unknown')}</span>
                </div>
            </div>
            <div class="form-group">
                <p class="text-gray">${escapeHtml(hadith.english || '')}</p>
                ${hadith.arabic ? `<p class="text-arabic">${escapeHtml(hadith.arabic)}</p>` : ''}
            </div>
            <div class="flex gap-sm">
                <button class="btn btn-secondary btn-sm" onclick="analyzeText('${escapeHtml(hadith.english || '')}')">
                    Analyze This
                </button>
                <button class="btn btn-primary btn-sm" onclick="copyToClipboard('${escapeHtml(hadith.english || '')}')">
                    Copy
                </button>
            </div>
        </div>
    `).join('');
    
    resultsContainer.innerHTML = resultsHtml;
}

/**
 * Analyze text from search results
 */
function analyzeText(text) {
    // Navigate to analyzer with pre-filled text
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/hadith-analyzer';
    
    const textInput = document.createElement('input');
    textInput.type = 'hidden';
    textInput.name = 'text';
    textInput.value = text;
    
    form.appendChild(textInput);
    document.body.appendChild(form);
    form.submit();
}

/**
 * Handle file uploads
 */
function handleFileUpload(input, previewContainer) {
    const file = input.files[0];
    if (!file) return;
    
    // Check file size
    if (file.size > APP_CONFIG.maxFileSize) {
        showAlert('File size exceeds 16MB limit', 'error');
        return;
    }
    
    // Check file type
    const fileType = file.type.split('/')[0];
    if (!APP_CONFIG.supportedFormats.includes(fileType)) {
        showAlert('Unsupported file format', 'error');
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const preview = document.createElement('div');
        preview.className = 'file-preview p-md';
        
        if (fileType === 'image') {
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview" class="max-w-full rounded">`;
        } else if (fileType === 'audio') {
            preview.innerHTML = `<audio src="${e.target.result}" controls class="w-full"></audio>`;
        } else {
            preview.innerHTML = `<p class="text-gray">File loaded: ${escapeHtml(file.name)}</p>`;
        }
        
        previewContainer.innerHTML = '';
        previewContainer.appendChild(preview);
    };
    
    reader.readAsDataURL(file);
}

/**
 * Chat with AI assistant
 */
async function sendChatMessage() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSendBtn');
    const messagesContainer = document.getElementById('chatMessages');
    
    const message = chatInput.value.trim();
    if (!message) return;
    
    showLoading(sendBtn, true);
    
    try {
        const result = await apiRequest('/chat/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        if (result.success) {
            displayChatMessage(message, 'user');
            displayChatMessage(result.response, 'assistant');
            chatInput.value = '';
        } else {
            showAlert(result.error || 'Chat failed', 'error');
        }
    } catch (error) {
        showAlert('Chat failed. Please try again.', 'error');
    } finally {
        showLoading(sendBtn, false);
    }
}

/**
 * Display chat message
 */
function displayChatMessage(message, sender) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageEl = document.createElement('div');
    messageEl.className = `chat-message chat-message-${sender} fade-in`;
    
    const isUser = sender === 'user';
    const avatar = isUser ? '👤' : '🤖';
    const bgColor = isUser ? 'bg-primary' : 'bg-gray-600';
    
    messageEl.innerHTML = `
        <div class="flex gap-sm">
            <div class="chat-avatar">${avatar}</div>
            <div class="chat-bubble ${bgColor}">
                <p class="text-white">${escapeHtml(message)}</p>
                <span class="chat-time">${new Date().toLocaleTimeString()}</span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// ======== INITIALIZATION ========

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        const debouncedSearch = debounce(searchHadith, APP_CONFIG.debounceDelay);
        searchInput.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
    }
    
    // Initialize file upload handlers
    const imageInput = document.getElementById('imageInput');
    const audioInput = document.getElementById('audioInput');
    
    if (imageInput) {
        imageInput.addEventListener('change', (e) => {
            handleFileUpload(e.target, document.getElementById('imagePreview'));
        });
    }
    
    if (audioInput) {
        audioInput.addEventListener('change', (e) => {
            handleFileUpload(e.target, document.getElementById('audioPreview'));
        });
    }
    
    // Initialize chat functionality
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');
    
    if (chatInput && chatSendBtn) {
        chatSendBtn.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
    
    // Initialize form submissions
    const analyzeForm = document.getElementById('analyzeForm');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(analyzeForm);
            analyzeHadith(formData);
        });
    }
    
    // Initialize theme toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('change', (e) => {
            document.body.classList.toggle('dark-theme', e.target.checked);
            localStorage.setItem('theme', e.target.checked ? 'dark' : 'light');
        });
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
            themeToggle.checked = true;
        }
    }
    
    // Initialize keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl+K for search
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            searchInput?.focus();
        }
        
        // Ctrl+/ for chat
        if (e.ctrlKey && e.key === '/') {
            e.preventDefault();
            chatInput?.focus();
        }
    });
    
    // Initialize offline detection
    window.addEventListener('online', () => {
        showAlert('Connection restored', 'success');
    });
    
    window.addEventListener('offline', () => {
        showAlert('Connection lost. Some features may not work.', 'warning');
    });
    
    console.log('AI Hadith Authenticator initialized successfully');
});

// ======== ERROR HANDLING ========

window.addEventListener('error', function(e) {
    console.error('Application Error:', e.error);
    showAlert('An unexpected error occurred. Please refresh the page.', 'error');
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled Promise Rejection:', e.reason);
    showAlert('An unexpected error occurred. Please try again.', 'error');
});

// Voice Search Variables
let recognition = null;
let isListening = false;

// Initialize Voice Recognition
function initVoiceRecognition() {
    // Check for browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.warn('Speech recognition not supported in this browser');
        document.getElementById('voiceSearchButton').style.display = 'none';
        return;
    }
    
    // Create recognition instance
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    // Event Handlers
    recognition.onstart = () => {
        isListening = true;
        document.getElementById('recordingStatus').classList.remove('hidden');
        document.getElementById('startRecordingBtn').innerHTML = '<i class="fas fa-stop mr-2"></i><span>Stop Recording</span>';
        document.getElementById('startRecordingBtn').classList.remove('bg-green-600', 'hover:bg-green-700');
        document.getElementById('startRecordingBtn').classList.add('bg-red-600', 'hover:bg-red-700');
    };
    
    recognition.onend = () => {
        isListening = false;
        document.getElementById('recordingStatus').classList.add('hidden');
        document.getElementById('startRecordingBtn').innerHTML = '<i class="fas fa-microphone mr-2"></i><span>Start Recording</span>';
        document.getElementById('startRecordingBtn').classList.remove('bg-red-600', 'hover:bg-red-700');
        document.getElementById('startRecordingBtn').classList.add('bg-green-600', 'hover:bg-green-700');
        
        // Hide voice options panel after a short delay
        setTimeout(() => {
            if (!isListening) {
                document.getElementById('voiceOptionsPanel').classList.add('hidden');
            }
        }, 2000);
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('searchInput').value = transcript;
        
        // Automatically submit the form after a short delay
        setTimeout(() => {
            document.getElementById('searchForm').dispatchEvent(new Event('submit'));
        }, 500);
    };
    
    recognition.onerror = function(event) {
        console.error('Speech Recognition Error:', event.error);
        
        let message = 'Unknown Error';
        
        switch(event.error) {
            case 'network':
                message = 'Network Error: Please check your internet connection. Google Speech API requires internet.';
                break;
            case 'not-allowed':
            case 'service-not-allowed':
                message = 'Permission Denied: Please click the Lock icon 🔒 in the address bar and Allow Microphone.';
                break;
            case 'audio-capture':
                message = 'No Microphone Found: Please check if your mic is connected and working.';
                break;
            case 'no-speech':
                message = 'No Speech Detected: Please speak louder or closer to the mic.';
                break;
            case 'aborted':
                message = 'Recording Aborted.';
                break;
            case 'language-not-supported':
                message = 'Language not supported. Please try with English (en-US).';
                break;
            case 'bad-grammar':
                message = 'Speech grammar error. Please try again.';
                break;
            default:
                message = `Speech Recognition Error: ${event.error}. Please try again.`;
        }
        
        // Show error message to user
        showToast(message, 'error');
        console.error('Speech Recognition Error Details:', event);
        
        // Reset UI
        isListening = false;
        const micIcon = document.querySelector('#voiceSearchButton i');
        if (micIcon) {
            micIcon.classList.remove('text-red-500', 'animate-pulse');
            micIcon.classList.add('text-gray-400');
        }
        
        // Hide recording status
        const recordingStatus = document.getElementById('recordingStatus');
        if (recordingStatus) recordingStatus.classList.add('hidden');
        
        // Reset button text and style
        const startBtn = document.getElementById('startRecordingBtn');
        if (startBtn) {
            startBtn.innerHTML = '<i class="fas fa-microphone mr-2"></i><span>Start Recording</span>';
            startBtn.classList.remove('bg-red-600', 'hover:bg-red-700');
            startBtn.classList.add('bg-green-600', 'hover:bg-green-700');
        }
    };
    
    // Setup event listeners for voice search UI
    setupVoiceSearchUI();
}

// Setup Voice Search UI Event Listeners
function setupVoiceSearchUI() {
    const voiceSearchBtn = document.getElementById('voiceSearchButton');
    const voiceOptionsPanel = document.getElementById('voiceOptionsPanel');
    const startRecordingBtn = document.getElementById('startRecordingBtn');
    
    if (!voiceSearchBtn || !voiceOptionsPanel || !startRecordingBtn) return;
    
    // Toggle voice options panel
    voiceSearchBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        voiceOptionsPanel.classList.toggle('hidden');
    });
    
    // Start/stop recording
    startRecordingBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (isListening) {
            recognition.stop();
        } else {
            try {
                recognition.start();
            } catch (error) {
                console.error('Error starting voice recognition:', error);
                showToast('Error starting voice recognition', 'error');
            }
        }
    });
    
    // Close panel when clicking outside
    document.addEventListener('click', (e) => {
        if (!voiceOptionsPanel.contains(e.target) && e.target !== voiceSearchBtn) {
            voiceOptionsPanel.classList.add('hidden');
        }
    });
}

// Main JavaScript for Landing Page
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dark mode
    initDarkMode();
    
    // Initialize animations
    initAnimations();
    
    // Setup smooth scrolling
    setupSmoothScroll();
    
    // Setup mobile menu
    setupMobileMenu();
    
    // Add search functionality
    setupSearch();
    
    // Initialize voice recognition
    initVoiceRecognition();
});

// Dark Mode Functionality
function initDarkMode() {
    // Check for saved dark mode preference
    const savedTheme = localStorage.getItem('darkMode');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Apply dark mode if saved preference exists or system prefers dark
    if (savedTheme === 'true' || (!savedTheme && systemPrefersDark)) {
        document.body.classList.add('dark-mode');
        updateDarkModeIcon(true);
    }
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('darkMode')) {
            if (e.matches) {
                document.body.classList.add('dark-mode');
                updateDarkModeIcon(true);
            } else {
                document.body.classList.remove('dark-mode');
                updateDarkModeIcon(false);
            }
        }
    });
}

function toggleDarkMode() {
    const isDark = document.body.classList.toggle('dark-mode');
    
    // Save preference to localStorage
    localStorage.setItem('darkMode', isDark);
    
    // Update icons
    updateDarkModeIcon(isDark);
    
    // Show toast notification
    showToast(`${isDark ? 'Dark' : 'Light'} mode activated`, 'success');
    
    // Add transition effect
    document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    
    // Trigger a custom event for other components to listen to
    window.dispatchEvent(new CustomEvent('darkModeToggle', { detail: { isDark } }));
}

function updateDarkModeIcon(isDark) {
    // Update main navigation icon
    const mainIcon = document.getElementById('darkModeIcon');
    if (mainIcon) {
        mainIcon.className = isDark ? 
            'fas fa-sun text-yellow-300 group-hover:text-yellow-400 transition-colors' : 
            'fas fa-moon text-white group-hover:text-yellow-300 transition-colors';
    }
    
    // Update mobile navigation icon
    const mobileIcon = document.getElementById('mobileDarkModeIcon');
    if (mobileIcon) {
        mobileIcon.className = isDark ? 'fas fa-sun text-yellow-300' : 'fas fa-moon';
    }
    
    // Update button title
    const toggleButton = document.getElementById('darkModeToggle');
    if (toggleButton) {
        toggleButton.title = isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    }
}

// Listen for dark mode changes across the site
window.addEventListener('darkModeToggle', (e) => {
    const { isDark } = e.detail;
    console.log(`Dark mode ${isDark ? 'enabled' : 'disabled'}`);
});

function initAnimations() {
    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });
}

function setupSmoothScroll() {
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function setupMobileMenu() {
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenuButton.contains(event.target) && !mobileMenu.contains(event.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }
}

// Toggle between collections and search results
function toggleViews(showSearchResults) {
    const collectionsSection = document.getElementById('collections');
    const searchResults = document.getElementById('searchResults');
    const searchInput = document.getElementById('searchInput');
    
    if (showSearchResults) {
        // Show search results, hide collections
        collectionsSection.classList.add('hidden');
        searchResults.classList.remove('hidden');
        // Scroll to search results
        searchResults.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        // Show collections, hide search results
        collectionsSection.classList.remove('hidden');
        searchResults.classList.add('hidden');
        // Clear search input
        if (searchInput) searchInput.value = '';
    }
}

function setupSearch() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const searchResults = document.getElementById('searchResults');
    const collectionsSection = document.getElementById('collections');
    const imageUpload = document.getElementById('imageUpload');
    
    if (!searchForm || !searchInput || !searchBtn || !searchResults || !collectionsSection || !imageUpload) return;
    
    // Handle image upload
    imageUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            showToast(`Image selected: ${file.name}`, 'info');
            // TODO: Add image processing and AI analysis here
            console.log('Selected file:', file);
            
            // Reset the input to allow selecting the same file again if needed
            e.target.value = '';
        }
    });
    
    // Handle form submission
    searchForm.addEventListener('submit', handleSearch);
    
    // Handle Enter key in search input
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleSearch(e);
        } else if (e.key === 'Escape' || this.value === '') {
            // Show collections when clearing search or pressing Escape
            toggleViews(false);
        }
    });
    
    // Handle search button click
    searchBtn.addEventListener('click', function(e) {
        e.preventDefault();
        handleSearch(e);
    });
    
    // Handle click outside search to close results
    document.addEventListener('click', function(e) {
        if (!searchForm.contains(e.target) && searchResults.innerHTML.trim() !== '') {
            toggleViews(false);
        }
    });
}

// Image upload & verification for Hadith images
function verifyHadithImage(event) {
    const input = event.target || event;
    const file = input.files ? input.files[0] : null;
    if (!file) return;

    // Notify user
    showToast('Uploading image for verification...', 'success');

    // Create modal preview
    const backdrop = document.createElement('div');
    backdrop.className = 'fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50';
    backdrop.id = 'hadithVerifyBackdrop';

    const modal = document.createElement('div');
    modal.className = 'bg-white rounded-lg shadow-2xl p-4 max-w-lg w-full mx-4';
    modal.innerHTML = `
        <div class="flex items-start space-x-4">
            <div class="w-1/3">
                <img id="hadithPreviewImg" src="" alt="Preview" class="w-full h-auto rounded" />
            </div>
            <div class="flex-1">
                <h3 class="text-lg font-semibold mb-2">Verifying Hadith Image</h3>
                <p class="text-sm text-gray-600 mb-4">We are analyzing the uploaded image to verify authenticity. This is a simulated check for demo purposes.</p>
                <div id="hadithVerifyResult" class="text-sm text-gray-800">Processing...</div>
                <div class="mt-4 flex justify-end">
                    <button id="hadithCloseBtn" class="px-4 py-2 modal-cancel-btn rounded mr-2">Cancel</button>
                </div>
            </div>
        </div>
    `;

    backdrop.appendChild(modal);
    document.body.appendChild(backdrop);

    // Read and show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = document.getElementById('hadithPreviewImg');
        if (img) img.src = e.target.result;
    };
    reader.readAsDataURL(file);

    const form = new FormData();
    form.append('file', file);
    fetch('/authenticate-hadith', {
        method: 'POST',
        body: form
    }).then(r => r.json()).then(data => {
        const resultDiv = document.getElementById('hadithVerifyResult');
        if (!resultDiv) return;
        if (data && data.success) {
            const val = typeof data.result === 'string' ? data.result : JSON.stringify(data.result);
            resultDiv.className = 'text-sm text-green-600';
            resultDiv.innerHTML = `<strong>Result:</strong> ${val}`;
            showToast('Verification complete', 'success');
        } else {
            resultDiv.className = 'text-sm text-red-600';
            resultDiv.textContent = data && data.error ? data.error : 'Verification failed.';
            showToast('Verification failed', 'error');
        }
    }).catch(err => {
        const resultDiv = document.getElementById('hadithVerifyResult');
        if (resultDiv) resultDiv.textContent = 'Verification failed. Please try again.';
        showToast('Image verification failed', 'error');
    });

    // Close handler
    document.addEventListener('click', function handler(e) {
        const closeBtn = document.getElementById('hadithCloseBtn');
        if (closeBtn && (e.target === closeBtn || e.target.closest('#hadithCloseBtn'))) {
            const bd = document.getElementById('hadithVerifyBackdrop');
            if (bd) bd.remove();
            // cleanup input value so same file can be selected again
            const fi = document.getElementById('hadithImageInput');
            if (fi) fi.value = '';
            document.removeEventListener('click', handler);
        }
    });
}

// Wire upload button & input after DOM ready
document.addEventListener('DOMContentLoaded', function() {
    const imgInput = document.getElementById('hadithImageInput');
    const uploadBtn = document.getElementById('uploadImageBtn');
    if (uploadBtn && imgInput) {
        uploadBtn.addEventListener('click', () => imgInput.click());
        imgInput.addEventListener('change', verifyHadithImage);
    }
});

function showSearchSuggestions(query) {
    // Remove existing suggestions
    hideSearchSuggestions();
    
    // Sample suggestions (in real app, this would come from API)
    const suggestions = [
        'Prayer times and importance',
        'Fasting during Ramadan',
        'Charity and Zakat',
        'Treatment of parents',
        'Honesty in business',
        'Kindness to animals',
        'Knowledge and learning',
        'Patience and perseverance'
    ];
    
    // Filter suggestions based on query
    const filteredSuggestions = suggestions.filter(s => 
        s.toLowerCase().includes(query.toLowerCase())
    );
    
    if (filteredSuggestions.length > 0) {
        // Create suggestions dropdown
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.id = 'searchSuggestions';
        suggestionsDiv.className = 'absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-lg shadow-lg mt-1 z-50';
        
        filteredSuggestions.slice(0, 5).forEach(suggestion => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = 'px-4 py-3 hover:bg-gray-50 cursor-pointer text-sm text-gray-700';
            suggestionItem.innerHTML = `
                <i class="fas fa-search text-gray-400 mr-2"></i>
                ${highlightMatch(suggestion, query)}
            `;
            suggestionItem.addEventListener('click', () => {
                document.getElementById('searchInput').value = suggestion;
                hideSearchSuggestions();
            });
            suggestionsDiv.appendChild(suggestionItem);
        });
        
        // Position suggestions below search bar
        const searchContainer = document.getElementById('searchInput').closest('.bg-white');
        searchContainer.style.position = 'relative';
        searchContainer.appendChild(suggestionsDiv);
    }
}

function hideSearchSuggestions() {
    const suggestions = document.getElementById('searchSuggestions');
    if (suggestions) {
        suggestions.remove();
    }
}

function highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<span class="font-semibold text-green-600">$1</span>');
}

async function handleSearch(event) {
    event.preventDefault();
    
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchBtn = document.getElementById('searchBtn');
    const collectionFilter = document.getElementById('collectionFilter');
    
    const query = searchInput.value.trim();
    const collection = collectionFilter ? collectionFilter.value : '';
    
    if (!query) {
        showToast('Please enter a search term', 'error');
        toggleViews(false);
        return;
    }
    
    console.log('Searching for:', query);
    
    // Show loading state
    const originalBtnText = searchBtn.innerHTML;
    searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    searchBtn.disabled = true;
    
    try {
        // Build search URL with query parameters
        const params = new URLSearchParams({ q: query });
        if (collection) {
            params.append('collection', collection);
        }
        
        // Show loading state
        searchResults.innerHTML = `
            <div class="flex flex-col items-center justify-center p-8">
                <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500 mb-4"></div>
                <p class="text-gray-300">Searching for "${query}"...</p>
            </div>
        `;
        
        // Make API request to backend
        const response = await fetch(`/search?${params.toString()}`);
        const data = await response.json();
        
        if (!response.ok) {
            console.error('Search API Error:', data);
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }
        
        console.log('Search results:', data);
        
        // Show search results view
        toggleViews(true);
        
        // Display results
        if (Array.isArray(data)) {
            displaySearchResults(data, query);
        } else {
            throw new Error('Invalid response format from server');
        }
        
    } catch (error) {
        console.error('Search error:', error);
        
        // Log the full error for debugging
        if (error instanceof Error) {
            console.error('Error details:', {
                message: error.message,
                stack: error.stack,
                name: error.name
            });
        }
        
        showToast('Error performing search. Please try again.', 'error');
        
        // Show user-friendly error message
        searchResults.innerHTML = `
            <div class="bg-red-900 bg-opacity-50 border border-red-700 text-red-200 p-8 rounded-xl max-w-2xl mx-auto">
                <div class="flex flex-col items-center text-center">
                    <i class="fas fa-exclamation-triangle text-4xl mb-4 text-red-400"></i>
                    <h3 class="text-xl font-bold mb-2">Search Failed</h3>
                    <p class="mb-6">${error.message || 'An error occurred while searching. Please try again.'}</p>
                    <button onclick="toggleViews(false)" class="px-6 py-2 bg-red-700 hover:bg-red-800 rounded-lg transition-colors text-white">
                        <i class="fas fa-arrow-left mr-2"></i> Back to Collections
                    </button>
                </div>
            </div>
        `;
    } finally {
        // Reset button state
        searchBtn.innerHTML = originalBtnText;
        searchBtn.disabled = false;
    }
}

function displaySearchResults(results, query) {
    const searchResults = document.getElementById('searchResults');
    
    if (!results || results.length === 0) {
        searchResults.innerHTML = `
            <div class="bg-yellow-900 bg-opacity-50 border border-yellow-700 text-yellow-200 p-8 rounded-xl text-center max-w-2xl mx-auto">
                <i class="fas fa-search text-4xl mb-4 text-yellow-400"></i>
                <h3 class="text-xl font-bold mb-2">No Results Found</h3>
                <p class="mb-6">We couldn't find any hadiths matching "${query}"</p>
                <button onclick="toggleViews(false)" class="px-6 py-2 bg-yellow-700 hover:bg-yellow-800 rounded-lg transition-colors text-white">
                    <i class="fas fa-arrow-left mr-2"></i> Back to Collections
                </button>
            </div>
        `;
        return;
    }
    
    // Create results HTML
    let resultsHTML = `
        <div class="mb-8">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
                <h2 class="text-2xl font-bold text-white mb-4 md:mb-0">
                    Search Results
                    <span class="text-gray-400 text-lg ml-2">${results.length} ${results.length === 1 ? 'result' : 'results'} for "${query}"</span>
                </h2>
                <button onclick="toggleViews(false)" class="text-gray-300 hover:text-white flex items-center justify-center md:justify-start">
                    <i class="fas fa-arrow-left mr-2"></i> Back to Collections
                </button>
            </div>
            <div class="space-y-6">
    `;
    
    results.forEach(hadith => {
        // Determine grade color - check both possible field names
        let gradeColor = 'bg-yellow-600';
        const grade = hadith.grade || hadith.classification || '';
        if (grade && grade.toLowerCase().includes('sahih')) {
            gradeColor = 'bg-green-600';
        } else if (grade && grade.toLowerCase().includes('hasan')) {
            gradeColor = 'bg-blue-600';
        }
        
        // Highlight search terms in text
        const highlightText = (text) => {
            if (!text || !query) return text || '';
            const regex = new RegExp(`(${query})`, 'gi');
            return text.replace(regex, '<span class="bg-yellow-500 bg-opacity-50">$1</span>');
        };
        
        resultsHTML += `
            <div class="bg-gray-800 bg-opacity-70 rounded-xl overflow-hidden border border-gray-700 hover:border-green-500 transition-all duration-200 relative group" 
                 onclick="copyToClipboard(this)">
                
                <!-- Header with source and number -->
                <div class="px-6 py-4 bg-gray-900 bg-opacity-50 border-b border-gray-700 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div>
                        <span class="font-semibold text-green-400">${hadith.source_book || hadith.book || 'Unknown Source'}</span>
                        ${hadith.hadith_number || hadith.hadithnumber ? `<span class="text-gray-400 text-sm ml-2">#${hadith.hadith_number || hadith.hadithnumber}</span>` : ''}
                    </div>
                    <button class="text-xs px-3 py-1 bg-indigo-600 text-white rounded-full w-fit hover:bg-indigo-700" onclick="event.stopPropagation(); verifyHadithTextFromCard(this)">Verify</button>
                    ${hadith.grade || hadith.classification ? `
                        <span class="text-xs px-3 py-1 ${gradeColor} text-white rounded-full w-fit">
                            ${hadith.grade || hadith.classification}
                        </span>
                    ` : ''}
                </div>
                
                <!-- Arabic Text -->
                ${hadith.text_arabic || hadith.text_ar ? `
                    <div class="p-6 text-right text-xl text-gray-200 leading-relaxed font-arabic" dir="rtl">
                        ${highlightText(hadith.text_arabic || hadith.text_ar)}
                    </div>
                ` : ''}
                
                <!-- English Text -->
                ${hadith.text_english || hadith.text_en ? `
                    <div class="p-6 pt-2 text-gray-300 border-t border-gray-700">
                        <div class="text-sm text-gray-400 mb-2">Translation:</div>
                        <div class="leading-relaxed">${highlightText(hadith.text_english || hadith.text_en)}</div>
                    </div>
                ` : `
                    <div class="p-6 pt-2 text-gray-400 border-t border-gray-700">
                        <div class="text-sm text-gray-500 mb-2">Translation:</div>
                        <div class="leading-relaxed italic">Translation not available.</div>
                    </div>
                `}
                
                ${hadith.chapter ? `
                    <div class="px-6 py-3 bg-gray-900 bg-opacity-30 text-sm text-gray-400 border-t border-gray-700">
                        <span class="font-medium">Chapter:</span> ${hadith.chapter}
                    </div>
                ` : ''}
                
                <!-- Hover effect -->
                <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-200 flex items-center justify-center opacity-0 group-hover:opacity-100">
                    <div class="bg-black bg-opacity-70 text-white text-xs px-3 py-1.5 rounded-full flex items-center">
                        <i class="fas fa-copy mr-1.5"></i>
                        <span>Click to copy</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    resultsHTML += '</div></div>'; // Close results container
    searchResults.innerHTML = resultsHTML;
    searchResults.classList.remove('hidden');
    
    // Scroll to results
    searchResults.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function verifyHadithTextFromCard(btn){
    const card = btn.closest('.bg-gray-800');
    if (!card) return;
    const arabicEl = card.querySelector('.font-arabic');
    const engEl = card.querySelector('.p-6.pt-2');
    const text = (arabicEl ? arabicEl.textContent : '') + '\n' + (engEl ? engEl.textContent.replace('Translation:', '') : '');
    verifyHadithText(text.trim(), card);
}

async function verifyHadithText(text, cardRef){
    if (!text) {
        showToast('No text to verify', 'error');
        return;
    }
    showToast('Verifying hadith...', 'success');
    try{
        const res = await fetch('/authenticate-hadith', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await res.json();
        if (data && data.success){
            const val = typeof data.result === 'string' ? data.result : JSON.stringify(data.result);
            showToast('Verification complete', 'success');
            showVerificationModal(val);
            if (cardRef) {
                let badge = cardRef.querySelector('.ai-verify-badge');
                if (!badge) {
                    const header = cardRef.querySelector('.px-6.py-4');
                    if (header) {
                        badge = document.createElement('span');
                        badge.className = 'ai-verify-badge ml-2 text-xs px-3 py-1 bg-indigo-600 text-white rounded-full';
                        header.appendChild(badge);
                    }
                }
                if (badge) {
                    badge.textContent = 'Verified';
                }
            }
        } else {
            showToast(data && data.error ? data.error : 'Verification failed', 'error');
        }
    } catch (e){
        showToast('Verification error', 'error');
    }
}

function showVerificationModal(content){
    let backdrop = document.getElementById('hfVerifyBackdrop');
    if (backdrop) backdrop.remove();
    backdrop = document.createElement('div');
    backdrop.id = 'hfVerifyBackdrop';
    backdrop.className = 'fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50';
    const modal = document.createElement('div');
    modal.className = 'bg-white rounded-lg shadow-2xl p-6 max-w-lg w-full mx-4';
    modal.innerHTML = `
        <h3 class="text-lg font-semibold mb-3">Hadith Verification</h3>
        <div class="text-sm text-gray-800 whitespace-pre-wrap break-words max-h-96 overflow-auto" id="hfVerifyContent">${content}</div>
        <div class="mt-4 flex justify-end">
            <button id="hfVerifyClose" class="px-4 py-2 modal-cancel-btn rounded">Close</button>
        </div>
    `;
    backdrop.appendChild(modal);
    document.body.appendChild(backdrop);
    const closeBtn = document.getElementById('hfVerifyClose');
    closeBtn.addEventListener('click', () => {
        const bd = document.getElementById('hfVerifyBackdrop');
        if (bd) bd.remove();
    });
}

// Copy to clipboard function
function copyToClipboard(element) {
    // Find text content to copy (Arabic or English) - check both possible field names
    const arabicTextElement = element.querySelector('.font-arabic');
    const englishTextElement = element.querySelector('.text-gray-300, .text-gray-400');
    
    const arabicText = arabicTextElement ? arabicTextElement.textContent : '';
    const englishText = englishTextElement ? englishTextElement.textContent : '';
    
    // Clean up the English text (remove "Translation:" label and "Translation not available.")
    let cleanEnglishText = englishText.replace('Translation:', '').trim();
    if (cleanEnglishText === 'Translation not available.') {
        cleanEnglishText = '';
    }
    
    // Combine both texts with a separator
    const textToCopy = `${arabicText}\n\n${cleanEnglishText}`.trim();
    
    // Copy to clipboard
    navigator.clipboard.writeText(textToCopy).then(() => {
        // Show toast notification
        showToast('Hadith copied to clipboard!', 'success');
        
        // Add visual feedback
        element.classList.add('ring-2', 'ring-green-500');
        setTimeout(() => {
            element.classList.remove('ring-2', 'ring-green-500');
        }, 1000);
    }).catch(err => {
        console.error('Failed to copy text:', err);
        showToast('Failed to copy to clipboard', 'error');
    });
}

function navigateToSection(section) {
    // Prevent default behavior
    event.preventDefault();
    
    // Show loading or navigation feedback
    showToast(`Opening ${section.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}...`, 'success');
    
    // In a real application, this would navigate to the specific section
    console.log('Navigating to:', section);
    
    // Simulate navigation delay
    setTimeout(() => {
        // For demo purposes, scroll to features section
        const featuresSection = document.getElementById('features');
        if (featuresSection) {
            featuresSection.scrollIntoView({ behavior: 'smooth' });
        }
    }, 500);
}

function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('hidden');
    }
}

function showToast(message, type = 'success') {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => toast.remove());
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} mr-2"></i>
        ${message}
    `;
    
    // Add to page
    document.body.appendChild(toast);
    
    // Show toast with animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Hide and remove after delay
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (document.body.contains(toast)) {
                document.body.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// Utility function for demo purposes
function simulateApiCall(data, delay = 1000) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({ success: true, data: data });
        }, delay);
    });
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + K for search focus
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close mobile menu
    if (event.key === 'Escape') {
        const mobileMenu = document.getElementById('mobileMenu');
        if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
            mobileMenu.classList.add('hidden');
        }
    }
});

// Add touch gestures for mobile
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', function(event) {
    touchStartX = event.changedTouches[0].screenX;
});

document.addEventListener('touchend', function(event) {
    touchEndX = event.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    // Swipe right to open mobile menu
    if (touchEndX - touchStartX > 50) {
        const mobileMenu = document.getElementById('mobileMenu');
        if (mobileMenu && mobileMenu.classList.contains('hidden')) {
            mobileMenu.classList.remove('hidden');
        }
    }
    
    // Swipe left to close mobile menu
    if (touchStartX - touchEndX > 50) {
        const mobileMenu = document.getElementById('mobileMenu');
        if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
            mobileMenu.classList.add('hidden');
        }
    }
}

// Initialize theme (dark/light mode) if needed
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
}

// Save theme preference
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    const isDark = document.body.classList.contains('dark-theme');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

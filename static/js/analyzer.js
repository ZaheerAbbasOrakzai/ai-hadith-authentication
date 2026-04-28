// Hadith Analyzer JavaScript
// Handles form submission, analysis, and UI updates

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analyzerForm');
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsSection = document.getElementById('resultsSection');

    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            
            // Show loading
            if (loadingIndicator) {
                loadingIndicator.classList.remove('hidden');
            }
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Analyzing...';
            }
            if (resultsSection) {
                resultsSection.classList.add('hidden');
            }

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    displayResults(data);
                } else {
                    showError(data.error || 'Analysis failed');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            } finally {
                if (loadingIndicator) {
                    loadingIndicator.classList.add('hidden');
                }
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Analyze Hadith';
                }
            }
        });
    }
});

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultContent = document.getElementById('resultContent');
    
    if (resultsSection && resultContent) {
        resultsSection.classList.remove('hidden');
        resultContent.innerHTML = `
            <div class="bg-white rounded-lg p-6 shadow-md">
                <h3 class="text-xl font-bold mb-4">Analysis Results</h3>
                <div class="mb-4">
                    <span class="font-semibold">Grade:</span> 
                    <span class="${getGradeColor(data.grade)}">${data.grade}</span>
                </div>
                <div class="mb-4">
                    <span class="font-semibold">Confidence:</span> ${data.confidence}
                </div>
                ${data.source ? `
                <div class="mb-4">
                    <span class="font-semibold">Source:</span> ${data.source}
                </div>
                ` : ''}
                ${data.analysis ? `
                <div class="mb-4">
                    <span class="font-semibold">Analysis:</span>
                    <p class="mt-2 text-gray-700">${data.analysis}</p>
                </div>
                ` : ''}
            </div>
        `;
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function getGradeColor(grade) {
    if (grade.includes('Sahih') || grade.includes('Authentic')) {
        return 'text-green-600 font-bold';
    } else if (grade.includes('Daif') || grade.includes('Weak')) {
        return 'text-red-600 font-bold';
    } else if (grade.includes('Hasan')) {
        return 'text-blue-600 font-bold';
    }
    return 'text-gray-600';
}

function showError(message) {
    const resultsSection = document.getElementById('resultsSection');
    const resultContent = document.getElementById('resultContent');
    
    if (resultsSection && resultContent) {
        resultsSection.classList.remove('hidden');
        resultContent.innerHTML = `
            <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                <div class="flex items-center">
                    <i class="fas fa-exclamation-circle text-red-500 mr-3"></i>
                    <span class="text-red-700">${message}</span>
                </div>
            </div>
        `;
    }
}

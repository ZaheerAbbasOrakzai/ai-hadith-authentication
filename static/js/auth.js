// Authentication JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dark mode
    initDarkMode();
    
    // Hide all messages on load
    hideMessages();
    
    // Add input validation listeners
    setupValidation();
    
    // Add password strength checker for signup
    if (document.getElementById('password')) {
        document.getElementById('password').addEventListener('input', checkPasswordStrength);
    }
    
    // Add confirm password validation
    if (document.getElementById('confirmPassword')) {
        document.getElementById('confirmPassword').addEventListener('input', validatePasswordMatch);
    }
});

// Dark Mode Functionality (shared with main.js)
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
    
    // Trigger a custom event
    window.dispatchEvent(new CustomEvent('darkModeToggle', { detail: { isDark } }));
}

function updateDarkModeIcon(isDark) {
    // Update auth page icon
    const icon = document.getElementById('darkModeIcon');
    if (icon) {
        icon.className = isDark ? 
            'fas fa-sun text-yellow-300 group-hover:text-yellow-400 transition-colors' : 
            'fas fa-moon text-white group-hover:text-yellow-300 transition-colors';
    }
    
    // Update button title
    const toggleButton = document.querySelector('[onclick="toggleDarkMode()"]');
    if (toggleButton) {
        toggleButton.title = isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    }
}

function hideMessages() {
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => {
        msg.style.display = 'none';
    });
}

function setupValidation() {
    // Email validation
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', validateEmail);
        emailInput.addEventListener('input', clearEmailError);
    }
    
    // Password validation
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('blur', validatePassword);
        passwordInput.addEventListener('input', clearPasswordError);
    }
    
    // Name validation for signup
    const nameInput = document.getElementById('name');
    if (nameInput) {
        nameInput.addEventListener('blur', validateName);
        nameInput.addEventListener('input', clearNameError);
    }
}

function validateEmail() {
    const email = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!emailRegex.test(email.value)) {
        email.classList.add('error');
        emailError.classList.remove('hidden');
        return false;
    }
    return true;
}

function clearEmailError() {
    const email = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    email.classList.remove('error');
    emailError.classList.add('hidden');
}

function validatePassword() {
    const password = document.getElementById('password');
    const passwordError = document.getElementById('passwordError');
    
    if (password.value.length < 6) {
        password.classList.add('error');
        passwordError.classList.remove('hidden');
        return false;
    }
    return true;
}

function clearPasswordError() {
    const password = document.getElementById('password');
    const passwordError = document.getElementById('passwordError');
    password.classList.remove('error');
    passwordError.classList.add('hidden');
}

function validateName() {
    const name = document.getElementById('fullName');
    const nameError = document.getElementById('nameError');
    
    if (name.value.trim().length < 2) {
        name.classList.add('error');
        nameError.classList.remove('hidden');
        return false;
    }
    return true;
}

function clearNameError() {
    const name = document.getElementById('fullName');
    const nameError = document.getElementById('nameError');
    name.classList.remove('error');
    nameError.classList.add('hidden');
}

function validatePasswordMatch() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    const confirmError = document.getElementById('confirmPasswordError');
    
    if (password.value !== confirmPassword.value) {
        confirmPassword.classList.add('error');
        confirmError.classList.remove('hidden');
        return false;
    }
    confirmPassword.classList.remove('error');
    confirmError.classList.add('hidden');
    return true;
}

function checkPasswordStrength() {
    const password = document.getElementById('password').value;
    const strengthBar = document.getElementById('passwordStrength');
    const strengthText = document.getElementById('strengthText');
    
    let strength = 0;
    
    // Length check
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    
    // Complexity checks
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    // Update UI
    const strengthPercentage = (strength / 5) * 100;
    strengthBar.style.width = strengthPercentage + '%';
    
    if (strength <= 1) {
        strengthBar.className = 'h-full bg-red-500 rounded-full transition-all duration-300';
        strengthText.textContent = 'Weak';
        strengthText.className = 'text-xs text-red-500';
    } else if (strength <= 3) {
        strengthBar.className = 'h-full bg-yellow-500 rounded-full transition-all duration-300';
        strengthText.textContent = 'Medium';
        strengthText.className = 'text-xs text-yellow-500';
    } else {
        strengthBar.className = 'h-full bg-green-500 rounded-full transition-all duration-300';
        strengthText.textContent = 'Strong';
        strengthText.className = 'text-xs text-green-500';
    }
}

function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    const toggle = document.getElementById(fieldId + 'Toggle');
    
    if (field.type === 'password') {
        field.type = 'text';
        toggle.classList.remove('fa-eye');
        toggle.classList.add('fa-eye-slash');
    } else {
        field.type = 'password';
        toggle.classList.remove('fa-eye-slash');
        toggle.classList.add('fa-eye');
    }
}

function handleLogin(event) {
    event.preventDefault();
    
    // Hide any existing messages
    hideMessages();
    
    // Validate form
    const isEmailValid = validateEmail();
    const isPasswordValid = validatePassword();
    
    if (!isEmailValid || !isPasswordValid) {
        document.getElementById('errorMessage').style.display = 'block';
        document.getElementById('errorText').textContent = 'Please fix the errors below';
        return;
    }
    
    // Show loading state
    const loginBtn = document.getElementById('loginBtn');
    const btnText = document.getElementById('btnText');
    
    loginBtn.disabled = true;
    btnText.textContent = 'Logging in...';
    
    // Simulate API call
    setTimeout(() => {
        // Simulate successful login
        document.getElementById('successMessage').style.display = 'block';

        // Persist a simple session flag. Honor "Remember me" if checked.
        const remember = document.getElementById('rememberMe');
        try {
            if (remember && remember.checked) {
                localStorage.setItem('isLoggedIn', '1');
            } else {
                // fallback to sessionStorage for non-persistent session
                sessionStorage.setItem('isLoggedIn', '1');
            }
        } catch (e) {
            // If storage is unavailable, still proceed with redirect
            console.warn('Storage unavailable, proceeding without persistent session');
        }

        // Reset button
        loginBtn.disabled = false;
        btnText.textContent = 'Login to Account';

        // Redirect after delay
        setTimeout(() => {
            showToast('Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/';
            }, 500);
        }, 500);

    }, 1500);
}

function handleSignup(event) {
    event.preventDefault();
    
    // Hide any existing messages
    hideMessages();
    
    // Validate form
    const isNameValid = validateName();
    const isEmailValid = validateEmail();
    const isPasswordValid = validatePassword();
    const isPasswordMatch = validatePasswordMatch();
    
    if (!isNameValid || !isEmailValid || !isPasswordValid || !isPasswordMatch) {
        document.getElementById('errorMessage').style.display = 'block';
        document.getElementById('errorText').textContent = 'Please fix the errors below';
        return;
    }
    
    // Show loading state
    const signupBtn = document.getElementById('signupBtn');
    const btnText = document.getElementById('btnText');
    
    signupBtn.disabled = true;
    btnText.textContent = 'Creating account...';
    
    // Simulate API call
    setTimeout(() => {
        // Simulate successful registration
        document.getElementById('successMessage').style.display = 'block';
        document.getElementById('successText').textContent = 'Registration successful! Redirecting to login...';
        
        // Reset button
        signupBtn.disabled = false;
        btnText.textContent = 'Create Account';
        
        // Redirect after delay
        setTimeout(() => {
            showToast('Account created successfully!', 'success');
            setTimeout(() => {
                window.location.href = '/login';
            }, 500);
        }, 500);
        
    }, 1500);
}

function validateLoginForm() {
    hideMessages();
    const isEmailValid = validateEmail();
    const isPasswordValid = validatePassword();
    if (!isEmailValid || !isPasswordValid) {
        const msg = document.getElementById('errorMessage');
        const txt = document.getElementById('errorText');
        if (msg) msg.style.display = 'block';
        if (txt) txt.textContent = 'Please enter a valid email and password';
        return false;
    }
    return true;
}

function validateSignupForm() {
    hideMessages();
    const isNameValid = validateName();
    const isEmailValid = validateEmail();
    const isPasswordValid = validatePassword();
    const isPasswordMatch = validatePasswordMatch();
    if (!isNameValid || !isEmailValid || !isPasswordValid || !isPasswordMatch) {
        const msg = document.getElementById('errorMessage');
        const txt = document.getElementById('errorText');
        if (msg) msg.style.display = 'block';
        if (txt) txt.textContent = 'Please fix errors below';
        return false;
    }
    return true;
}

function showToast(message, type) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} mr-2"></i>
        ${message}
    `;
    
    // Add to page
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Hide and remove after delay
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

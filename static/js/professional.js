/**
 * AI Hadith Authenticator - Professional JavaScript Framework
 * Enterprise-grade interactions and animations
 */

class ProfessionalUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupThemeSystem();
        this.setupAnimations();
        this.setupNavigation();
        this.setupInteractions();
        this.setupFormValidation();
        this.setupTooltips();
        this.setupNotifications();
        this.setupScrollEffects();
        this.setupKeyboardNavigation();
    }

    // Theme Management System
    setupThemeSystem() {
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Apply saved theme on load
        this.applySavedTheme();
    }

    toggleTheme() {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update icon
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.textContent = newTheme === 'dark' ? 'light_mode' : 'dark_mode';
        }
        
        // Add transition effect
        html.style.transition = 'background-color 0.3s ease';
        
        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: newTheme } }));
    }

    applySavedTheme() {
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = savedTheme || (prefersDark ? 'dark' : 'light');
        
        document.documentElement.setAttribute('data-theme', theme);
        
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.textContent = theme === 'dark' ? 'light_mode' : 'dark_mode';
        }
    }

    // Advanced Animation System
    setupAnimations() {
        this.setupIntersectionObserver();
        this.setupScrollAnimations();
        this.setupHoverEffects();
        this.setupLoadingAnimations();
    }

    setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target);
                }
            });
        }, observerOptions);

        // Observe all animated elements
        document.querySelectorAll('.animate-fade-in, .animate-slide-in-left, .animate-slide-in-right').forEach(el => {
            observer.observe(el);
        });
    }

    animateElement(element) {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
        
        // Add stagger effect for multiple elements
        const delay = element.dataset.delay || 0;
        element.style.transitionDelay = `${delay}ms`;
    }

    setupScrollAnimations() {
        let ticking = false;
        
        const updateScrollEffects = () => {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('.parallax');
            
            parallaxElements.forEach(el => {
                const speed = el.dataset.speed || 0.5;
                const yPos = -(scrolled * speed);
                el.style.transform = `translateY(${yPos}px)`;
            });
            
            ticking = false;
        };

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateScrollEffects);
                ticking = true;
            }
        });
    }

    setupHoverEffects() {
        // Card hover effects
        document.querySelectorAll('.card, .feature-card').forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                this.addHoverEffect(e.target);
            });
            
            card.addEventListener('mouseleave', (e) => {
                this.removeHoverEffect(e.target);
            });
        });
    }

    addHoverEffect(element) {
        element.style.transform = 'translateY(-8px) scale(1.02)';
        element.style.boxShadow = '0 25px 50px -12px rgba(0, 0, 0, 0.25)';
    }

    removeHoverEffect(element) {
        element.style.transform = '';
        element.style.boxShadow = '';
    }

    setupLoadingAnimations() {
        // Loading states for buttons
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                if (btn.dataset.loading !== 'false') {
                    this.setButtonLoading(btn, true);
                }
            });
        });
    }

    setButtonLoading(button, loading) {
        if (loading) {
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = '<span class="animate-spin">refresh</span> Loading...';
            button.disabled = true;
        } else {
            button.innerHTML = button.dataset.originalText;
            button.disabled = false;
            delete button.dataset.originalText;
        }
    }

    // Navigation System
    setupNavigation() {
        this.setupMobileMenu();
        this.setupActiveNavigation();
        this.setupSmoothScrolling();
        this.setupBreadcrumbNavigation();
    }

    setupMobileMenu() {
        const toggle = document.getElementById('navbarToggle');
        const menu = document.getElementById('navbarNav');
        
        if (toggle && menu) {
            toggle.addEventListener('click', () => {
                menu.classList.toggle('active');
                toggle.classList.toggle('active');
            });
            
            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!toggle.contains(e.target) && !menu.contains(e.target)) {
                    menu.classList.remove('active');
                    toggle.classList.remove('active');
                }
            });
        }
    }

    setupActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }

    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    setupBreadcrumbNavigation() {
        // Auto-generate breadcrumbs if needed
        this.generateBreadcrumbs();
    }

    generateBreadcrumbs() {
        const breadcrumbContainer = document.getElementById('breadcrumb');
        if (!breadcrumbContainer) return;
        
        const path = window.location.pathname;
        const pathSegments = path.split('/').filter(segment => segment);
        
        let breadcrumbHTML = '<nav class="breadcrumb"><ol class="breadcrumb-list">';
        breadcrumbHTML += '<li><a href="/">Home</a></li>';
        
        pathSegments.forEach((segment, index) => {
            const url = '/' + pathSegments.slice(0, index + 1).join('/');
            const name = this.formatBreadcrumbName(segment);
            const isLast = index === pathSegments.length - 1;
            
            if (isLast) {
                breadcrumbHTML += `<li class="active">${name}</li>`;
            } else {
                breadcrumbHTML += `<li><a href="${url}">${name}</a></li>`;
            }
        });
        
        breadcrumbHTML += '</ol></nav>';
        breadcrumbContainer.innerHTML = breadcrumbHTML;
    }

    formatBreadcrumbName(segment) {
        return segment.charAt(0).toUpperCase() + segment.slice(1).replace(/-/g, ' ');
    }

    // Interactive Components
    setupInteractions() {
        this.setupTabs();
        this.setupAccordions();
        this.setupModals();
        this.setupDropdowns();
        this.setupCarousels();
    }

    setupTabs() {
        document.querySelectorAll('[data-tabs]').forEach(container => {
            const tabs = container.querySelectorAll('[data-tab]');
            const panels = container.querySelectorAll('[data-panel]');
            
            tabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    const targetPanel = tab.dataset.tab;
                    
                    // Update active states
                    tabs.forEach(t => t.classList.remove('active'));
                    panels.forEach(p => p.classList.remove('active'));
                    
                    tab.classList.add('active');
                    container.querySelector(`[data-panel="${targetPanel}"]`).classList.add('active');
                });
            });
        });
    }

    setupAccordions() {
        document.querySelectorAll('[data-accordion]').forEach(accordion => {
            const triggers = accordion.querySelectorAll('[data-accordion-trigger]');
            
            triggers.forEach(trigger => {
                trigger.addEventListener('click', () => {
                    const content = trigger.nextElementSibling;
                    const isOpen = trigger.classList.contains('active');
                    
                    // Close all accordions in the same group
                    triggers.forEach(t => {
                        t.classList.remove('active');
                        t.nextElementSibling.style.maxHeight = '0';
                    });
                    
                    // Open clicked accordion if it wasn't open
                    if (!isOpen) {
                        trigger.classList.add('active');
                        content.style.maxHeight = content.scrollHeight + 'px';
                    }
                });
            });
        });
    }

    setupModals() {
        const modals = document.querySelectorAll('[data-modal]');
        
        modals.forEach(modal => {
            const triggers = document.querySelectorAll(`[data-modal-target="${modal.id}"]`);
            const closeBtn = modal.querySelector('[data-modal-close]');
            
            triggers.forEach(trigger => {
                trigger.addEventListener('click', () => this.openModal(modal));
            });
            
            closeBtn?.addEventListener('click', () => this.closeModal(modal));
            
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal);
                }
            });
        });
    }

    openModal(modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        modal.setAttribute('aria-hidden', 'false');
    }

    closeModal(modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        modal.setAttribute('aria-hidden', 'true');
    }

    setupDropdowns() {
        document.querySelectorAll('[data-dropdown]').forEach(dropdown => {
            const trigger = dropdown.querySelector('[data-dropdown-trigger]');
            
            trigger.addEventListener('click', (e) => {
                e.stopPropagation();
                const isOpen = dropdown.classList.contains('active');
                
                // Close all other dropdowns
                document.querySelectorAll('[data-dropdown]').forEach(d => {
                    d.classList.remove('active');
                });
                
                if (!isOpen) {
                    dropdown.classList.add('active');
                }
            });
        });
        
        // Close dropdowns when clicking outside
        document.addEventListener('click', () => {
            document.querySelectorAll('[data-dropdown]').forEach(d => {
                d.classList.remove('active');
            });
        });
    }

    setupCarousels() {
        document.querySelectorAll('[data-carousel]').forEach(carousel => {
            this.initCarousel(carousel);
        });
    }

    initCarousel(carousel) {
        const items = carousel.querySelectorAll('[data-carousel-item]');
        const prevBtn = carousel.querySelector('[data-carousel-prev]');
        const nextBtn = carousel.querySelector('[data-carousel-next]');
        const indicators = carousel.querySelectorAll('[data-carousel-indicator]');
        
        let currentIndex = 0;
        
        const goToSlide = (index) => {
            items.forEach((item, i) => {
                item.classList.toggle('active', i === index);
            });
            
            indicators.forEach((indicator, i) => {
                indicator.classList.toggle('active', i === index);
            });
            
            currentIndex = index;
        };
        
        const nextSlide = () => {
            const nextIndex = (currentIndex + 1) % items.length;
            goToSlide(nextIndex);
        };
        
        const prevSlide = () => {
            const prevIndex = (currentIndex - 1 + items.length) % items.length;
            goToSlide(prevIndex);
        };
        
        prevBtn?.addEventListener('click', prevSlide);
        nextBtn?.addEventListener('click', nextSlide);
        
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => goToSlide(index));
        });
        
        // Auto-play
        const autoPlay = carousel.dataset.carouselAutoplay;
        if (autoPlay) {
            setInterval(nextSlide, parseInt(autoPlay) * 1000);
        }
    }

    // Form Validation
    setupFormValidation() {
        document.querySelectorAll('form[data-validate]').forEach(form => {
            this.setupFormValidationListeners(form);
        });
    }

    setupFormValidationListeners(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
        
        form.addEventListener('submit', (e) => {
            if (!this.validateForm(form)) {
                e.preventDefault();
            }
        });
    }

    validateField(field) {
        const rules = field.dataset.rules?.split('|') || [];
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';
        
        rules.forEach(rule => {
            if (!isValid) return;
            
            const [ruleName, ruleValue] = rule.split(':');
            
            switch (ruleName) {
                case 'required':
                    if (!value) {
                        isValid = false;
                        errorMessage = 'This field is required';
                    }
                    break;
                case 'email':
                    if (!this.isValidEmail(value)) {
                        isValid = false;
                        errorMessage = 'Please enter a valid email address';
                    }
                    break;
                case 'min':
                    if (value.length < parseInt(ruleValue)) {
                        isValid = false;
                        errorMessage = `Minimum ${ruleValue} characters required`;
                    }
                    break;
                case 'max':
                    if (value.length > parseInt(ruleValue)) {
                        isValid = false;
                        errorMessage = `Maximum ${ruleValue} characters allowed`;
                    }
                    break;
            }
        });
        
        if (!isValid) {
            this.showFieldError(field, errorMessage);
        }
        
        return isValid;
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    showFieldError(field, message) {
        field.classList.add('error');
        
        let errorElement = field.nextElementSibling;
        if (!errorElement || !errorElement.classList.contains('error-message')) {
            errorElement = document.createElement('div');
            errorElement.className = 'error-message';
            field.parentNode.insertBefore(errorElement, field.nextSibling);
        }
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    clearFieldError(field) {
        field.classList.remove('error');
        const errorElement = field.nextElementSibling;
        if (errorElement && errorElement.classList.contains('error-message')) {
            errorElement.style.display = 'none';
        }
    }

    validateForm(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    // Tooltip System
    setupTooltips() {
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            this.initTooltip(element);
        });
    }

    initTooltip(element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = element.dataset.tooltip;
        tooltip.setAttribute('role', 'tooltip');
        
        document.body.appendChild(tooltip);
        
        const showTooltip = (e) => {
            const rect = element.getBoundingClientRect();
            tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
            tooltip.classList.add('active');
        };
        
        const hideTooltip = () => {
            tooltip.classList.remove('active');
        };
        
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
        element.addEventListener('focus', showTooltip);
        element.addEventListener('blur', hideTooltip);
    }

    // Notification System
    setupNotifications() {
        this.notificationContainer = this.createNotificationContainer();
    }

    createNotificationContainer() {
        const container = document.createElement('div');
        container.className = 'notification-container';
        container.setAttribute('aria-live', 'polite');
        document.body.appendChild(container);
        return container;
    }

    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${this.getNotificationIcon(type)}</span>
                <span class="notification-message">${message}</span>
                <button class="notification-close" aria-label="Close notification">
                    <span>close</span>
                </button>
            </div>
        `;
        
        this.notificationContainer.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('active'), 10);
        
        // Auto dismiss
        const dismissTimeout = setTimeout(() => {
            this.dismissNotification(notification);
        }, duration);
        
        // Manual dismiss
        notification.querySelector('.notification-close').addEventListener('click', () => {
            clearTimeout(dismissTimeout);
            this.dismissNotification(notification);
        });
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check_circle',
            error: 'error',
            warning: 'warning',
            info: 'info'
        };
        return icons[type] || icons.info;
    }

    dismissNotification(notification) {
        notification.classList.remove('active');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }

    // Scroll Effects
    setupScrollEffects() {
        this.setupNavbarScroll();
        this.setupScrollProgress();
        this.setupBackToTop();
    }

    setupNavbarScroll() {
        const navbar = document.getElementById('navbar');
        if (!navbar) return;
        
        let lastScroll = 0;
        
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            // Hide/show navbar on scroll
            if (currentScroll > lastScroll && currentScroll > 100) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            
            // Add background on scroll
            if (currentScroll > 50) {
                navbar.style.background = 'rgba(15, 118, 110, 0.95)';
                navbar.style.backdropFilter = 'blur(20px)';
            } else {
                navbar.style.background = '';
                navbar.style.backdropFilter = '';
            }
            
            lastScroll = currentScroll;
        });
    }

    setupScrollProgress() {
        const progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        document.body.appendChild(progressBar);
        
        window.addEventListener('scroll', () => {
            const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollProgress = (window.pageYOffset / scrollHeight) * 100;
            progressBar.style.width = `${scrollProgress}%`;
        });
    }

    setupBackToTop() {
        const backToTopBtn = document.createElement('button');
        backToTopBtn.className = 'back-to-top';
        backToTopBtn.innerHTML = '<span>arrow_upward</span>';
        backToTopBtn.setAttribute('aria-label', 'Back to top');
        document.body.appendChild(backToTopBtn);
        
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 500) {
                backToTopBtn.classList.add('active');
            } else {
                backToTopBtn.classList.remove('active');
            }
        });
        
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Keyboard Navigation
    setupKeyboardNavigation() {
        this.setupKeyboardShortcuts();
        this.setupFocusManagement();
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.openSearchModal();
            }
            
            // Escape to close modals
            if (e.key === 'Escape') {
                this.closeAllModals();
            }
            
            // Alt + T for theme toggle
            if (e.altKey && e.key === 't') {
                e.preventDefault();
                this.toggleTheme();
            }
        });
    }

    openSearchModal() {
        // Implementation for search modal
        console.log('Search modal opened');
    }

    closeAllModals() {
        document.querySelectorAll('[data-modal].active').forEach(modal => {
            this.closeModal(modal);
        });
    }

    setupFocusManagement() {
        // Trap focus within modals
        document.querySelectorAll('[data-modal]').forEach(modal => {
            const focusableElements = modal.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            
            if (focusableElements.length > 0) {
                const firstElement = focusableElements[0];
                const lastElement = focusableElements[focusableElements.length - 1];
                
                modal.addEventListener('keydown', (e) => {
                    if (e.key === 'Tab') {
                        if (e.shiftKey) {
                            if (document.activeElement === firstElement) {
                                e.preventDefault();
                                lastElement.focus();
                            }
                        } else {
                            if (document.activeElement === lastElement) {
                                e.preventDefault();
                                firstElement.focus();
                            }
                        }
                    }
                });
            }
        });
    }
}

// Initialize the professional UI
document.addEventListener('DOMContentLoaded', () => {
    window.professionalUI = new ProfessionalUI();
    
    // Show welcome notification for first-time users
    if (!localStorage.getItem('visited')) {
        setTimeout(() => {
            window.professionalUI.showNotification(
                'Welcome to AI Hadith Authenticator! Explore our advanced features.',
                'success',
                8000
            );
            localStorage.setItem('visited', 'true');
        }, 1000);
    }
});

// Export for external use
window.ProfessionalUI = ProfessionalUI;

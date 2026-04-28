document.addEventListener('DOMContentLoaded', () => {
  // Initialize all components
  initThemeToggle();
  initMobileMenu();
  initScrollAnimations();
  initParticleBackground();
  initCardGlow();
  initNavbarScroll();
  initSmoothScroll();
  initCounters();
});

// Theme Toggle
function initThemeToggle() {
  const toggle = document.getElementById('themeToggle');
  const html = document.documentElement;
  
  // Check saved theme or default to dark
  const savedTheme = localStorage.getItem('theme') || 'dark';
  html.setAttribute('data-theme', savedTheme);
  
  toggle?.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });
}

// Mobile Menu
function initMobileMenu() {
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  
  navToggle?.addEventListener('click', () => {
    navToggle.classList.toggle('active');
    navLinks?.classList.toggle('active');
  });
  
  // Close menu on link click
  navLinks?.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navToggle.classList.remove('active');
      navLinks.classList.remove('active');
    });
  });
}

// Scroll Animations
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll('[data-animate]');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const delay = entry.target.dataset.delay || 0;
        setTimeout(() => {
          entry.target.classList.add('animate-in');
        }, delay);
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });
  
  animatedElements.forEach(el => observer.observe(el));
}

// Particle Background
function initParticleBackground() {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  let particles = [];
  let animationId;
  let isActive = true;
  
  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  
  resize();
  window.addEventListener('resize', resize, { passive: true });
  
  class Particle {
    constructor() {
      this.reset();
    }
    
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 2 + 1;
      this.speedX = (Math.random() - 0.5) * 0.5;
      this.speedY = (Math.random() - 0.5) * 0.5;
      this.opacity = Math.random() * 0.5 + 0.2;
    }
    
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      
      if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
        this.reset();
      }
    }
    
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(20, 184, 166, ${this.opacity})`;
      ctx.fill();
    }
  }
  
  // Create particles
  const particleCount = window.matchMedia('(pointer: coarse)').matches ? 15 : 30;
  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }
  
  let frameCount = 0;
  function animate() {
    if (!isActive) return;
    
    frameCount++;
    // Render every 2nd frame for performance (30fps)
    if (frameCount % 2 === 0) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach(particle => {
        particle.update();
        particle.draw();
      });
      
      // Draw connections
      particles.forEach((p1, i) => {
        if (i % 3 !== 0) return; // Only check every 3rd particle
        
        particles.slice(i + 1).forEach((p2, j) => {
          if (j % 3 !== 0) return;
          
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < 100) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(20, 184, 166, ${0.1 * (1 - distance / 100)})`;
            ctx.lineWidth = 1;
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        });
      });
    }
    
    animationId = requestAnimationFrame(animate);
  }
  
  animate();
  
  // Pause when tab is hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      isActive = false;
      cancelAnimationFrame(animationId);
    } else {
      isActive = true;
      animate();
    }
  });
}

// Card Glow Effect
function initCardGlow() {
  const cards = document.querySelectorAll('.dashboard-card, .feature-card-large');
  
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      card.style.setProperty('--mouse-x', `${x}%`);
      card.style.setProperty('--mouse-y', `${y}%`);
    });
  });
}

// Navbar Scroll Effect
function initNavbarScroll() {
  const navbar = document.getElementById('navbar');
  let lastScroll = 0;
  
  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
      navbar.style.background = 'rgba(12, 10, 9, 0.95)';
      navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.3)';
    } else {
      navbar.style.background = 'rgba(12, 10, 9, 0.8)';
      navbar.style.boxShadow = 'none';
    }
    
    lastScroll = currentScroll;
  }, { passive: true });
}

// Smooth Scroll
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
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

// Animated Counters
function initCounters() {
  const counters = document.querySelectorAll('[data-count]');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = entry.target;
        const end = parseInt(target.dataset.count);
        const duration = 2000;
        const start = 0;
        const startTime = performance.now();
        
        function updateCounter(currentTime) {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          
          // Easing function
          const easeOutQuart = 1 - Math.pow(1 - progress, 4);
          const current = Math.floor(easeOutQuart * (end - start) + start);
          
          target.textContent = current.toLocaleString() + (target.textContent.includes('%') ? '%' : target.textContent.includes('+') ? '+' : '');
          
          if (progress < 1) {
            requestAnimationFrame(updateCounter);
          }
        }
        
        requestAnimationFrame(updateCounter);
        observer.unobserve(target);
      }
    });
  }, { threshold: 0.5 });
  
  counters.forEach(counter => observer.observe(counter));
}

// Hover effect enhancement for buttons
document.querySelectorAll('[data-hover]').forEach(el => {
  el.addEventListener('mouseenter', () => {
    el.style.transform = 'translateY(-2px)';
  });
  
  el.addEventListener('mouseleave', () => {
    el.style.transform = 'translateY(0)';
  });
});

// Alert/Notification System
// FAQ Toggle Function
window.toggleFaq = (button) => {
  const faqItem = button.parentElement;
  const wasActive = faqItem.classList.contains('active');
  
  // Close all FAQ items
  document.querySelectorAll('.faq-item').forEach(item => {
    item.classList.remove('active');
  });
  
  // Open clicked item if it wasn't active
  if (!wasActive) {
    faqItem.classList.add('active');
  }
};

window.showAlert = (message, type = 'info') => {
  const container = document.getElementById('alertContainer') || document.body;
  const alert = document.createElement('div');
  alert.className = `alert alert-${type}`;
  alert.innerHTML = `
    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
    <span>${message}</span>
  `;
  
  Object.assign(alert.style, {
    position: 'fixed',
    top: '100px',
    right: '20px',
    padding: '16px 24px',
    background: type === 'success' ? 'rgba(34, 197, 94, 0.9)' : type === 'error' ? 'rgba(239, 68, 68, 0.9)' : 'rgba(59, 130, 246, 0.9)',
    color: 'white',
    borderRadius: '12px',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    fontWeight: '500',
    boxShadow: '0 10px 30px rgba(0, 0, 0, 0.3)',
    zIndex: '9999',
    transform: 'translateX(150%)',
    transition: 'transform 0.3s ease'
  });
  
  container.appendChild(alert);
  
  requestAnimationFrame(() => {
    alert.style.transform = 'translateX(0)';
  });
  
  setTimeout(() => {
    alert.style.transform = 'translateX(150%)';
    setTimeout(() => alert.remove(), 300);
  }, 4000);
};

// Mobile Swipe Carousels
function initSwipeCarousels() {
  const isMobile = window.innerWidth <= 768;

  // Helper function to setup swipe carousel
  const setupCarousel = (containerSelector, indicatorId, cardSelector) => {
    const container = document.querySelector(containerSelector);
    const indicator = document.getElementById(indicatorId);

    if (!container || !indicator) return;

    const dots = indicator.querySelectorAll('.swipe-dot');
    const cards = container.querySelectorAll(cardSelector);

    if (cards.length === 0 || dots.length === 0) return;

    // Update dots on scroll
    container.addEventListener('scroll', () => {
      const scrollLeft = container.scrollLeft;
      const cardWidth = cards[0]?.offsetWidth + 16; // card width + gap
      const activeIndex = Math.min(Math.round(scrollLeft / cardWidth), dots.length - 1);

      dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === activeIndex);
      });
    });

    // Click dots to scroll
    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        const cardWidth = cards[0]?.offsetWidth + 16;
        container.scrollTo({
          left: cardWidth * index,
          behavior: 'smooth'
        });
      });
    });
  };

  // Setup all carousels
  setupCarousel('.testimonials-grid', 'testimonials-indicator', '.testimonial-card');
  setupCarousel('.features-grid', 'features-indicator', '.feature-card-large');
  setupCarousel('.tech-features', 'tech-indicator', '.tech-item');
}

// Initialize on load and resize
window.addEventListener('load', initSwipeCarousels);
window.addEventListener('resize', initSwipeCarousels);

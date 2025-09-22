// Performance optimization: Use passive event listeners where possible
const passiveSupported = (() => {
    let passiveSupported = false;
    try {
        const options = {
            get passive() {
                passiveSupported = true;
                return false;
            }
        };
        window.addEventListener("test", null, options);
        window.removeEventListener("test", null, options);
    } catch(err) {
        passiveSupported = false;
    }
    return passiveSupported;
})();

document.addEventListener('DOMContentLoaded', () => {


    // Header scroll effect with throttling for better performance
    const header = document.querySelector('.header');
    const headerHeight = header.offsetHeight;
    let ticking = false;

    function updateHeader() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateHeader);
            ticking = true;
        }
    }

    window.addEventListener('scroll', requestTick, passiveSupported ? { passive: true } : false);

    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-link[data-target]');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            const targetId = link.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                const offsetTop = targetSection.offsetTop - headerHeight;

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Back to top button with throttling
    const backToTopBtn = document.getElementById('back-to-top');
    let backToTopTicking = false;

    function updateBackToTop() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
        backToTopTicking = false;
    }

    function requestBackToTopTick() {
        if (!backToTopTicking) {
            requestAnimationFrame(updateBackToTop);
            backToTopTicking = true;
        }
    }

    window.addEventListener('scroll', requestBackToTopTick, passiveSupported ? { passive: true } : false);

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.agent, .blog-card, .content-box');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Active navigation highlighting
    const sections = document.querySelectorAll('.section');

    const navObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');

                // Remove active class from all nav links
                navLinks.forEach(link => link.classList.remove('active'));

                // Add active class to current nav link
                const activeLink = document.querySelector(`[data-target="${id}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    }, {
        threshold: 0.3
    });

    sections.forEach(section => {
        navObserver.observe(section);
    });

    // Blog modal functionality
    const modal = document.getElementById("blogModal");
    const modalTitle = document.getElementById("modalTitle");
    const modalContent = document.getElementById("modalContent");
    const modalImage = document.getElementById("modalImage");
    const modalDate = document.getElementById("modalDate");
    const closeBtn = document.querySelector(".close-button");

    // Open modal when read more button is clicked
    document.querySelectorAll(".read-more").forEach(button => {
        button.addEventListener("click", function () {
            modalTitle.textContent = this.getAttribute("data-title");
            modalContent.innerHTML = this.getAttribute("data-content");
            modalImage.src = this.getAttribute("data-image");
            modalImage.alt = this.getAttribute("data-title");
            modalDate.textContent = this.getAttribute("data-date");

            modal.style.display = "block";
            modal.setAttribute("aria-hidden", "false");
            document.body.style.overflow = "hidden";
        });
    });

    // Close modal
    function closeModal() {
        modal.style.display = "none";
        modal.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "auto";
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", closeModal);
    }

    // Close modal when clicking outside
    modal?.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Close modal with Escape key
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && modal.style.display === "block") {
            closeModal();
        }
    });

    // Toast notification system
    function showToast(message, type = 'success') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icon = type === 'success' ? '✓' : '✕';

        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-icon">${icon}</span>
                <p class="toast-message">${message}</p>
                <button class="toast-close" aria-label="Close notification">&times;</button>
            </div>
            <div class="toast-progress"></div>
        `;

        toastContainer.appendChild(toast);

        // Show toast with animation
        setTimeout(() => toast.classList.add('show'), 100);

        // Auto hide after 5 seconds
        const autoHideTimer = setTimeout(() => hideToast(toast), 5000);

        // Manual close button
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            clearTimeout(autoHideTimer);
            hideToast(toast);
        });

        function hideToast(toastElement) {
            toastElement.classList.add('hide');
            setTimeout(() => {
                if (toastElement.parentNode) {
                    toastElement.parentNode.removeChild(toastElement);
                }
            }, 400);
        }
    }

    // Contact form handling with AJAX
    const contactForm = document.getElementById("contact-form");
    if (contactForm) {
        contactForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevent default form submission
            e.stopPropagation(); // Stop event bubbling

            console.log('Form submission intercepted'); // Debug log

            const submitButton = this.querySelector(".submit-button");
            const buttonText = submitButton.querySelector(".button-text");
            const buttonLoading = submitButton.querySelector(".button-loading");
            const formData = new FormData(this);

            // Show loading state
            buttonText.style.display = "none";
            buttonLoading.style.display = "inline-flex";
            submitButton.disabled = true;

            // Submit form via AJAX
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                console.log('Response received:', response.status); // Debug log
                return response.json();
            })
            .then(data => {
                console.log('Data received:', data); // Debug log
                if (data.success) {
                    showToast(data.message, 'success');
                    this.reset(); // Clear the form

                    // Scroll to top of contact section smoothly to show the toast
                    const contactSection = document.getElementById('contact-us');
                    if (contactSection) {
                        contactSection.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Something went wrong. Please try again later.', 'error');
            })
            .finally(() => {
                // Reset button state
                buttonText.style.display = "inline";
                buttonLoading.style.display = "none";
                submitButton.disabled = false;
            });

            return false; // Extra prevention of default behavior
        });
    }

    // Enhanced form validation
    const inputs = document.querySelectorAll('.input-field');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateField(this);
            }
        });
    });

    function validateField(field) {
        const value = field.value.trim();
        const fieldType = field.type;
        let isValid = true;
        let errorMessage = '';

        // Remove existing error styling
        field.classList.remove('error');
        const existingError = field.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Validate based on field type
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        } else if (fieldType === 'email' && value && !isValidEmail(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }

        if (!isValid) {
            field.classList.add('error');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = errorMessage;
            field.parentNode.appendChild(errorDiv);
        }

        return isValid;
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Smooth reveal animations for elements
    const revealElements = document.querySelectorAll('.agent, .blog-card, .content-box');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100); // Stagger the animations
                revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        revealObserver.observe(el);
    });

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.submit-button, .read-more, .page-link');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Performance optimization: Lazy load images
    const images = document.querySelectorAll('img[loading="lazy"]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }
});

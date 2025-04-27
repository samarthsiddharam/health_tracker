/**
 * Main JavaScript File for Health Tracker Application
 * 
 * Handles:
 * - Mobile navigation
 * - Form interactions
 * - Loading states
 * - AJAX requests
 * - UI enhancements
 */

// Wait for DOM to be fully loaded before executing scripts
document.addEventListener('DOMContentLoaded', function() {
    // ======================
    // MOBILE NAVIGATION
    // ======================
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.querySelector('.sidebar');
    
    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-show');
            this.setAttribute('aria-expanded', 
                sidebar.classList.contains('mobile-show'));
        });
    }

    // ======================
    // FORM ENHANCEMENTS
    // ======================
    const formInputs = document.querySelectorAll('.form-group input, .form-group select, .form-group textarea');
    
    formInputs.forEach(input => {
        // Add focus styles
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        // Remove focus styles if empty
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Initialize focused state for pre-filled inputs
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });

    // ======================
    // PASSWORD VISIBILITY TOGGLE
    // ======================
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const icon = this.querySelector('i');
            const isPassword = input.type === 'password';
            
            // Toggle input type and icon
            input.type = isPassword ? 'text' : 'password';
            icon.classList.toggle('fa-eye-slash', isPassword);
            icon.classList.toggle('fa-eye', !isPassword);
            
            // Update ARIA label for accessibility
            this.setAttribute('aria-label', 
                isPassword ? 'Hide password' : 'Show password');
        });
    });

    // ======================
    // MESSAGE HANDLING
    // ======================
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Fade out alerts after 5 seconds
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300); // Match CSS transition duration
        }, 5000);
    });

    // Manual message dismissal
    document.querySelectorAll('[data-dismiss="alert"]').forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.alert').style.display = 'none';
        });
    });

    // ======================
    // FORM SUBMISSION HANDLING
    // ======================
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            showLoading();
        });
    });

    // Prevent form resubmission on page refresh
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }
});

// ======================
// LOGOUT CONFIRMATION
// ======================
document.querySelectorAll('.logout-link').forEach(link => {
    link.addEventListener('click', function(e) {
        if (!confirm('Are you sure you want to logout?')) {
            e.preventDefault();
        }
    });
});

// ======================
// LOADING STATE MANAGEMENT
// ======================
/**
 * Shows loading spinner and overlay
 */
function showLoading() {
    const spinner = document.getElementById('loading-spinner');
    const overlay = document.querySelector('.loading-overlay');
    
    if (spinner) spinner.classList.add('active');
    if (overlay) overlay.classList.add('active');
}

/**
 * Hides loading spinner and overlay
 */
function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    const overlay = document.querySelector('.loading-overlay');
    
    if (spinner) spinner.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
}

// ======================
// AJAX REQUEST HANDLER
// ======================
/**
 * Makes an AJAX request to the server
 * @param {string} url - Endpoint URL
 * @param {string} method - HTTP method (GET, POST, etc.)
 * @param {object} data - Data to send
 * @param {function} callback - Callback function to handle response
 */
function makeAjaxRequest(url, method, data, callback) {
    showLoading();
    
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') || '',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        callback(data);
    })
    .catch(error => {
        console.error('AJAX Error:', error);
        showMessage('error', 'An error occurred. Please try again.');
    })
    .finally(() => {
        hideLoading();
    });
}

// ======================
// UTILITY FUNCTIONS
// ======================
/**
 * Gets cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value or null if not found
 */
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return decodeURIComponent(cookieValue);
        }
    }
    return null;
}

/**
 * Displays a user message
 * @param {string} type - Message type (success, error, warning, info)
 * @param {string} text - Message content
 */
function showMessage(type, text) {
    const container = document.querySelector('.messages-container') || document.body;
    const message = document.createElement('div');
    message.className = `alert alert-${type}`;
    message.innerHTML = `
        <i class="fas fa-${getMessageIcon(type)}"></i>
        ${text}
        <button class="close" aria-label="Close">&times;</button>
    `;
    container.prepend(message);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 300);
    }, 5000);
}

/**
 * Gets appropriate icon for message type
 * @param {string} type - Message type
 * @returns {string} Icon class suffix
 */
function getMessageIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}
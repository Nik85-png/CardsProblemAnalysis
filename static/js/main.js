// Main JavaScript Utilities for Flask Card Analysis Application

/**
 * Show loading spinner in an element
 */
function showLoading(element) {
    element.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading...</p>
        </div>
    `;
    element.style.display = 'block';
}

/**
 * Hide an element
 */
function hideElement(element) {
    element.style.display = 'none';
}

/**
 * Show an element
 */
function showElement(element) {
    element.style.display = 'block';
}

/**
 * Fetch JSON data from API
 */
async function fetchJSON(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

/**
 * Show error message in element
 */
function showError(element, message) {
    element.innerHTML = `
        <div class="error-message" style="padding: 2rem; text-align: center; color: #f44336;">
            <p style="font-size: 1.2rem;">⚠️ ${message}</p>
        </div>
    `;
    element.style.display = 'block';
}

/**
 * Format trial label for display
 */
function formatTrialLabel(trial) {
    return `Participant ${trial.participant}, Trial ${trial.trial} (${trial.moves} moves)`;
}

/**
 * Clear element content
 */
function clearElement(element) {
    element.innerHTML = '';
}

/**
 * Create a DOM element with attributes
 */
function createElement(tag, attributes = {}, content = '') {
    const element = document.createElement(tag);
    
    for (let key in attributes) {
        if (key === 'className') {
            element.className = attributes[key];
        } else {
            element.setAttribute(key, attributes[key]);
        }
    }
    
    if (content) {
        element.innerHTML = content;
    }
    
    return element;
}

function initBackToTopButton() {
    const button = document.getElementById('back-to-top');

    if (!button) {
        return;
    }

    const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const scrollThreshold = 240;

    const updateVisibility = () => {
        button.hidden = window.scrollY < scrollThreshold;
    };

    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: reducedMotionQuery.matches ? 'auto' : 'smooth'
        });
    };

    button.addEventListener('click', scrollToTop);
    window.addEventListener('scroll', updateVisibility, { passive: true });
    updateVisibility();
}

function initNavToggle() {
    const toggle = document.querySelector('.nav-toggle');
    const menu = document.getElementById('nav-menu');
    if (!toggle || !menu) {
        return;
    }

    toggle.addEventListener('click', () => {
        const isOpen = menu.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Close the menu after following a link (mobile)
    menu.addEventListener('click', (event) => {
        if (event.target.closest('a')) {
            menu.classList.remove('is-open');
            toggle.setAttribute('aria-expanded', 'false');
        }
    });
}

if (typeof window !== 'undefined') {
    document.addEventListener('DOMContentLoaded', initBackToTopButton);
    document.addEventListener('DOMContentLoaded', initNavToggle);
}

// Export functions if using modules (optional)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showLoading,
        hideElement,
        showElement,
        fetchJSON,
        showError,
        formatTrialLabel,
        clearElement,
        createElement,
        initBackToTopButton
    };
}

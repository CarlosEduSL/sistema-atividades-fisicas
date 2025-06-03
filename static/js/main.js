// Funções utilitárias globais para o Sistema de Atividades Físicas

// Toast notifications
function showToast(message, type = 'success') {
    const toastId = type === 'success' ? 'successToast' : 'errorToast';
    const messageId = type === 'success' ? 'successMessage' : 'errorMessage';
    
    document.getElementById(messageId).textContent = message;
    
    const toast = new bootstrap.Toast(document.getElementById(toastId));
    toast.show();
}

// Format date to Brazilian format
function formatDateBR(dateString) {
    return new Date(dateString).toLocaleDateString('pt-BR');
}

// Format datetime to Brazilian format
function formatDateTimeBR(dateString) {
    return new Date(dateString).toLocaleString('pt-BR');
}

// Format duration in minutes to readable format
function formatDuration(minutes) {
    if (minutes < 60) {
        return `${minutes} min`;
    }
    
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    
    if (remainingMinutes === 0) {
        return `${hours}h`;
    }
    
    return `${hours}h ${remainingMinutes}min`;
}

// Get intensity badge color
function getIntensityBadgeClass(intensity) {
    const classes = {
        'baixa': 'bg-success',
        'moderada': 'bg-warning text-dark',
        'alta': 'bg-danger'
    };
    return classes[intensity] || 'bg-secondary';
}

// Loading state management
function setLoading(elementId, isLoading = true) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    if (isLoading) {
        element.classList.add('loading');
        element.style.pointerEvents = 'none';
    } else {
        element.classList.remove('loading');
        element.style.pointerEvents = 'auto';
    }
}

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Clear form validation
function clearValidation(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.querySelectorAll('.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
    });
}

// Debounce function for search inputs
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

// Local storage helpers
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function getFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Error reading from localStorage:', error);
        return null;
    }
}

// Network status handling
function handleNetworkError(error) {
    console.error('Network error:', error);
    showToast('Erro de conexão. Verifique sua internet.', 'error');
}

// API request wrapper with error handling
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            handleNetworkError(error);
        } else {
            console.error('API Error:', error);
            showToast(error.message || 'Erro na operação', 'error');
        }
        throw error;
    }
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Enhanced console logging for development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('🏃‍♂️ Sistema de Atividades Físicas - Modo Desenvolvimento');
    
    // Add development helpers to window object
    window.devTools = {
        showToast,
        formatDateBR,
        formatDuration,
        apiRequest,
        saveToLocalStorage,
        getFromLocalStorage
    };
}

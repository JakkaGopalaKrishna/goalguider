// ========== TOAST NOTIFICATIONS ==========
function showToast(message, type = 'success', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideInRight 0.3s ease-out reverse forwards';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// ========== LOGOUT FUNCTION ==========
function logout() {
  if (confirm("Are you sure you want to logout?")) {
    localStorage.removeItem("token");
    showToast("Logged out successfully", "success", 1500);
    setTimeout(() => {
      window.location.href = "login.html";
    }, 500);
  }
}

// ========== FORM VALIDATION ==========
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function validatePassword(password) {
  return password.length >= 6;
}

function validateUsername(username) {
  return username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username);
}

function validateForm(fields) {
  let isValid = true;
  
  fields.forEach(({ id, validation, errorMsg }) => {
    const input = document.getElementById(id);
    const value = input.value.trim();
    const isFieldValid = validation(value);
    
    if (!isFieldValid) {
      input.classList.add('error');
      showErrorMessage(id, errorMsg);
      isValid = false;
    } else {
      input.classList.remove('error');
      hideErrorMessage(id);
    }
  });
  
  return isValid;
}

function showErrorMessage(inputId, message) {
  const input = document.getElementById(inputId);
  const errorEl = input.parentElement.querySelector('.error-message') || createErrorElement(input);
  errorEl.textContent = message;
}

function hideErrorMessage(inputId) {
  const input = document.getElementById(inputId);
  const errorEl = input.parentElement.querySelector('.error-message');
  if (errorEl) errorEl.textContent = '';
}

function createErrorElement(inputElement) {
  const div = document.createElement('div');
  div.className = 'error-message';
  inputElement.parentElement.appendChild(div);
  return div;
}

// ========== LOADING STATE ==========
function setButtonLoading(buttonElement, isLoading) {
  if (!buttonElement) {
    // nothing to toggle (defensive) — avoid uncaught TypeError
    console.warn('setButtonLoading called with null buttonElement');
    return;
  }

  if (isLoading) {
    buttonElement.classList.add('loading');
    buttonElement.disabled = true;
  } else {
    buttonElement.classList.remove('loading');
    buttonElement.disabled = false;
  }
}

// ========== API WRAPPER WITH ERROR HANDLING ==========
async function apiCall(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        ...options.headers
      },
      ...options
    });
    
    if (response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = 'login.html';
      return null;
    }
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'An error occurred');
    }
    
    return await response.json();
  } catch (error) {
    showToast(error.message || 'Network error', 'error');
    throw error;
  }
}

// ========== DEBOUNCE FUNCTION ==========
function debounce(func, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}




// util.js — shared helpers

function stopFormReload(event) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  return false;
}

function redirectTo(path) {
  // Always absolute to avoid file:// issues
  window.location.assign(`http://127.0.0.1:5500/${path}`);
}

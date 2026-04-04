/**
 * SEU Volunteering Platform - Main JavaScript
 * Handles interactivity, forms, and UI enhancements
 */

// ============================================
// 1. Language Switching (Arabic/English)
// ============================================

const languageToggle = document.getElementById('langToggle');
if (languageToggle) {
    languageToggle.addEventListener('click', function() {
        const html = document.documentElement;
        const currentDir = html.getAttribute('dir') || 'ltr';
        const newDir = currentDir === 'ltr' ? 'rtl' : 'ltr';
        const newLang = newDir === 'rtl' ? 'ar' : 'en';
        
        html.setAttribute('dir', newDir);
        html.setAttribute('lang', newLang);
        
        // Update toggle button text
        const langText = document.getElementById('langText');
        if (langText) {
            langText.textContent = newDir === 'rtl' ? 'English' : 'عربي';
        }
        
        // Store preference
        localStorage.setItem('preferredLanguage', newLang);
        localStorage.setItem('preferredDirection', newDir);
        
        // Show notification
        showNotification(newDir === 'rtl' ? 'تم التبديل للعربية' : 'Switched to English', 'info');
    });
    
    // Restore preference on page load
    const savedLang = localStorage.getItem('preferredLanguage') || 'en';
    const savedDir = localStorage.getItem('preferredDirection') || 'ltr';
    document.documentElement.setAttribute('dir', savedDir);
    document.documentElement.setAttribute('lang', savedLang);
    
    if (document.getElementById('langText')) {
        document.getElementById('langText').textContent = savedDir === 'rtl' ? 'English' : 'عربي';
    }
}

// ============================================
// 2. Notification System
// ============================================

function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// ============================================
// 3. Form Validation
// ============================================

function validateForm(formElement) {
    if (formElement.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
        return false;
    }
    return true;
}

document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(event) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (!form.checkValidity()) {
            // prevent submission and clear loading state
            event.preventDefault();
            event.stopPropagation();
            if (submitBtn) setLoadingState(submitBtn, false);
        }
        form.classList.add('was-validated');
    }, false);
});

// reset any stale loading buttons when page loads (e.g. after server returned login page)
window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button[type="submit"]').forEach(btn => setLoadingState(btn, false));
});

// ============================================
// 4. Password Toggle
// ============================================

function setupPasswordToggle() {
    document.querySelectorAll('.togglePassword, #togglePassword').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.parentElement.querySelector('input[type="password"], input[type="text"]');
            const icon = this.querySelector('i');
            
            if (input) {
                if (input.type === 'password') {
                    input.type = 'text';
                    if (icon) {
                        icon.classList.remove('fa-eye');
                        icon.classList.add('fa-eye-slash');
                    }
                } else {
                    input.type = 'password';
                    if (icon) {
                        icon.classList.remove('fa-eye-slash');
                        icon.classList.add('fa-eye');
                    }
                }
            }
        });
    });
}

setupPasswordToggle();

// ============================================
// 5. Opportunity Filters
// ============================================

function filterOpportunities() {
    const categories = Array.from(document.querySelectorAll('.category-filter:checked')).map(cb => cb.value);
    const difficulties = Array.from(document.querySelectorAll('.difficulty-filter:checked')).map(cb => cb.value);
    const searchTerm = document.getElementById('searchInput')?.value.toLowerCase();
    
    const opportunities = document.querySelectorAll('.opportunity-card');
    let visibleCount = 0;
    
    opportunities.forEach(card => {
        let isVisible = true;
        
        // Check category filter
        if (categories.length > 0) {
            const cardCategory = card.getAttribute('data-category');
            isVisible = isVisible && categories.includes(cardCategory);
        }
        
        // Check difficulty filter
        if (difficulties.length > 0) {
            const cardDifficulty = card.getAttribute('data-difficulty');
            isVisible = isVisible && difficulties.includes(cardDifficulty);
        }
        
        // Check search term
        if (searchTerm) {
            const cardText = card.textContent.toLowerCase();
            isVisible = isVisible && cardText.includes(searchTerm);
        }
        
        card.style.display = isVisible ? 'block' : 'none';
        if (isVisible) visibleCount++;
    });
    
    // Update count
    const countElement = document.getElementById('count');
    if (countElement) {
        countElement.textContent = visibleCount;
    }
}

// Setup filter listeners
document.querySelectorAll('.category-filter, .difficulty-filter, .date-filter').forEach(element => {
    element.addEventListener('change', filterOpportunities);
});

const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', filterOpportunities);
}

// ============================================
// 6. Favorite/Save Functionality
// ============================================

document.querySelectorAll('.favorite-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const icon = this.querySelector('i');
        const isFavorited = this.classList.contains('favorited');
        
        if (!isFavorited) {
            this.classList.add('favorited');
            icon.classList.remove('far');
            icon.classList.add('fas');
            icon.classList.add('text-danger');
            showNotification('Added to your favorites!', 'success');
        } else {
            this.classList.remove('favorited');
            icon.classList.remove('fas');
            icon.classList.add('far');
            icon.classList.remove('text-danger');
            showNotification('Removed from favorites', 'info');
        }
        
        // Save to localStorage
        const opportunityId = this.getAttribute('data-opportunity-id');
        if (opportunityId) {
            saveFavorite(opportunityId, !isFavorited);
        }
    });
});

function saveFavorite(id, isFavorite) {
    let favorites = JSON.parse(localStorage.getItem('favoriteOpportunities')) || [];
    
    if (isFavorite) {
        if (!favorites.includes(id)) {
            favorites.push(id);
        }
    } else {
        favorites = favorites.filter(fav => fav !== id);
    }
    
    localStorage.setItem('favoriteOpportunities', JSON.stringify(favorites));
}

// ============================================
// 7. Copy to Clipboard
// ============================================

document.querySelectorAll('.btn-copy, [data-copy-text]').forEach(element => {
    if (element.classList.contains('btn-copy')) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            const textToCopy = this.getAttribute('data-copy-text') || 
                             this.previousElementSibling?.value ||
                             this.previousElementSibling?.textContent;
            
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    showNotification('Copied to clipboard!', 'success');
                }).catch(() => {
                    showNotification('Failed to copy', 'danger');
                });
            }
        });
    }
});

// ============================================
// 8. Data Export
// ============================================

function exportTableToCSV(filename, tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        let csvRow = [];
        
        cols.forEach(col => {
            csvRow.push('"' + col.textContent.trim() + '"');
        });
        
        csv.push(csvRow.join(','));
    });
    
    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename + '.csv';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// ============================================
// 9. Modal Management
// ============================================

function openModal(modalId) {
    const modalElement = document.getElementById(modalId);
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

function closeModal(modalId) {
    const modalElement = document.getElementById(modalId);
    if (modalElement) {
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
    }
}

// ============================================
// 10. Smooth Scrolling
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#' && !href.includes('navbarNav')) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
});

// ============================================
// 11. Responsive Tables
// ============================================

function makeTableResponsive() {
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        if (!table.closest('.table-responsive')) {
            table.addEventListener('scroll', function() {
                if (this.scrollLeft > 0) {
                    table.classList.add('scrolling');
                } else {
                    table.classList.remove('scrolling');
                }
            });
        }
    });
}

makeTableResponsive();

// ============================================
// 12. Loading States
// ============================================

/*
function setLoadingState(element, isLoading = true) {
    if (!element) return;
    
    if (isLoading) {
        element.disabled = true;
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    } else {
        element.disabled = false;
        element.innerHTML = element.getAttribute('data-original-text') || 'Submit';
    }
}

// temporarily disable automatic loading indicators because they were causing
// the button to remain stuck in "Loading..." during form submission in some
// browsers/contexts. we can re-enable once the issue is resolved.
document.querySelectorAll('button[type="submit"]').forEach(btn => {
    btn.setAttribute('data-original-text', btn.innerHTML);
    btn.addEventListener('click', function() {
        if (this.closest('form').checkValidity()) {
            // setLoadingState(this, true);
        }
    });
});
*/

// simplified loading state: do nothing
function setLoadingState(element, isLoading = true) {
    // no-op to prevent spinner lockup
}

// keep the reset on page load just in case
window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button[type="submit"]').forEach(btn => setLoadingState(btn, false));
});

// ============================================
// 13. Dark Mode Toggle (Optional)
// ============================================

function setupDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (!darkModeToggle) return;
    
    // Check for saved preference
    const prefersDark = localStorage.getItem('darkMode') === 'true';
    if (prefersDark) {
        document.body.classList.add('dark-mode');
    }
    
    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
    });
}

setupDarkMode();

// ============================================
// 14. Confirmation Dialogs
// ============================================

function confirmAction(message = 'Are you sure?') {
    return new Promise((resolve) => {
        const modalHtml = `
            <div class="modal fade" id="confirmModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content border-0">
                        <div class="modal-header border-0">
                            <h5 class="modal-title fw-bold">Confirm Action</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                        </div>
                        <div class="modal-footer border-0">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-danger" id="confirmBtn">Confirm</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const modalWrapper = document.createElement('div');
        modalWrapper.innerHTML = modalHtml;
        document.body.appendChild(modalWrapper);
        
        const modalElement = document.getElementById('confirmModal');
        const modal = new bootstrap.Modal(modalElement);
        
        document.getElementById('confirmBtn').addEventListener('click', () => {
            modal.hide();
            resolve(true);
            setTimeout(() => modalWrapper.remove(), 300);
        });
        
        modalElement.addEventListener('hidden.bs.modal', () => {
            resolve(false);
            setTimeout(() => modalWrapper.remove(), 300);
        });
        
        modal.show();
    });
}

// ============================================
// 15. Utility Functions
// ============================================

// Format date
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Format time ago
function timeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    let interval = seconds / 31536000;
    
    if (interval > 1) {
        return Math.floor(interval) + ' years ago';
    }
    interval = seconds / 2592000;
    if (interval > 1) {
        return Math.floor(interval) + ' months ago';
    }
    interval = seconds / 86400;
    if (interval > 1) {
        return Math.floor(interval) + ' days ago';
    }
    interval = seconds / 3600;
    if (interval > 1) {
        return Math.floor(interval) + ' hours ago';
    }
    interval = seconds / 60;
    if (interval > 1) {
        return Math.floor(interval) + ' minutes ago';
    }
    return Math.floor(seconds) + ' seconds ago';
}

// Debounce function
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

// ============================================
// 16. Initialize on Page Load
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(popoverTriggerEl => {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add animation to cards on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-up');
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.card, .opportunity-card').forEach(card => {
        observer.observe(card);
    });
    
    console.log('SEU Volunteering Platform initialized successfully');
});

// ============================================
// 17. Export Module (for use in HTML)
// ============================================

window.SEUVolunteer = {
    showNotification,
    confirmAction,
    openModal,
    closeModal,
    filterOpportunities,
    exportTableToCSV,
    formatDate,
    timeAgo,
    saveFavorite
};

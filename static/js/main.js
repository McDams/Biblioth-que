// =================================
// Système de Gestion Bibliothèque
// JavaScript principal
// =================================

$(document).ready(function() {
    // Animation d'entrée pour les cartes
    $('.card').addClass('fade-in');
    
    // Confirmation des suppressions
    $('.btn-danger[data-action="delete"]').on('click', function(e) {
        if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
            e.preventDefault();
        }
    });
    
    // Auto-hide des messages après 5 secondes
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Recherche en temps réel
    let searchTimeout;
    $('#search-input').on('input', function() {
        clearTimeout(searchTimeout);
        const query = $(this).val();
        
        if (query.length >= 3) {
            searchTimeout = setTimeout(function() {
                performSearch(query);
            }, 500);
        }
    });
    
    // Initialisation des tooltips Bootstrap
    $('[data-toggle="tooltip"]').tooltip();
    
    // Initialisation des popovers Bootstrap
    $('[data-toggle="popover"]').popover();
    
    // Validation des formulaires
    $('form').on('submit', function() {
        $(this).find('button[type="submit"]').addClass('loading').prop('disabled', true);
    });
    
    // Prévisualisation des images
    $('.file-input').on('change', function() {
        previewImage(this);
    });
    
    // Gestion des onglets avec localStorage
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });
    
    const activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        $('a[href="' + activeTab + '"]').tab('show');
    }
    
    // Compteur de caractères pour les textarea
    $('textarea[maxlength]').each(function() {
        const maxLength = $(this).attr('maxlength');
        const textareaId = $(this).attr('id');
        
        $(this).after('<small class="form-text text-muted"><span id="' + textareaId + '-count">0</span>/' + maxLength + ' caractères</small>');
        
        $(this).on('input', function() {
            const currentLength = $(this).val().length;
            $('#' + textareaId + '-count').text(currentLength);
            
            if (currentLength > maxLength * 0.9) {
                $('#' + textareaId + '-count').addClass('text-warning');
            } else {
                $('#' + textareaId + '-count').removeClass('text-warning');
            }
        });
    });
    
    // Filtres dynamiques
    $('.filter-checkbox').on('change', function() {
        applyFilters();
    });
    
    // Tri des tableaux
    $('.sortable th').on('click', function() {
        const column = $(this).data('sort');
        const direction = $(this).hasClass('sort-asc') ? 'desc' : 'asc';
        
        $('.sortable th').removeClass('sort-asc sort-desc');
        $(this).addClass('sort-' + direction);
        
        sortTable(column, direction);
    });
    
    // Sélection multiple dans les tableaux
    $('#select-all').on('change', function() {
        $('.row-checkbox').prop('checked', $(this).prop('checked'));
        updateBulkActions();
    });
    
    $('.row-checkbox').on('change', function() {
        updateBulkActions();
    });
    
    // Actions groupées
    $('#bulk-action-btn').on('click', function() {
        const action = $('#bulk-action-select').val();
        const selectedIds = $('.row-checkbox:checked').map(function() {
            return $(this).val();
        }).get();
        
        if (selectedIds.length === 0) {
            alert('Veuillez sélectionner au moins un élément.');
            return;
        }
        
        if (confirm('Êtes-vous sûr de vouloir effectuer cette action sur ' + selectedIds.length + ' élément(s) ?')) {
            performBulkAction(action, selectedIds);
        }
    });
});

// Fonctions utilitaires

function performSearch(query) {
    // Implémentation de la recherche AJAX
    $.ajax({
        url: '/search/',
        method: 'GET',
        data: { q: query },
        success: function(response) {
            $('#search-results').html(response);
        },
        error: function() {
            console.error('Erreur lors de la recherche');
        }
    });
}

function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const previewId = $(input).data('preview');
            $('#' + previewId).attr('src', e.target.result).show();
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

function applyFilters() {
    const filters = {};
    
    $('.filter-checkbox:checked').each(function() {
        const filterName = $(this).data('filter');
        const filterValue = $(this).val();
        
        if (!filters[filterName]) {
            filters[filterName] = [];
        }
        filters[filterName].push(filterValue);
    });
    
    // Appliquer les filtres via AJAX ou redirection
    const queryString = $.param(filters);
    window.location.href = window.location.pathname + '?' + queryString;
}

function sortTable(column, direction) {
    const queryParams = new URLSearchParams(window.location.search);
    queryParams.set('sort', column);
    queryParams.set('direction', direction);
    
    window.location.href = window.location.pathname + '?' + queryParams.toString();
}

function updateBulkActions() {
    const selectedCount = $('.row-checkbox:checked').length;
    const totalCount = $('.row-checkbox').length;
    
    $('#bulk-action-btn').prop('disabled', selectedCount === 0);
    $('#selected-count').text(selectedCount);
    
    $('#select-all').prop('indeterminate', selectedCount > 0 && selectedCount < totalCount);
    $('#select-all').prop('checked', selectedCount === totalCount);
}

function performBulkAction(action, ids) {
    // Implémentation des actions groupées
    $.ajax({
        url: '/bulk-action/',
        method: 'POST',
        data: {
            action: action,
            ids: ids,
            csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            if (response.success) {
                location.reload();
            } else {
                alert('Erreur: ' + response.message);
            }
        },
        error: function() {
            alert('Erreur lors de l\'exécution de l\'action.');
        }
    });
}

// Gestion des notifications
function showNotification(message, type = 'info') {
    const alertClass = 'alert-' + type;
    const notification = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="close" data-dismiss="alert">
                <span>&times;</span>
            </button>
        </div>
    `;
    
    $('#notifications').prepend(notification);
    
    // Auto-hide après 5 secondes
    setTimeout(function() {
        $('.alert').first().fadeOut('slow');
    }, 5000);
}

// Validation côté client
function validateForm(formId) {
    let isValid = true;
    
    $('#' + formId + ' [required]').each(function() {
        if (!$(this).val().trim()) {
            $(this).addClass('is-invalid');
            isValid = false;
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    // Validation des emails
    $('#' + formId + ' input[type="email"]').each(function() {
        const email = $(this).val();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (email && !emailRegex.test(email)) {
            $(this).addClass('is-invalid');
            isValid = false;
        }
    });
    
    return isValid;
}

// Gestion du panier de livres (pour les emprunts multiples)
let bookCart = JSON.parse(localStorage.getItem('bookCart') || '[]');

function addToCart(bookId, bookTitle) {
    if (!bookCart.find(book => book.id === bookId)) {
        bookCart.push({ id: bookId, title: bookTitle });
        localStorage.setItem('bookCart', JSON.stringify(bookCart));
        updateCartDisplay();
        showNotification('Livre ajouté au panier', 'success');
    } else {
        showNotification('Ce livre est déjà dans le panier', 'warning');
    }
}

function removeFromCart(bookId) {
    bookCart = bookCart.filter(book => book.id !== bookId);
    localStorage.setItem('bookCart', JSON.stringify(bookCart));
    updateCartDisplay();
    showNotification('Livre retiré du panier', 'info');
}

function clearCart() {
    bookCart = [];
    localStorage.removeItem('bookCart');
    updateCartDisplay();
    showNotification('Panier vidé', 'info');
}

function updateCartDisplay() {
    const cartCount = bookCart.length;
    $('#cart-count').text(cartCount);
    
    if (cartCount > 0) {
        $('#cart-badge').show();
    } else {
        $('#cart-badge').hide();
    }
    
    // Mettre à jour l'affichage du panier si on est sur la page du panier
    if ($('#cart-items').length) {
        displayCartItems();
    }
}

function displayCartItems() {
    const cartContainer = $('#cart-items');
    cartContainer.empty();
    
    if (bookCart.length === 0) {
        cartContainer.html('<p class="text-muted">Votre panier est vide.</p>');
        return;
    }
    
    bookCart.forEach(book => {
        const item = `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span>${book.title}</span>
                <button class="btn btn-sm btn-outline-danger" onclick="removeFromCart(${book.id})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        cartContainer.append(item);
    });
}

// Initialisation du panier au chargement de la page
$(document).ready(function() {
    updateCartDisplay();
});

// Gestion des favoris
function toggleFavorite(bookId) {
    $.ajax({
        url: `/books/${bookId}/toggle-favorite/`,
        method: 'POST',
        data: {
            csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            if (response.is_favorite) {
                $(`#favorite-btn-${bookId}`).removeClass('btn-outline-danger').addClass('btn-danger');
                $(`#favorite-icon-${bookId}`).removeClass('far').addClass('fas');
                showNotification('Livre ajouté aux favoris', 'success');
            } else {
                $(`#favorite-btn-${bookId}`).removeClass('btn-danger').addClass('btn-outline-danger');
                $(`#favorite-icon-${bookId}`).removeClass('fas').addClass('far');
                showNotification('Livre retiré des favoris', 'info');
            }
        },
        error: function() {
            showNotification('Erreur lors de la mise à jour des favoris', 'danger');
        }
    });
}

// Statistiques en temps réel
function updateDashboardStats() {
    $.ajax({
        url: '/dashboard/stats/',
        method: 'GET',
        success: function(response) {
            Object.keys(response).forEach(key => {
                $(`#stat-${key}`).text(response[key]);
            });
        },
        error: function() {
            console.error('Erreur lors de la mise à jour des statistiques');
        }
    });
}

// Mise à jour automatique des statistiques toutes les 30 secondes
if (window.location.pathname.includes('/dashboard/')) {
    setInterval(updateDashboardStats, 30000);
}

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Loan, LoanHistory, Reservation


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Administration des emprunts"""
    list_display = ['get_book_title', 'get_borrower_name', 'loan_date', 'due_date', 
                   'returned_date', 'get_status_display', 'is_overdue']
    list_filter = ['status', 'loan_date', 'due_date', 'returned_date']
    search_fields = ['book__title', 'borrower__username', 'borrower__first_name', 'borrower__last_name']
    ordering = ['-loan_date']
    readonly_fields = ['loan_date', 'created_by']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('book', 'borrower', 'loan_date')
        }),
        ('Dates', {
            'fields': ('due_date', 'returned_date')
        }),
        ('Statut et notes', {
            'fields': ('status', 'notes', 'librarian_notes')
        }),
        ('Métadonnées', {
            'fields': ('created_by',),
            'classes': ['collapse']
        })
    )
    
    def get_book_title(self, obj):
        """Titre du livre avec lien"""
        url = reverse('admin:books_book_change', args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.title)
    get_book_title.short_description = 'Livre'
    
    def get_borrower_name(self, obj):
        """Nom de l'emprunteur avec lien"""
        url = reverse('admin:accounts_customuser_change', args=[obj.borrower.id])
        return format_html('<a href="{}">{}</a>', url, obj.borrower.get_full_name())
    get_borrower_name.short_description = 'Emprunteur'
    
    def get_status_display(self, obj):
        """Affichage coloré du statut"""
        colors = {
            'active': 'green',
            'returned': 'blue',
            'overdue': 'red',
            'lost': 'orange'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    get_status_display.short_description = 'Statut'
    
    def is_overdue(self, obj):
        """Indicateur de retard"""
        if obj.is_overdue():
            return format_html('<span style="color: red;">⚠️ Oui</span>')
        return format_html('<span style="color: green;">✓ Non</span>')
    is_overdue.short_description = 'En retard'
    is_overdue.boolean = False
    
    def save_model(self, request, obj, form, change):
        """Enregistrer l'utilisateur qui crée l'emprunt"""
        if not change:  # Nouvel emprunt
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(LoanHistory)
class LoanHistoryAdmin(admin.ModelAdmin):
    """Administration de l'historique des emprunts"""
    list_display = ['loan', 'action', 'performed_by', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['loan__book__title', 'loan__borrower__username', 'performed_by__username']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    
    def has_add_permission(self, request):
        """Interdire l'ajout manuel d'historique"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Interdire la modification de l'historique"""
        return False


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Administration des réservations"""
    list_display = ['get_book_title', 'get_user_name', 'reserved_date', 'expiry_date', 
                   'get_status_display', 'notified']
    list_filter = ['status', 'reserved_date', 'expiry_date', 'notified']
    search_fields = ['book__title', 'user__username', 'user__first_name', 'user__last_name']
    ordering = ['-reserved_date']
    readonly_fields = ['reserved_date']
    
    def get_book_title(self, obj):
        """Titre du livre avec lien"""
        url = reverse('admin:books_book_change', args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.title)
    get_book_title.short_description = 'Livre'
    
    def get_user_name(self, obj):
        """Nom de l'utilisateur avec lien"""
        url = reverse('admin:accounts_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name())
    get_user_name.short_description = 'Utilisateur'
    
    def get_status_display(self, obj):
        """Affichage coloré du statut"""
        colors = {
            'pending': 'orange',
            'available': 'green',
            'fulfilled': 'blue',
            'cancelled': 'red',
            'expired': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    get_status_display.short_description = 'Statut'

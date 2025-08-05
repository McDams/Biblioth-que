from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Book, Author, Publisher, Category, BookReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administration des catégories"""
    list_display = ['name', 'book_count', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def book_count(self, obj):
        """Nombre de livres dans la catégorie"""
        count = obj.book_set.count()
        if count > 0:
            url = reverse('admin:books_book_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} livre{}</a>', url, count, 's' if count > 1 else '')
        return '0'
    book_count.short_description = 'Nombre de livres'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Administration des auteurs"""
    list_display = ['get_full_name', 'nationality', 'birth_date', 'book_count']
    list_filter = ['nationality', 'birth_date']
    search_fields = ['first_name', 'last_name', 'nationality']
    ordering = ['last_name', 'first_name']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Nom complet'
    
    def book_count(self, obj):
        """Nombre de livres de l'auteur"""
        count = obj.book_set.count()
        if count > 0:
            url = reverse('admin:books_book_changelist') + f'?authors__id__exact={obj.id}'
            return format_html('<a href="{}">{} livre{}</a>', url, count, 's' if count > 1 else '')
        return '0'
    book_count.short_description = 'Nombre de livres'


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Administration des éditeurs"""
    list_display = ['name', 'book_count', 'website']
    search_fields = ['name', 'address']
    ordering = ['name']
    
    def book_count(self, obj):
        """Nombre de livres de l'éditeur"""
        count = obj.book_set.count()
        if count > 0:
            url = reverse('admin:books_book_changelist') + f'?publisher__id__exact={obj.id}'
            return format_html('<a href="{}">{} livre{}</a>', url, count, 's' if count > 1 else '')
        return '0'
    book_count.short_description = 'Nombre de livres'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Administration des livres"""
    list_display = ['title', 'get_authors_display', 'category', 'publisher', 'publication_date', 
                   'available_copies', 'total_copies', 'is_active', 'created_at']
    list_filter = ['category', 'publisher', 'language', 'is_active', 'publication_date', 'created_at']
    search_fields = ['title', 'isbn', 'authors__first_name', 'authors__last_name', 'keywords']
    ordering = ['-created_at']
    filter_horizontal = ['authors']
    readonly_fields = ['created_at', 'updated_at', 'added_by']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'subtitle', 'isbn', 'authors', 'publisher', 'category')
        }),
        ('Détails de publication', {
            'fields': ('publication_date', 'pages', 'language', 'cover_image')
        }),
        ('Description', {
            'fields': ('summary', 'keywords')
        }),
        ('Gestion des stocks', {
            'fields': ('total_copies', 'available_copies')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'added_by'),
            'classes': ['collapse']
        })
    )
    
    def save_model(self, request, obj, form, change):
        """Enregistrer l'utilisateur qui ajoute le livre"""
        if not change:  # Nouveau livre
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_authors_display(self, obj):
        """Affichage des auteurs"""
        return obj.get_authors_display()
    get_authors_display.short_description = 'Auteurs'


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    """Administration des avis sur les livres"""
    list_display = ['book', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'reviewer__username', 'comment']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def get_readonly_fields(self, request, obj=None):
        """Champs en lecture seule"""
        if obj:  # Édition
            return self.readonly_fields + ['book', 'reviewer']
        return self.readonly_fields

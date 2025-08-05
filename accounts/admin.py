from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Administration personnalisée pour les utilisateurs"""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active_member', 'registration_date', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'is_active_member', 'registration_date']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['-registration_date']
    
    # Ajout des champs personnalisés au formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('phone', 'address', 'birth_date', 'profile_picture', 'is_active_member')
        }),
    )
    
    # Ajout des champs lors de la création
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('email', 'first_name', 'last_name', 'phone', 'address', 'birth_date')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Champs en lecture seule selon le contexte"""
        if obj:  # Édition d'un utilisateur existant
            return ['registration_date']
        return []

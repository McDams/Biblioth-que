from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Modèle utilisateur personnalisé avec des champs supplémentaires"""
    
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        verbose_name="Téléphone"
    )
    address = models.TextField(
        blank=True, 
        verbose_name="Adresse"
    )
    birth_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Date de naissance"
    )
    registration_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Date d'inscription"
    )
    is_active_member = models.BooleanField(
        default=True, 
        verbose_name="Membre actif"
    )
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        blank=True, 
        null=True,
        verbose_name="Photo de profil"
    )
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username
    
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def can_borrow_books(self):
        """Vérifie si l'utilisateur peut emprunter des livres"""
        return self.is_active and self.is_active_member

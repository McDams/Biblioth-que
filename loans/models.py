from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from books.models import Book

User = get_user_model()


class Loan(models.Model):
    """Modèle pour les emprunts de livres"""
    
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('returned', 'Retourné'),
        ('overdue', 'En retard'),
        ('lost', 'Perdu'),
    ]
    
    # Relations
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Livre")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Emprunteur")
    
    # Dates
    loan_date = models.DateTimeField(default=timezone.now, verbose_name="Date d'emprunt")
    due_date = models.DateField(verbose_name="Date de retour prévue")
    returned_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de retour effective")
    
    # Statut
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name="Statut"
    )
    
    # Notes
    notes = models.TextField(blank=True, verbose_name="Notes")
    librarian_notes = models.TextField(blank=True, verbose_name="Notes du bibliothécaire")
    
    # Métadonnées
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_loans',
        verbose_name="Créé par"
    )
    
    class Meta:
        verbose_name = "Emprunt"
        verbose_name_plural = "Emprunts"
        ordering = ['-loan_date']
        indexes = [
            models.Index(fields=['borrower', 'status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.book.title} - {self.borrower.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Définir la date de retour prévue (par défaut 14 jours)
        if not self.due_date:
            self.due_date = (self.loan_date + timedelta(days=14)).date()
        
        # Mettre à jour le statut automatiquement
        if not self.returned_date and self.due_date < timezone.now().date():
            self.status = 'overdue'
        elif self.returned_date:
            self.status = 'returned'
        
        super().save(*args, **kwargs)
    
    def is_overdue(self):
        """Vérifie si l'emprunt est en retard"""
        if self.returned_date:
            return False
        return self.due_date < timezone.now().date()
    
    def days_overdue(self):
        """Retourne le nombre de jours de retard"""
        if not self.is_overdue():
            return 0
        return (timezone.now().date() - self.due_date).days
    
    def days_until_due(self):
        """Retourne le nombre de jours avant échéance"""
        if self.returned_date:
            return None
        days = (self.due_date - timezone.now().date()).days
        return days if days >= 0 else 0
    
    def return_book(self, librarian=None, notes=""):
        """Retourne le livre"""
        if not self.returned_date:
            self.returned_date = timezone.now()
            self.status = 'returned'
            if notes:
                self.librarian_notes = notes
            self.book.return_book()  # Augmente le stock disponible
            self.save()
            return True
        return False


class LoanHistory(models.Model):
    """Historique des actions sur les emprunts"""
    
    ACTION_CHOICES = [
        ('created', 'Créé'),
        ('extended', 'Prolongé'),
        ('returned', 'Retourné'),
        ('marked_lost', 'Marqué comme perdu'),
        ('renewed', 'Renouvelé'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='history', verbose_name="Emprunt")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Action")
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Effectué par")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Horodatage")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Historique d'emprunt"
        verbose_name_plural = "Historiques d'emprunts"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.loan} - {self.get_action_display()}"


class Reservation(models.Model):
    """Modèle pour les réservations de livres"""
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('available', 'Disponible'),
        ('fulfilled', 'Satisfaite'),
        ('cancelled', 'Annulée'),
        ('expired', 'Expirée'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Livre")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    reserved_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de réservation")
    expiry_date = models.DateTimeField(verbose_name="Date d'expiration")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Statut"
    )
    notified = models.BooleanField(default=False, verbose_name="Notifié")
    
    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-reserved_date']
        unique_together = ['book', 'user', 'status']
    
    def __str__(self):
        return f"{self.book.title} - {self.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Définir la date d'expiration (7 jours par défaut)
        if not self.expiry_date:
            self.expiry_date = self.reserved_date + timedelta(days=7)
        super().save(*args, **kwargs)

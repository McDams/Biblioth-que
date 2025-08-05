from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    """Modèle pour les catégories de livres"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Author(models.Model):
    """Modèle pour les auteurs"""
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    death_date = models.DateField(null=True, blank=True, verbose_name="Date de décès")
    biography = models.TextField(blank=True, verbose_name="Biographie")
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Nationalité")
    
    class Meta:
        verbose_name = "Auteur"
        verbose_name_plural = "Auteurs"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    """Modèle pour les éditeurs"""
    name = models.CharField(max_length=200, unique=True, verbose_name="Nom")
    address = models.TextField(blank=True, verbose_name="Adresse")
    website = models.URLField(blank=True, verbose_name="Site web")
    
    class Meta:
        verbose_name = "Éditeur"
        verbose_name_plural = "Éditeurs"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Modèle principal pour les livres"""
    
    # Informations de base
    title = models.CharField(max_length=300, verbose_name="Titre")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    authors = models.ManyToManyField(Author, verbose_name="Auteurs")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name="Éditeur")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Catégorie")
    
    # Détails de publication
    publication_date = models.DateField(verbose_name="Date de publication")
    pages = models.PositiveIntegerField(verbose_name="Nombre de pages")
    language = models.CharField(max_length=50, default="Français", verbose_name="Langue")
    
    # Description et contenu
    summary = models.TextField(verbose_name="Résumé")
    keywords = models.CharField(max_length=500, blank=True, verbose_name="Mots-clés")
    
    # Informations physiques
    cover_image = models.ImageField(
        upload_to='book_covers/', 
        blank=True, 
        null=True,
        verbose_name="Image de couverture"
    )
    
    # Gestion des stocks
    total_copies = models.PositiveIntegerField(
        default=1, 
        validators=[MinValueValidator(1)],
        verbose_name="Exemplaires totaux"
    )
    available_copies = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name="Exemplaires disponibles"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ajouté le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    added_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Ajouté par"
    )
    
    # Statut
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['isbn']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'pk': self.pk})
    
    def is_available(self):
        """Vérifie si le livre est disponible pour emprunt"""
        return self.available_copies > 0 and self.is_active
    
    def get_authors_display(self):
        """Retourne la liste des auteurs sous forme de chaîne"""
        return ", ".join([author.get_full_name() for author in self.authors.all()])
    
    def borrow_book(self):
        """Emprunte un exemplaire du livre"""
        if self.available_copies > 0:
            self.available_copies -= 1
            self.save()
            return True
        return False
    
    def return_book(self):
        """Retourne un exemplaire du livre"""
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            self.save()
            return True
        return False


class BookReview(models.Model):
    """Modèle pour les avis sur les livres"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Livre")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note"
    )
    comment = models.TextField(blank=True, verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    
    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        unique_together = ['book', 'reviewer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.book.title} - {self.reviewer.username} ({self.rating}/5)"

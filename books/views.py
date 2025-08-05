from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Book, Category, Author, BookReview
from loans.models import Loan


class BookListView(ListView):
    """Vue liste des livres pour les utilisateurs"""
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Book.objects.filter(is_active=True).select_related('category', 'publisher')
        
        # Recherche
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(authors__first_name__icontains=query) |
                Q(authors__last_name__icontains=query) |
                Q(keywords__icontains=query)
            ).distinct()
        
        # Filtrage par catégorie
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Tri
        sort_by = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['current_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        return context


class BookDetailView(DetailView):
    """Vue détail d'un livre"""
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        
        # Avis sur le livre
        context['reviews'] = book.reviews.all()[:5]
        context['average_rating'] = book.reviews.aggregate(
            avg_rating=models.Avg('rating')
        )['avg_rating']
        
        # Vérifier si l'utilisateur peut emprunter
        if self.request.user.is_authenticated:
            context['can_borrow'] = book.is_available()
            context['user_has_active_loan'] = Loan.objects.filter(
                borrower=self.request.user,
                book=book,
                returned_date__isnull=True
            ).exists()
        
        # Livres similaires
        context['similar_books'] = Book.objects.filter(
            category=book.category,
            is_active=True
        ).exclude(id=book.id)[:4]
        
        return context


@login_required
def toggle_favorite(request, book_id):
    """Toggle favori pour un livre"""
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        # Implémentation des favoris (nécessite un modèle Favorite)
        return JsonResponse({'is_favorite': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def add_review(request, book_id):
    """Ajouter un avis sur un livre"""
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        review, created = BookReview.objects.get_or_create(
            book=book,
            reviewer=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if not created:
            review.rating = rating
            review.comment = comment
            review.save()
        
        messages.success(request, 'Votre avis a été ajouté avec succès!')
        return redirect('books:detail', pk=book_id)
    
    return redirect('books:list')


# Vues d'administration (à compléter)
class AdminBookListView(LoginRequiredMixin, ListView):
    """Vue d'administration pour la liste des livres"""
    model = Book
    template_name = 'books/admin_book_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Accès non autorisé.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

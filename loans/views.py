from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Loan, LoanHistory, Reservation
from books.models import Book


class MyLoansView(LoginRequiredMixin, ListView):
    """Vue des emprunts de l'utilisateur connecté"""
    model = Loan
    template_name = 'loans/my_loans.html'
    context_object_name = 'loans'
    
    def get_queryset(self):
        return Loan.objects.filter(
            borrower=self.request.user
        ).select_related('book').order_by('-loan_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_loans = self.get_queryset()
        
        context['active_loans'] = user_loans.filter(returned_date__isnull=True)
        context['overdue_loans'] = user_loans.filter(
            returned_date__isnull=True,
            due_date__lt=timezone.now().date()
        )
        context['loan_history'] = user_loans.filter(returned_date__isnull=False)[:10]
        
        return context


@login_required
def borrow_book(request, book_id):
    """Emprunter un livre"""
    book = get_object_or_404(Book, id=book_id)
    
    if not book.is_available():
        messages.error(request, "Ce livre n'est pas disponible pour l'emprunt.")
        return redirect('books:detail', pk=book_id)
    
    # Vérifier si l'utilisateur a déjà emprunté ce livre
    existing_loan = Loan.objects.filter(
        borrower=request.user,
        book=book,
        returned_date__isnull=True
    ).exists()
    
    if existing_loan:
        messages.warning(request, "Vous avez déjà emprunté ce livre.")
        return redirect('books:detail', pk=book_id)
    
    # Vérifier le nombre d'emprunts actifs
    active_loans_count = Loan.objects.filter(
        borrower=request.user,
        returned_date__isnull=True
    ).count()
    
    if active_loans_count >= 5:  # Limite de 5 emprunts simultanés
        messages.error(request, "Vous avez atteint la limite d'emprunts simultanés (5).")
        return redirect('books:detail', pk=book_id)
    
    # Créer l'emprunt
    loan = Loan.objects.create(
        book=book,
        borrower=request.user,
        due_date=timezone.now().date() + timedelta(days=14)
    )
    
    # Réduire le stock disponible
    book.borrow_book()
    
    # Créer l'historique
    LoanHistory.objects.create(
        loan=loan,
        action='created',
        performed_by=request.user
    )
    
    messages.success(request, f"Livre '{book.title}' emprunté avec succès! Date de retour: {loan.due_date}")
    return redirect('loans:my_loans')


@login_required
def return_book(request, pk):
    """Retourner un livre"""
    loan = get_object_or_404(Loan, pk=pk, borrower=request.user)
    
    if loan.returned_date:
        messages.warning(request, "Ce livre a déjà été retourné.")
        return redirect('loans:my_loans')
    
    # Retourner le livre
    loan.return_book(notes="Retour par l'utilisateur")
    
    # Créer l'historique
    LoanHistory.objects.create(
        loan=loan,
        action='returned',
        performed_by=request.user
    )
    
    messages.success(request, f"Livre '{loan.book.title}' retourné avec succès!")
    return redirect('loans:my_loans')


@login_required
def extend_loan(request, pk):
    """Prolonger un emprunt"""
    loan = get_object_or_404(Loan, pk=pk, borrower=request.user)
    
    if loan.returned_date:
        messages.warning(request, "Ce livre a déjà été retourné.")
        return redirect('loans:my_loans')
    
    # Vérifier si l'extension est possible (pas plus de 2 extensions)
    extensions_count = LoanHistory.objects.filter(
        loan=loan,
        action='extended'
    ).count()
    
    if extensions_count >= 2:
        messages.error(request, "Vous avez déjà prolongé cet emprunt 2 fois (limite atteinte).")
        return redirect('loans:my_loans')
    
    # Prolonger de 7 jours
    loan.due_date += timedelta(days=7)
    loan.save()
    
    # Créer l'historique
    LoanHistory.objects.create(
        loan=loan,
        action='extended',
        performed_by=request.user,
        notes=f"Prolongé jusqu'au {loan.due_date}"
    )
    
    messages.success(request, f"Emprunt prolongé jusqu'au {loan.due_date}")
    return redirect('loans:my_loans')


@login_required
def reserve_book(request, book_id):
    """Réserver un livre"""
    book = get_object_or_404(Book, id=book_id)
    
    if book.is_available():
        messages.info(request, "Ce livre est disponible, vous pouvez l'emprunter directement.")
        return redirect('books:detail', pk=book_id)
    
    # Vérifier si l'utilisateur a déjà une réservation
    existing_reservation = Reservation.objects.filter(
        user=request.user,
        book=book,
        status='pending'
    ).exists()
    
    if existing_reservation:
        messages.warning(request, "Vous avez déjà réservé ce livre.")
        return redirect('books:detail', pk=book_id)
    
    # Créer la réservation
    reservation = Reservation.objects.create(
        book=book,
        user=request.user,
        expiry_date=timezone.now() + timedelta(days=7)
    )
    
    messages.success(request, f"Livre '{book.title}' réservé avec succès! Vous serez notifié quand il sera disponible.")
    return redirect('books:detail', pk=book_id)


# Vues d'administration (à compléter)
class AdminLoanListView(LoginRequiredMixin, ListView):
    """Vue d'administration pour les emprunts"""
    model = Loan
    template_name = 'loans/admin_loan_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Accès non autorisé.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)


class AdminLoanDetailView(LoginRequiredMixin, DetailView):
    """Vue de détail d'un emprunt pour l'administration"""
    model = Loan
    template_name = 'loans/admin_loan_detail.html'
    context_object_name = 'loan'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Accès non autorisé.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

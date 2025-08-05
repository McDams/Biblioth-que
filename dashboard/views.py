from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta, datetime
from books.models import Book, Category
from loans.models import Loan
from accounts.models import CustomUser


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Vue principale du tableau de bord"""
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_staff:
            # Statistiques pour les administrateurs
            context.update(self.get_admin_stats())
        else:
            # Statistiques pour les utilisateurs
            context.update(self.get_user_stats(user))
        
        return context
    
    def get_user_stats(self, user):
        """Statistiques pour un utilisateur normal"""
        # Emprunts de l'utilisateur
        user_loans = Loan.objects.filter(borrower=user)
        active_loans = user_loans.filter(returned_date__isnull=True)
        overdue_loans = active_loans.filter(due_date__lt=timezone.now().date())
        
        # Livres récemment ajoutés
        recent_books = Book.objects.filter(is_active=True).order_by('-created_at')[:6]
        
        # Livres populaires
        popular_books = Book.objects.filter(is_active=True).annotate(
            loan_count=Count('loan')
        ).order_by('-loan_count')[:6]
        
        return {
            'total_loans': user_loans.count(),
            'active_loans': active_loans,
            'overdue_loans': overdue_loans,
            'recent_books': recent_books,
            'popular_books': popular_books,
            'is_user_dashboard': True,
        }
    
    def get_admin_stats(self):
        """Statistiques pour les administrateurs"""
        today = timezone.now().date()
        this_month = today.replace(day=1)
        
        # Statistiques générales
        total_books = Book.objects.filter(is_active=True).count()
        total_users = CustomUser.objects.filter(is_active=True).count()
        total_loans = Loan.objects.count()
        active_loans = Loan.objects.filter(returned_date__isnull=True).count()
        overdue_loans = Loan.objects.filter(
            returned_date__isnull=True,
            due_date__lt=today
        ).count()
        
        # Statistiques du mois
        monthly_loans = Loan.objects.filter(
            loan_date__gte=this_month
        ).count()
        
        # Livres les plus empruntés
        popular_books = Book.objects.annotate(
            loan_count=Count('loan')
        ).order_by('-loan_count')[:5]
        
        # Catégories les plus populaires
        popular_categories = Category.objects.annotate(
            book_count=Count('book')
        ).order_by('-book_count')[:5]
        
        # Emprunts récents
        recent_loans = Loan.objects.select_related(
            'book', 'borrower'
        ).order_by('-loan_date')[:10]
        
        return {
            'total_books': total_books,
            'total_users': total_users,
            'total_loans': total_loans,
            'active_loans': active_loans,
            'overdue_loans': overdue_loans,
            'monthly_loans': monthly_loans,
            'popular_books': popular_books,
            'popular_categories': popular_categories,
            'recent_loans': recent_loans,
            'is_admin_dashboard': True,
        }


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """Tableau de bord administrateur avancé"""
    template_name = 'dashboard/admin.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Accès non autorisé.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques détaillées
        context.update(self.get_detailed_stats())
        
        return context
    
    def get_detailed_stats(self):
        """Statistiques détaillées pour l'administration"""
        today = timezone.now().date()
        
        # Graphiques et données pour les derniers 12 mois
        monthly_data = []
        for i in range(12):
            month_start = (today.replace(day=1) - timedelta(days=i*30)).replace(day=1)
            month_end = (month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            
            loans_count = Loan.objects.filter(
                loan_date__gte=month_start,
                loan_date__lte=month_end
            ).count()
            
            monthly_data.append({
                'month': month_start.strftime('%Y-%m'),
                'loans': loans_count
            })
        
        return {
            'monthly_data': list(reversed(monthly_data)),
        }


@login_required
def dashboard_stats(request):
    """API endpoint pour les statistiques en temps réel"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    today = timezone.now().date()
    
    stats = {
        'total_books': Book.objects.filter(is_active=True).count(),
        'total_users': CustomUser.objects.filter(is_active=True).count(),
        'active_loans': Loan.objects.filter(returned_date__isnull=True).count(),
        'overdue_loans': Loan.objects.filter(
            returned_date__isnull=True,
            due_date__lt=today
        ).count(),
    }
    
    return JsonResponse(stats)


@login_required
def user_profile(request):
    """Profil utilisateur avec statistiques"""
    user = request.user
    
    # Statistiques de l'utilisateur
    user_loans = Loan.objects.filter(borrower=user)
    total_loans = user_loans.count()
    active_loans = user_loans.filter(returned_date__isnull=True)
    
    # Catégories préférées
    favorite_categories = Category.objects.filter(
        book__loan__borrower=user
    ).annotate(
        loan_count=Count('book__loan')
    ).order_by('-loan_count')[:5]
    
    context = {
        'user': user,
        'total_loans': total_loans,
        'active_loans': active_loans,
        'favorite_categories': favorite_categories,
    }
    
    return render(request, 'dashboard/user_profile.html', context)


# Vues pour les rapports (à implémenter selon les besoins)
@login_required
def books_report(request):
    """Rapport sur les livres"""
    if not request.user.is_staff:
        return redirect('dashboard:home')
    return render(request, 'dashboard/reports/books.html')


@login_required
def loans_report(request):
    """Rapport sur les emprunts"""
    if not request.user.is_staff:
        return redirect('dashboard:home')
    return render(request, 'dashboard/reports/loans.html')


@login_required
def users_report(request):
    """Rapport sur les utilisateurs"""
    if not request.user.is_staff:
        return redirect('dashboard:home')
    return render(request, 'dashboard/reports/users.html')

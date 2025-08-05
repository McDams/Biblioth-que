from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import CustomUser


class CustomLoginView(LoginView):
    """Vue de connexion personnalisée"""
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard:home')


class CustomLogoutView(LogoutView):
    """Vue de déconnexion personnalisée"""
    next_page = reverse_lazy('accounts:login')


class RegisterView(CreateView):
    """Vue d'inscription"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Votre compte a été créé avec succès! Vous pouvez maintenant vous connecter.')
        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    """Vue du profil utilisateur"""
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Votre profil a été mis à jour avec succès!')
        return response


@login_required
def profile_detail(request):
    """Vue détaillée du profil utilisateur"""
    user = request.user
    
    # Statistiques de l'utilisateur
    from loans.models import Loan
    total_loans = Loan.objects.filter(borrower=user).count()
    active_loans = Loan.objects.filter(borrower=user, returned_date__isnull=True).count()
    overdue_loans = Loan.objects.filter(
        borrower=user, 
        returned_date__isnull=True,
        due_date__lt=timezone.now().date()
    ).count()
    
    context = {
        'user': user,
        'total_loans': total_loans,
        'active_loans': active_loans,
        'overdue_loans': overdue_loans,
    }
    
    return render(request, 'accounts/profile_detail.html', context)

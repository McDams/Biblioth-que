from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('admin/', views.AdminDashboardView.as_view(), name='admin'),
    path('stats/', views.dashboard_stats, name='stats'),
    path('profile/', views.user_profile, name='profile'),
    
    # Statistiques et rapports
    path('reports/books/', views.books_report, name='books_report'),
    path('reports/loans/', views.loans_report, name='loans_report'),
    path('reports/users/', views.users_report, name='users_report'),
    
    # API endpoints pour les graphiques
    path('api/stats/monthly/', views.monthly_stats, name='monthly_stats'),
    path('api/stats/categories/', views.category_stats, name='category_stats'),
    path('api/stats/popular-books/', views.popular_books_stats, name='popular_books'),
]

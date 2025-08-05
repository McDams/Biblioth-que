from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    # Liste des emprunts (admin)
    path('', views.AdminLoanListView.as_view(), name='list'),
    
    # Emprunts de l'utilisateur
    path('my-loans/', views.MyLoansView.as_view(), name='my_loans'),
    
    # Actions sur les emprunts
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow'),
    path('return/<int:pk>/', views.return_book, name='return'),
    path('extend/<int:pk>/', views.extend_loan, name='renew'),
    path('reserve/<int:book_id>/', views.reserve_book, name='reserve'),
    
    # Admin
    path('admin/detail/<int:pk>/', views.AdminLoanDetailView.as_view(), name='admin_detail'),
]

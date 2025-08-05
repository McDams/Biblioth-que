from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('', views.LoanListView.as_view(), name='list'),
    path('my-loans/', views.MyLoansView.as_view(), name='my_loans'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow'),
    path('<int:pk>/return/', views.return_book, name='return'),
    path('<int:pk>/extend/', views.extend_loan, name='extend'),
    path('history/', views.LoanHistoryView.as_view(), name='history'),
    
    # Réservations
    path('reservations/', views.ReservationListView.as_view(), name='reservations'),
    path('reserve/<int:book_id>/', views.reserve_book, name='reserve'),
    path('reservation/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    
    # Administration
    path('admin/', views.AdminLoanListView.as_view(), name='admin_list'),
    path('admin/<int:pk>/', views.AdminLoanDetailView.as_view(), name='admin_detail'),
    path('admin/<int:pk>/return/', views.admin_return_book, name='admin_return'),
    path('admin/overdue/', views.OverdueLoansView.as_view(), name='overdue'),
    
    # Rapports
    path('reports/', views.loan_reports, name='reports'),
    path('reports/export/', views.export_loans, name='export'),
]

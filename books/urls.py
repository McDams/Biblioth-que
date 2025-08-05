from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('search/', views.BookSearchView.as_view(), name='search'),
    path('category/<int:category_id>/', views.BooksByCategoryView.as_view(), name='by_category'),
    path('author/<int:author_id>/', views.BooksByAuthorView.as_view(), name='by_author'),
    
    # Administration
    path('admin/', views.AdminBookListView.as_view(), name='admin_list'),
    path('admin/add/', views.AdminBookCreateView.as_view(), name='admin_add'),
    path('admin/<int:pk>/edit/', views.AdminBookUpdateView.as_view(), name='admin_edit'),
    path('admin/<int:pk>/delete/', views.AdminBookDeleteView.as_view(), name='admin_delete'),
    
    # API endpoints
    path('<int:book_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:book_id>/review/', views.add_review, name='add_review'),
]

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Loan, Reservation
from books.models import Book, Author, Publisher, Category

User = get_user_model()


class LoanModelTest(TestCase):
    """Tests pour le modèle Loan"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(name='Test Category')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.author = Author.objects.create(first_name='Test', last_name='Author')
        
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            publisher=self.publisher,
            category=self.category,
            publication_date='2023-01-01',
            pages=100,
            summary='Test summary',
            total_copies=3,
            available_copies=3
        )
        self.book.authors.add(self.author)
        
        self.loan = Loan.objects.create(
            book=self.book,
            borrower=self.user,
            due_date=timezone.now().date() + timedelta(days=14)
        )
    
    def test_loan_creation(self):
        """Test de création d'emprunt"""
        self.assertEqual(self.loan.book, self.book)
        self.assertEqual(self.loan.borrower, self.user)
        self.assertEqual(self.loan.status, 'active')
    
    def test_is_overdue(self):
        """Test de détection de retard"""
        # Emprunt pas en retard
        self.assertFalse(self.loan.is_overdue())
        
        # Mettre l'emprunt en retard
        self.loan.due_date = timezone.now().date() - timedelta(days=1)
        self.loan.save()
        self.assertTrue(self.loan.is_overdue())
    
    def test_return_book(self):
        """Test de retour de livre"""
        initial_available = self.book.available_copies
        
        result = self.loan.return_book()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.loan.returned_date)
        self.assertEqual(self.loan.status, 'returned')
        
        # Vérifier que le stock a été mis à jour
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, initial_available + 1)

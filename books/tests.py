from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Book, Author, Publisher, Category

User = get_user_model()


class BookModelTest(TestCase):
    """Tests pour le modèle Book"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            name='Test Category',
            description='Test description'
        )
        
        self.publisher = Publisher.objects.create(
            name='Test Publisher'
        )
        
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author'
        )
        
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            publisher=self.publisher,
            category=self.category,
            publication_date='2023-01-01',
            pages=100,
            summary='Test summary',
            total_copies=3,
            available_copies=3,
            added_by=self.user
        )
        self.book.authors.add(self.author)
    
    def test_book_creation(self):
        """Test de création de livre"""
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.isbn, '1234567890123')
        self.assertTrue(self.book.is_available())
    
    def test_borrow_book(self):
        """Test d'emprunt de livre"""
        initial_copies = self.book.available_copies
        result = self.book.borrow_book()
        
        self.assertTrue(result)
        self.assertEqual(self.book.available_copies, initial_copies - 1)
    
    def test_return_book(self):
        """Test de retour de livre"""
        # Emprunter d'abord
        self.book.borrow_book()
        initial_copies = self.book.available_copies
        
        result = self.book.return_book()
        
        self.assertTrue(result)
        self.assertEqual(self.book.available_copies, initial_copies + 1)
    
    def test_get_authors_display(self):
        """Test d'affichage des auteurs"""
        self.assertEqual(self.book.get_authors_display(), 'Test Author')

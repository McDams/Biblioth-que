from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Tests pour le modèle CustomUser"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_creation(self):
        """Test de création d'utilisateur"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_get_full_name(self):
        """Test de la méthode get_full_name"""
        self.assertEqual(self.user.get_full_name(), 'Test User')
    
    def test_can_borrow_books(self):
        """Test de la méthode can_borrow_books"""
        self.assertTrue(self.user.can_borrow_books())
        
        # Désactiver l'utilisateur
        self.user.is_active = False
        self.user.save()
        self.assertFalse(self.user.can_borrow_books())
        
        # Réactiver mais désactiver l'adhésion
        self.user.is_active = True
        self.user.is_active_member = False
        self.user.save()
        self.assertFalse(self.user.can_borrow_books())

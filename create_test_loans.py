#!/usr/bin/env python
"""Script pour créer des données de test pour les emprunts"""

import os
import sys
import django
from datetime import date, timedelta
from django.utils import timezone

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from books.models import Book
from loans.models import Loan

User = get_user_model()

def create_test_loans():
    """Créer des emprunts de test"""
    
    # Récupérer l'utilisateur admin
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("Utilisateur 'admin' non trouvé. Créez d'abord un superuser avec 'python manage.py createsuperuser'")
        return
    
    # Récupérer quelques livres
    books = Book.objects.filter(is_active=True)[:5]
    
    if not books:
        print("Aucun livre trouvé. Importez d'abord des livres.")
        return
    
    print("Création d'emprunts de test...")
    
    # Créer des emprunts de test avec des dates correctes
    loans_created = 0
    
    for i, book in enumerate(books):
        # Emprunt en cours
        if i == 0:
            loan_date = timezone.now() - timedelta(days=5)
            due_date = (loan_date + timedelta(days=14)).date()
            
            loan = Loan.objects.create(
                book=book,
                borrower=user,
                loan_date=loan_date,
                due_date=due_date,
                status='active',
                created_by=user
            )
            loans_created += 1
            print(f"✓ Emprunt créé: {book.title} (en cours)")
        
        # Emprunt en retard
        elif i == 1:
            loan_date = timezone.now() - timedelta(days=20)
            due_date = (loan_date + timedelta(days=14)).date()
            
            loan = Loan.objects.create(
                book=book,
                borrower=user,
                loan_date=loan_date,
                due_date=due_date,
                status='overdue',
                created_by=user
            )
            loans_created += 1
            print(f"✓ Emprunt créé: {book.title} (en retard)")
        
        # Emprunt retourné
        elif i == 2:
            loan_date = timezone.now() - timedelta(days=30)
            due_date = (loan_date + timedelta(days=14)).date()
            returned_date = loan_date + timedelta(days=10)
            
            loan = Loan.objects.create(
                book=book,
                borrower=user,
                loan_date=loan_date,
                due_date=due_date,
                returned_date=returned_date,
                status='returned',
                created_by=user
            )
            loans_created += 1
            print(f"✓ Emprunt créé: {book.title} (retourné)")
    
    print(f"\n{loans_created} emprunts de test créés avec succès!")
    print("Vous pouvez maintenant tester le dashboard.")

if __name__ == '__main__':
    create_test_loans()

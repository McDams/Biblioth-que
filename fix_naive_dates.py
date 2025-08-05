#!/usr/bin/env python
"""Script pour corriger les dates naives dans les emprunts"""

import os
import sys
import django
from django.utils import timezone

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from loans.models import Loan

def fix_naive_dates():
    """Corriger les dates naives dans les emprunts"""
    
    loans_with_naive_dates = Loan.objects.filter(loan_date__isnull=False)
    
    print("Correction des dates naives...")
    
    for loan in loans_with_naive_dates:
        # Si la date est naive, la convertir en timezone-aware
        if loan.loan_date and timezone.is_naive(loan.loan_date):
            # Convertir en timezone-aware en gardant la même date/heure
            loan.loan_date = timezone.make_aware(loan.loan_date)
            loan.save()
            print(f"✓ Date corrigée pour l'emprunt {loan.id}")
        
        # Même chose pour returned_date si elle existe
        if loan.returned_date and timezone.is_naive(loan.returned_date):
            loan.returned_date = timezone.make_aware(loan.returned_date)
            loan.save()
            print(f"✓ Date de retour corrigée pour l'emprunt {loan.id}")
    
    print("Correction terminée!")

if __name__ == '__main__':
    fix_naive_dates()

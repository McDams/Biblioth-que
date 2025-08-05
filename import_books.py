#!/usr/bin/env python
"""
Import du dataset Kaggle Goodreads Books
Fichier books.csv dans la racine du projet
"""

import os
import sys
import django
import pandas as pd
from datetime import date
import re
import random

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from books.models import Category, Author, Publisher, Book


def clean_text(text):
    """Nettoyer le texte"""
    if pd.isna(text) or not text:
        return ''
    return str(text).strip()


def parse_authors(authors_str):
    """Parser la chaîne d'auteurs"""
    if not authors_str:
        return []
    
    authors = []
    for author in authors_str.split(','):
        author = author.strip()
        if author:
            # Séparer prénom/nom
            parts = author.split()
            if len(parts) >= 2:
                first_name = ' '.join(parts[:-1])
                last_name = parts[-1]
            else:
                first_name = author
                last_name = ''
            
            authors.append({
                'first_name': first_name,
                'last_name': last_name
            })
    
    return authors


def clean_isbn(isbn):
    """Nettoyer l'ISBN"""
    if pd.isna(isbn):
        return ''
    
    isbn = str(isbn).strip()
    isbn = re.sub(r'[^0-9X]', '', isbn.upper())
    
    if len(isbn) in [10, 13]:
        return isbn
    
    return ''


def create_categories():
    """Créer les catégories de base"""
    categories_data = [
        {'name': 'Fiction', 'description': 'Romans et nouvelles'},
        {'name': 'Sciences', 'description': 'Livres scientifiques'},
        {'name': 'Histoire', 'description': 'Livres d\'histoire'},
        {'name': 'Biographie', 'description': 'Biographies'},
        {'name': 'Fantasy', 'description': 'Fantasy et fantastique'},
        {'name': 'Thriller', 'description': 'Thrillers et policiers'},
        {'name': 'Jeunesse', 'description': 'Livres jeunesse'},
        {'name': 'Art', 'description': 'Art et culture'},
        {'name': 'Informatique', 'description': 'Technologies'},
        {'name': 'Autres', 'description': 'Autres genres'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['name']] = category
    
    return categories


def import_books_from_csv():
    """Importer les livres depuis books.csv"""
    csv_file = 'books.csv'
    
    if not os.path.exists(csv_file):
        print(f"❌ Fichier {csv_file} non trouvé dans la racine du projet.")
        return
    
    print(f"📖 Import depuis {csv_file}...")
    
    try:
        # Lire le CSV avec gestion d'erreurs
        df = pd.read_csv(csv_file, on_bad_lines='skip', encoding='utf-8')
        print(f"📊 {len(df)} livres trouvés dans le dataset")
        
        # Limiter à 500 livres pour commencer
        df = df.head(500)
        
        # Créer les catégories
        categories = create_categories()
        
        # Compteurs
        books_created = 0
        authors_created = 0
        publishers_created = 0
        errors = 0
        
        for index, row in df.iterrows():
            try:
                # Extraire les données
                title = clean_text(row.get('title', ''))
                authors_str = clean_text(row.get('authors', ''))
                isbn = clean_isbn(row.get('isbn', ''))
                isbn13 = clean_isbn(row.get('isbn13', ''))
                
                # Validation de base
                if not title or not authors_str:
                    continue
                
                # ISBN final
                final_isbn = isbn13 if isbn13 else isbn
                if not final_isbn:
                    final_isbn = f"CSV{index:06d}"
                
                # Vérifier si existe
                if Book.objects.filter(isbn=final_isbn).exists():
                    continue
                
                # Traiter les auteurs
                authors_data = parse_authors(authors_str)
                book_authors = []
                
                for author_data in authors_data:
                    author, created = Author.objects.get_or_create(
                        first_name=author_data['first_name'],
                        last_name=author_data['last_name']
                    )
                    book_authors.append(author)
                    if created:
                        authors_created += 1
                
                # Éditeur
                publisher_name = clean_text(row.get('publisher', 'Éditeur Inconnu'))
                if not publisher_name:
                    publisher_name = 'Éditeur Inconnu'
                
                publisher, created = Publisher.objects.get_or_create(
                    name=publisher_name[:100]  # Limiter la longueur
                )
                if created:
                    publishers_created += 1
                
                # Date de publication
                try:
                    year = int(float(row.get('original_publication_year', 2000)))
                    if 1800 <= year <= 2024:
                        pub_date = date(year, 1, 1)
                    else:
                        pub_date = date(2000, 1, 1)
                except:
                    pub_date = date(2000, 1, 1)
                
                # Pages
                try:
                    pages = int(row.get('num_pages', 0))
                    pages = max(0, pages)
                except:
                    pages = 0
                
                # Note
                try:
                    rating = float(row.get('average_rating', 0))
                except:
                    rating = 0
                
                # Créer le livre
                book = Book.objects.create(
                    title=title[:200],
                    isbn=final_isbn,
                    publisher=publisher,
                    category=categories['Fiction'],  # Catégorie par défaut
                    publication_date=pub_date,
                    pages=pages,
                    language='Anglais',
                    summary=f"Note moyenne: {rating:.1f}/5. Importé depuis Kaggle Goodreads dataset.",
                    keywords='kaggle, goodreads',
                    total_copies=random.randint(2, 6),
                    available_copies=random.randint(1, 4),
                )
                
                # Ajouter les auteurs
                book.authors.set(book_authors)
                books_created += 1
                
                if books_created % 50 == 0:
                    print(f"  📚 {books_created} livres importés...")
                
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"  ❌ Erreur ligne {index}: {e}")
        
        print(f"\n✅ Import terminé:")
        print(f"   📚 {books_created} livres créés")
        print(f"   👥 {authors_created} auteurs créés")
        print(f"   🏢 {publishers_created} éditeurs créés")
        print(f"   ❌ {errors} erreurs")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")


def main():
    """Fonction principale"""
    print("=" * 50)
    print("📥 IMPORT DATASET KAGGLE")
    print("=" * 50)
    
    import_books_from_csv()
    
    print("\n" + "=" * 50)
    print("🎉 IMPORT TERMINÉ!")
    print("=" * 50)


if __name__ == '__main__':
    main()

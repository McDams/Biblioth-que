#!/usr/bin/env python
"""
Script de configuration initiale pour le système de gestion de bibliothèque

Usage:
    python setup_library.py
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from books.models import Category, Author, Publisher, Book
from datetime import date, datetime
from django.utils import timezone


def create_sample_data():
    """Créer des données d'exemple pour la bibliothèque"""
    
    print("🚀 Création des données d'exemple...")
    
    # Créer des catégories
    categories_data = [
        {'name': 'Fiction', 'description': 'Romans et nouvelles de fiction'},
        {'name': 'Science-Fiction', 'description': 'Science-fiction et fantasy'},
        {'name': 'Histoire', 'description': 'Livres d\'histoire et biographies'},
        {'name': 'Sciences', 'description': 'Livres scientifiques et techniques'},
        {'name': 'Philosophie', 'description': 'Philosophie et essais'},
        {'name': 'Jeunesse', 'description': 'Livres pour enfants et adolescents'},
        {'name': 'Informatique', 'description': 'Programmation et technologies'},
        {'name': 'Art', 'description': 'Beaux-arts et créativité'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['name']] = category
        if created:
            print(f"  ✓ Catégorie créée: {category.name}")
    
    # Créer des éditeurs
    publishers_data = [
        {'name': 'Gallimard', 'address': 'Paris, France'},
        {'name': 'Hachette', 'address': 'Paris, France'},
        {'name': 'Flammarion', 'address': 'Paris, France'},
        {'name': 'Seuil', 'address': 'Paris, France'},
        {'name': 'O\'Reilly Media', 'website': 'https://oreilly.com'},
        {'name': 'Eyrolles', 'address': 'Paris, France'},
        {'name': 'Dunod', 'address': 'Paris, France'},
    ]
    
    publishers = {}
    for pub_data in publishers_data:
        publisher, created = Publisher.objects.get_or_create(
            name=pub_data['name'],
            defaults=pub_data
        )
        publishers[pub_data['name']] = publisher
        if created:
            print(f"  ✓ Éditeur créé: {publisher.name}")
    
    # Créer des auteurs
    authors_data = [
        {'first_name': 'Victor', 'last_name': 'Hugo', 'nationality': 'Française'},
        {'first_name': 'Marcel', 'last_name': 'Proust', 'nationality': 'Française'},
        {'first_name': 'Albert', 'last_name': 'Camus', 'nationality': 'Française'},
        {'first_name': 'Isaac', 'last_name': 'Asimov', 'nationality': 'Américaine'},
        {'first_name': 'Arthur C.', 'last_name': 'Clarke', 'nationality': 'Britannique'},
        {'first_name': 'Yuval Noah', 'last_name': 'Harari', 'nationality': 'Israélienne'},
        {'first_name': 'Michelle', 'last_name': 'Obama', 'nationality': 'Américaine'},
        {'first_name': 'Antoine de', 'last_name': 'Saint-Exupéry', 'nationality': 'Française'},
        {'first_name': 'Agatha', 'last_name': 'Christie', 'nationality': 'Britannique'},
        {'first_name': 'Paulo', 'last_name': 'Coelho', 'nationality': 'Brésilienne'},
    ]
    
    authors = {}
    for author_data in authors_data:
        author, created = Author.objects.get_or_create(
            first_name=author_data['first_name'],
            last_name=author_data['last_name'],
            defaults=author_data
        )
        authors[f"{author_data['first_name']} {author_data['last_name']}"] = author
        if created:
            print(f"  ✓ Auteur créé: {author.get_full_name()}")
    
    # Créer des livres
    books_data = [
        {
            'title': 'Les Misérables',
            'isbn': '9782070409228',
            'authors': ['Victor Hugo'],
            'publisher': 'Gallimard',
            'category': 'Fiction',
            'publication_date': date(1862, 1, 1),
            'pages': 1900,
            'summary': 'Un chef-d\'œuvre de la littérature française qui suit les destins croisés de plusieurs personnages dans la France du XIXe siècle.',
            'keywords': 'classique, littérature française, histoire',
            'total_copies': 3,
            'available_copies': 3,
        },
        {
            'title': 'Du côté de chez Swann',
            'isbn': '9782070409235',
            'authors': ['Marcel Proust'],
            'publisher': 'Gallimard',
            'category': 'Fiction',
            'publication_date': date(1913, 11, 14),
            'pages': 420,
            'summary': 'Premier tome de "À la recherche du temps perdu", une exploration magistrale de la mémoire et du temps.',
            'keywords': 'classique, mémoire, littérature française',
            'total_copies': 2,
            'available_copies': 2,
        },
        {
            'title': 'L\'Étranger',
            'isbn': '9782070360024',
            'authors': ['Albert Camus'],
            'publisher': 'Gallimard',
            'category': 'Fiction',
            'publication_date': date(1942, 1, 1),
            'pages': 150,
            'summary': 'L\'histoire de Meursault, un homme indifférent qui tue un Arabe sur une plage d\'Alger.',
            'keywords': 'absurde, philosophie, existentialisme',
            'total_copies': 4,
            'available_copies': 4,
        },
        {
            'title': 'Foundation',
            'isbn': '9780553293357',
            'authors': ['Isaac Asimov'],
            'publisher': 'Hachette',
            'category': 'Science-Fiction',
            'publication_date': date(1951, 5, 1),
            'pages': 244,
            'summary': 'Premier tome de la série Fondation, une saga épique sur l\'avenir de l\'humanité.',
            'keywords': 'science-fiction, espace, futur',
            'total_copies': 3,
            'available_copies': 3,
        },
        {
            'title': '2001: A Space Odyssey',
            'isbn': '9780451457998',
            'authors': ['Arthur C. Clarke'],
            'publisher': 'Hachette',
            'category': 'Science-Fiction',
            'publication_date': date(1968, 1, 1),
            'pages': 297,
            'summary': 'Une odyssée à travers l\'espace et le temps, de la préhistoire au futur lointain.',
            'keywords': 'espace, intelligence artificielle, évolution',
            'total_copies': 2,
            'available_copies': 2,
        },
        {
            'title': 'Sapiens',
            'isbn': '9782226257017',
            'authors': ['Yuval Noah Harari'],
            'publisher': 'Flammarion',
            'category': 'Histoire',
            'publication_date': date(2014, 9, 4),
            'pages': 512,
            'summary': 'Une brève histoire de l\'humanité, de l\'âge de pierre à l\'ère moderne.',
            'keywords': 'anthropologie, histoire, société',
            'total_copies': 5,
            'available_copies': 5,
        },
        {
            'title': 'Le Petit Prince',
            'isbn': '9782070408504',
            'authors': ['Antoine de Saint-Exupéry'],
            'publisher': 'Gallimard',
            'category': 'Jeunesse',
            'publication_date': date(1943, 4, 6),
            'pages': 96,
            'summary': 'L\'histoire poétique d\'un petit prince qui voyage de planète en planète.',
            'keywords': 'enfance, philosophie, poésie',
            'total_copies': 6,
            'available_copies': 6,
        },
        {
            'title': 'Devenir',
            'isbn': '9782213717449',
            'authors': ['Michelle Obama'],
            'publisher': 'Flammarion',
            'category': 'Histoire',
            'publication_date': date(2018, 11, 13),
            'pages': 464,
            'summary': 'Les mémoires inspirantes de l\'ancienne Première Dame des États-Unis.',
            'keywords': 'biographie, politique, inspiration',
            'total_copies': 4,
            'available_copies': 4,
        },
    ]
    
    for book_data in books_data:
        # Récupérer les objets liés
        book_authors = [authors[name] for name in book_data['authors']]
        book_publisher = publishers[book_data['publisher']]
        book_category = categories[book_data['category']]
        
        # Supprimer les clés qui ne sont pas des champs du modèle
        book_fields = book_data.copy()
        del book_fields['authors']
        book_fields['publisher'] = book_publisher
        book_fields['category'] = book_category
        
        book, created = Book.objects.get_or_create(
            isbn=book_data['isbn'],
            defaults=book_fields
        )
        
        if created:
            # Ajouter les auteurs
            book.authors.set(book_authors)
            print(f"  ✓ Livre créé: {book.title}")
    
    print("\n✅ Données d'exemple créées avec succès!")
    print(f"   📚 {Book.objects.count()} livres")
    print(f"   👥 {Author.objects.count()} auteurs")
    print(f"   🏢 {Publisher.objects.count()} éditeurs")
    print(f"   📂 {Category.objects.count()} catégories")


def create_superuser():
    """Créer un superutilisateur si aucun n'existe"""
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        print("\n👑 Création du superutilisateur...")
        User.objects.create_user(
            username='admin',
            email='admin@bibliotheque.local',
            password='admin123',
            first_name='Admin',
            last_name='Bibliothèque',
            is_staff=True,
            is_superuser=True
        )
        print("  ✓ Superutilisateur créé:")
        print("     Username: admin")
        print("     Password: admin123")
        print("     Email: admin@bibliotheque.local")
    else:
        print("\n👑 Un superutilisateur existe déjà.")


def main():
    """Fonction principale de configuration"""
    print("=" * 60)
    print("🏛️  CONFIGURATION SYSTÈME DE GESTION BIBLIOTHÈQUE")
    print("=" * 60)
    
    try:
        # Vérifier les migrations
        print("\n🔄 Vérification des migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("  ✓ Migrations appliquées")
        
        # Créer le superutilisateur
        create_superuser()
        
        # Créer les données d'exemple
        create_sample_data()
        
        # Collecter les fichiers statiques
        print("\n📁 Collection des fichiers statiques...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("  ✓ Fichiers statiques collectés")
        
        print("\n" + "=" * 60)
        print("🎉 CONFIGURATION TERMINÉE AVEC SUCCÈS!")
        print("=" * 60)
        print("\n🚀 Pour démarrer le serveur:")
        print("   python manage.py runserver")
        print("\n🌐 Accès à l'application:")
        print("   http://127.0.0.1:8000")
        print("\n👨‍💼 Administration Django:")
        print("   http://127.0.0.1:8000/admin")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n📚 Bon développement!")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la configuration: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

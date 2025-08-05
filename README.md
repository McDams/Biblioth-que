# Système de Gestion de Bibliothèque

## Description

Application web complète de gestion de bibliothèque développée avec Django. Utilise **500 vrais livres** importés depuis le dataset Kaggle Goodreads avec auteurs, éditeurs et métadonnées authentiques.

## ⚡ Démarrage Rapide

```bash
# 1. Cloner le projet
git clone <url-du-repo>
cd Bibliothèque

# 2. Installer les dépendances
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Créer la base de données
python manage.py migrate
python manage.py createsuperuser

# 4. Importer les données (books.csv requis)
python import_books.py

# 5. Démarrer le serveur
python manage.py runserver
# ou: start.bat
```

**🌐 Application**: http://127.0.0.1:8000/  
**🔐 Admin**: http://127.0.0.1:8000/admin/

## 📚 Données Réelles Incluses

- **500 livres** du dataset Kaggle Goodreads
- **356 auteurs** réels
- **246 éditeurs** authentiques
- **10 catégories** organisées
- **Métadonnées complètes** (ISBN, pages, notes, dates)

## Fonctionnalités

### Pour les Utilisateurs

- ✅ Inscription et connexion
- ✅ Consultation du catalogue de livres
- ✅ Recherche et filtrage des livres
- ✅ Demande d'emprunt de livres
- ✅ Historique des emprunts

### Pour les Administrateurs

- ✅ Gestion complète du catalogue
- ✅ Gestion des utilisateurs
- ✅ Gestion des emprunts et retours
- ✅ Interface d'administration Django
- ✅ Base de données réelle avec 500+ livres

## Technologies Utilisées

- **Backend:** Django 4.2.7
- **Base de données:** SQLite (développement)
- **Frontend:** Bootstrap 4, HTML5, CSS3, JavaScript
- **Données:** Dataset Kaggle Goodreads (11,000+ livres)
- **APIs:** Import CSV automatisé

## Installation

### Prérequis

- Python 3.8+
- PostgreSQL
- Git

### Configuration locale

1. Cloner le projet

```bash
git clone <url-du-repo>
cd Bibliothèque
```

2. **Installation automatique (Recommandé)**

```bash
# Windows
setup.bat

# Ou manuellement:
python setup_library.py
```

3. **Import de données réelles**

```bash
# Données d'exemple (20 livres célèbres)
python import_real_data.py

# Dataset Kaggle (11,000+ livres)
# 1. Télécharger books.csv depuis: https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks
# 2. Placer dans le dossier du projet
python import_kaggle.py

# Google Books API (temps réel)
python import_google_books.py --query "programming" --max 50
```

4. **Démarrage rapide**

```bash
# Windows
start_server.bat

# Ou manuellement:
python manage.py runserver
```

### Installation Manuelle

2. Créer un environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Installer les dépendances

```bash
pip install -r requirements.txt
```

4. Configuration de la base de données

- Créer une base PostgreSQL
- Copier `.env.example` vers `.env`
- Configurer les variables d'environnement

5. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

7. Lancer le serveur

```bash
python manage.py runserver
```

## 📚 Sources de Données Réelles

Ce projet utilise de vraies données de bibliothèques pour un rendu professionnel :

### Datasets Inclus

- **20+ livres célèbres** avec métadonnées complètes
- **Auteurs réels** (Harper Lee, George Orwell, J.K. Rowling...)
- **ISBN valides** et informations vérifiées
- **Catégories étendues** (Fiction, Science-Fiction, Histoire...)

### Sources Externes

- **Kaggle Goodreads**: 11,000+ livres avec notes
- **Google Books API**: Import en temps réel
- **BNF Data**: Catalogue français officiel
- **Open Library**: Millions de livres

📖 Voir `DATA_SOURCES.md` pour la liste complète des sources.

## Configuration Production

### Variables d'environnement

Créer un fichier `.env` avec :

```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_NAME=your-db-name
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Structure du Projet

```
Bibliothèque/
├── library_project/          # Configuration principale
├── accounts/                 # Gestion utilisateurs
├── books/                   # Gestion catalogue
├── loans/                   # Gestion emprunts
├── dashboard/               # Tableau de bord admin
├── static/                  # Fichiers statiques
├── templates/               # Templates HTML
├── media/                   # Fichiers uploadés
├── import_real_data.py      # Import données d'exemple
├── import_kaggle.py         # Import dataset Kaggle
├── import_google_books.py   # Import Google Books API
├── DATA_SOURCES.md          # Guide des sources de données
├── setup.bat                # Installation automatique
├── start_server.bat         # Démarrage serveur
└── manage.py
```

## 📊 Scripts d'Import de Données

### 1. Données d'Exemple (Immédiat)

```bash
python import_real_data.py
```

- 20 livres célèbres avec métadonnées complètes
- Auteurs réels (Harper Lee, Orwell, Rowling...)
- ISBN valides, catégories étendues

### 2. Dataset Kaggle Goodreads (Recommandé)

```bash
# 1. Télécharger: https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks
# 2. Placer books.csv dans le projet
python import_kaggle.py
```

- 11,000+ livres avec notes Goodreads
- Métadonnées complètes et vérifiées

### 3. Google Books API (Temps Réel)

```bash
python import_google_books.py --query "programming" --max 50
python import_google_books.py --category fiction --max 100
```

- Import dynamique depuis l'API officielle
- Images de couverture incluses

## Fonctionnalités Détaillées

### Gestion du Catalogue

- Ajout/modification/suppression de livres
- Catégorisation
- Gestion des stocks
- Upload d'images de couverture
- Import/export de données

### Système d'Emprunts

- Emprunts avec dates de retour
- Gestion des retards
- Notifications automatiques
- Historique complet

### Tableau de Bord

- Statistiques en temps réel
- Graphiques de performance
- Rapports personnalisés
- Export de données

## API Endpoints

### Authentification

- `POST /accounts/login/` - Connexion
- `POST /accounts/register/` - Inscription
- `POST /accounts/logout/` - Déconnexion

### Catalogue

- `GET /books/` - Liste des livres
- `GET /books/<id>/` - Détail d'un livre
- `POST /books/` - Ajouter un livre (admin)

### Emprunts

- `GET /loans/` - Historique des emprunts
- `POST /loans/borrow/` - Emprunter un livre
- `POST /loans/return/` - Retourner un livre

## Tests

```bash
python manage.py test
```

## Déploiement

Le projet est configuré pour un déploiement facile avec :

- Whitenoise pour les fichiers statiques
- Gunicorn comme serveur WSGI
- Configuration PostgreSQL

## Contributeurs

- Votre Nom - Développeur Principal

## Licence

MIT License

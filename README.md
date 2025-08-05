# Système de Gestion de Bibliothèque

## Description

Application web complète de gestion de bibliothèque développée avec Django. Cette application permet de gérer un catalogue de livres, les emprunts, les utilisateurs et fournit un tableau de bord administrateur complet.

## Fonctionnalités

### Pour les Utilisateurs

- ✅ Inscription et connexion
- ✅ Consultation du catalogue de livres
- ✅ Recherche et filtrage des livres
- ✅ Demande d'emprunt de livres
- ✅ Historique des emprunts
- ✅ Profil utilisateur

### Pour les Administrateurs

- ✅ Gestion complète du catalogue
- ✅ Gestion des utilisateurs
- ✅ Gestion des emprunts et retours
- ✅ Tableau de bord avec statistiques
- ✅ Rapports et exports
- ✅ Gestion des catégories

## Technologies Utilisées

- **Backend:** Django 4.2.7
- **Base de données:** PostgreSQL
- **Frontend:** Bootstrap 4, HTML5, CSS3, JavaScript
- **Authentification:** Django Auth System
- **Rapports:** ReportLab (PDF), OpenPyXL (Excel)

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
└── manage.py
```

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

@echo off
title Système de Gestion Bibliothèque - Serveur

echo =========================================================
echo   DEMARRAGE DU SERVEUR BIBLIOTHEQUE
echo =========================================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo ERREUR: Environnement virtuel non trouve
    echo Veuillez executer setup.bat d'abord
    pause
    exit /b 1
)

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo Verification des migrations...
python manage.py makemigrations --check --dry-run >nul 2>&1
if not errorlevel 1 (
    echo Application des nouvelles migrations...
    python manage.py makemigrations
    python manage.py migrate
)

echo.
echo =========================================================
echo   SERVEUR DEMARRE
echo =========================================================
echo.
echo Application disponible sur : http://127.0.0.1:8000
echo Administration Django : http://127.0.0.1:8000/admin
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

python manage.py runserver

@echo off
title Système de Gestion Bibliothèque - Configuration

echo =========================================================
echo   SYSTEME DE GESTION BIBLIOTHEQUE - CONFIGURATION
echo =========================================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

echo Python detecte : 
python --version

echo.
echo 1. Creation de l'environnement virtuel...
python -m venv venv
if errorlevel 1 (
    echo ERREUR: Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)

echo 2. Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo 3. Installation des dependances...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERREUR: Impossible d'installer les dependances
    pause
    exit /b 1
)

echo 4. Configuration de la base de donnees et donnees d'exemple...
python setup_library.py
if errorlevel 1 (
    echo ERREUR: Probleme lors de la configuration
    pause
    exit /b 1
)

echo.
echo =========================================================
echo   CONFIGURATION TERMINEE AVEC SUCCES!
echo =========================================================
echo.
echo Pour demarrer l'application :
echo   1. Activez l'environnement virtuel : venv\Scripts\activate
echo   2. Lancez le serveur : python manage.py runserver
echo   3. Ouvrez votre navigateur : http://127.0.0.1:8000
echo.
echo Administration Django : http://127.0.0.1:8000/admin
echo   Username: admin
echo   Password: admin123
echo.
pause

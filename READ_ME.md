README: FastAPI pour les Évènements Culturels

Description

Cette API, construite avec FastAPI, permet de gérer et d'analyser des évènements culturels. Elle utilise un fichier CSV contenant les informations des évènements pour fournir plusieurs fonctionnalités, notamment :

Lister les évènements à venir.

Filtrer les évènements par date ou par météo.

Ajouter des informations météorologiques basées sur la latitude et la longitude.

Afficher des métadonnées sur le projet.

Prérequis

Avant de lancer cette API, vous devez :

Installer les dépendances :

pip install fastapi pandas uvicorn requests

Fichiers nécessaires :

better_result.csv : Contient les données des évènements.

metadata.json : Contient les métadonnées pour l'API.

Configurer l'API météo :

L'API utilise OpenWeatherMap pour ajouter des informations météo. Assurez-vous d'avoir une clé API valide.

Remplacez api_key par votre clé API dans le fichier Python.

Étapes Préparatoires

Utiliser Parsehub ou un autre programme de parsing pour générer les données initiales dans un fichier CSV.

Lancer les programmes better_csv.py et removeline.py pour nettoyer et préparer les données avant de démarrer l'API.

Fonctionnalités

Endpoints Disponibles

Racine de l'API :

GET / :

{
  "message": "Bienvenue dans l'API FastAPI des évènements culturels."
}

Lister les évènements à venir :

GET /evenements

Retourne une liste des évènements à venir.

Filtrer par date :

GET /evenements/{date}

Paramètre : date au format YYYY-MM-DD.

Retourne les évènements pour une date spécifique.

Métadonnées :

GET /evenements/metadata

Retourne les colonnes et le nombre total d'évènements.

Filtrer par météo :

GET /evenements/meteo/{meteo}

Paramètre : meteo (ex. "ensoleillé", "pluvieux").

Retourne les évènements correspondant à une météo spécifique.

Ajouter des informations météo :

POST /evenements/ajouter-meteo

Ajoute une colonne météo en utilisant les coordonnées (latitude, longitude) des évènements.

Lancement de l'API

Démarrer le serveur :

uvicorn fastapi_meteo:app --reload

Accéder à la documentation interactive :

Ouvrez http://127.0.0.1:8000/docs pour Swagger UI.

Structure des Données

Fichier better_result.csv

Le fichier CSV doit inclure les colonnes suivantes :

id : Identifiant unique.

date : Date de l'évènement (format ISO 8601).

latitude, longitude : Coordonnées géographiques.

meteo : Description de la météo (ajoutée automatiquement).

Fichier metadata.json

Exemple :

{
  "columns": ["id", "date", "latitude", "longitude", "meteo"],
  "total_events": 100
}

Notes

L'API renverra des erreurs claires si des colonnes nécessaires sont absentes ou si les données sont mal formatées.

Les programmes better_csv.py et removeline.py doivent être exécutés pour préparer correctement le fichier CSV.

La clé API pour OpenWeatherMap est essentielle pour utiliser la fonctionnalité météo.

Limitations

Les données météo sont récupérées uniquement pour les évènements ayant des coordonnées valides.

Assurez-vous que le fichier CSV est encodé correctement (UTF-8 ou latin1).

Auteurs

Simona Müller
Boris Pahnke

Licence

Ce projet est sous licence MIT.
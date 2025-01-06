import numpy as numpy
import matplotlib.pyplot as plt
import pandas as pd
import locale
from datetime import datetime
import re

filename = "C:\\Users\\coral\\Desktop\\Travail_de_Groupe\\better_result_25_11_2024_copie.csv"

# Configurer la locale pour le français
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # Pour les systèmes Unix/Linux/Mac
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR')  # Alternative pour Windows
    except locale.Error:
        print("Impossible de définir la locale en français. Assurez-vous que le package de locale française est installé.")

donnees = pd.read_csv(filename, sep=',')

donnees = donnees.dropna(axis=0)

donnees = donnees.drop([165, 47, 65, 118, 8, 35, 83, 84, 88, 91, 94, 85, 99, 100, 105, 121, 122, 126, 140, 141, 174, 21, 27, 109, 162 ], axis=0)

def clean_date(date_str):
   date_str = date_str.strip()  # Enlever les espaces avant et après
   return date_str

# Appliquer la fonction de nettoyage
donnees['evenement_date'] = donnees['evenement_date'].apply(clean_date)

print(donnees['evenement_date'])

# Expression régulière mise à jour pour accepter les jours à un ou deux chiffres
regex = r"^(Dimanche|Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi) (\d{1,2}) (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre), (\d{1,2})h(\d{0,2})$"

print(donnees.loc[111])

# Fonction pour parser les dates avec l'année 2024
def parse_date(date_str):
    # Vérifier si la date correspond à la regex
    match = re.match(regex, date_str)
    if match:
        # Extraire les composants de la date
        day_of_week = match.group(1)  # Jour de la semaine (ex: Dimanche)
        day = match.group(2).zfill(2)  # Jour (ajouter un zéro si nécessaire)
        month = match.group(3)  # Mois (ex: décembre)
        hour = match.group(4)  # Heure
        minute = match.group(5).zfill(2) if match.group(5) else '00'  # Minute (ajouter :00 si pas de minutes)
        
        # Recombiner la date sous la forme "Jour Mois Jour Heure:Minute 2024"
        date_str = f"{day_of_week} {day} {month}, {hour}:{minute} 2024"
        print(date_str)
        # Convertir la chaîne en datetime avec to_datetime
        try:
            return pd.to_datetime(date_str, format="%A %d %B, %H:%M %Y")
        except ValueError:
            return pd.NaT  # Retourne NaT si la conversion échoue
    
    return pd.NaT  # Retourne NaT si aucun format ne correspond
print(pd.NaT)
print(pd.to_datetime)
print(donnees['evenement_date'])

# Appliquer la fonction
donnees['evenement_date'] = donnees['evenement_date'].apply(parse_date)

# Affichage des résultats
#print(donnees['evenement_date'])

# Vérification des lignes où la conversion échoue
invalid_dates = donnees[donnees['evenement_date'].isna()]
if not invalid_dates.empty:
    print("Lignes échouant à la conversion :")
    print(invalid_dates)

donnees = donnees.dropna(axis=0)

donnees = donnees.drop('evenement_tarif', axis=1)

donnees.to_csv("C:\\Users\\coral\\Desktop\\Travail_de_Groupe\\resultatss_09122024.csv", sep=',')




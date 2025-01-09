from fastapi import FastAPI, HTTPException
import pandas as pd
import json
import requests
from datetime import datetime, timedelta

# Charger les données CSV
df = pd.read_csv("better_result.csv")

# Assurez-vous que les colonnes "date" et "meteo" existent et sont bien formatées
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Créer l'application FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    """
    Endpoint racine de l'API.
    """
    return {"message": "Bienvenue dans l'API FastAPI des évènements culturels."}

@app.get("/evenements")
def get_evenements():
    """
    Récupérer tous les évènements à venir.
    """
    maintenant = datetime.now()
    evenements_a_venir = df[df['date'] >= maintenant]
    if evenements_a_venir.empty:
        return {"message": "Aucun évènement à venir."}
    return evenements_a_venir.to_dict(orient="records")

@app.get("/evenements/{date}")
def get_evenements_par_date(date: str):
    """
    Récupérer tous les évènements à une date spécifique.
    Format attendu pour la date : YYYY-MM-DD
    """
    try:
        date_choisie = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD.")

    maintenant = datetime.now()
    if date_choisie > maintenant + timedelta(days=4):
        raise HTTPException(status_code=400, detail="Données météo indisponibles pour cette date.")

    evenements_a_la_date = df[df['date'] == date_choisie]
    if evenements_a_la_date.empty:
        raise HTTPException(status_code=404, detail="Aucun évènement trouvé pour cette date.")

    return evenements_a_la_date[['date', 'meteo']].to_dict(orient="records")

@app.get("/evenements/metadata")
def get_metadata():
    """
    Afficher les métadonnées du projet.
    """
    try:
        with open("metadata.json", "r") as f:
            metadata = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Le fichier metadata.json est introuvable.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Erreur lors de la lecture de metadata.json.")

    return metadata

@app.get("/evenements/meteo/{meteo}")
def get_evenements_par_meteo(meteo: str):
    """
    Récupérer tous les évènements en fonction de la météo spécifiée.
    Vous pouvez choisir parmi les options suivantes: 
    """
    evenements_meteo = df[df['meteo'].str.lower() == meteo.lower()]
    if evenements_meteo.empty:
        raise HTTPException(status_code=404, detail="Aucun évènement trouvé pour cette météo.")

    return evenements_meteo.to_dict(orient="records")

@app.post("/evenements/ajouter-meteo")
def ajouter_colonne_meteo():
    """
    Ajouter une colonne météo à chaque ligne en fonction de la longitude et de la latitude (sauf pour /evenements/metadata).
    """
    if not {'latitude', 'longitude'}.issubset(df.columns):
        raise HTTPException(status_code=400, detail="Les colonnes 'latitude' et 'longitude' doivent exister dans le fichier CSV.")

    api_key = "3de4423688c70ab54243991f5ce50f38"
    base_url = "https://api.openweathermap.org/data/2.5/forecast"

    meteo_data = []

    for index, row in df.iterrows():
        lat = row['latitude']
        lon = row['longitude']

        url = f"{base_url}?lat={lat}&lon={lon}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Extraire les informations météo pertinentes
            meteo = data['list'][0]['weather'][0]['description'] if 'list' in data and data['list'] else "Non disponible"
            meteo_data.append(meteo)
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'interrogation de l'API pour les coordonnées ({lat}, {lon}): {e}")
            meteo_data.append("Erreur API")

    df['meteo'] = meteo_data
    df.to_csv("better_result.csv", index=False)

    return {"message": "La colonne météo a été ajoutée avec succès, sauf pour les métadonnées."}
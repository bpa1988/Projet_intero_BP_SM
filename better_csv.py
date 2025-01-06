import pandas as pd
import re

events_csv_path = "C:/Users/simon/Documents/heg/Semestre 5/interopérabilité/Projet/Parser/run_results4.csv"

test = pd.read_csv(events_csv_path)

def extract_lat_long_from_html(html_content):
    """
    Extracts latitude and longitude directly from the Google Maps link in the HTML string.
    """
    # Expression régulière pour capturer les coordonnées GPS dans le lien Google Maps
    match = re.search(r"https://www\.google\.com/maps/@(-?\d+\.\d+),(-?\d+\.\d+)", html_content)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

sad = test["evenement_lieu"][0]
asd = extract_lat_long_from_html(sad)
print(asd)

def better_csv(df):
    """
    Transforms the evenement_lieu column to only retain latitude and longitude.
    Handles NaN values in the evenement_lieu column.
    """
    # Appliquer la fonction pour extraire les coordonnées, en gérant les valeurs NaN
    df[["latitude", "longitude"]] = df["evenement_lieu"].apply(
        lambda x: pd.Series(extract_lat_long_from_html(x)) if pd.notna(x) else pd.Series([None, None])
    )
    # Supprimer la colonne d'origine si nécessaire
    df.drop(columns=["evenement_lieu"], inplace=True)
    return df

awd = better_csv(test)
print(awd.head())

# save csv in dir
awd.to_csv("C:/Users/simon/Documents/heg/Semestre 5/interopérabilité/Projet/Parser/better_result.csv", index=False)
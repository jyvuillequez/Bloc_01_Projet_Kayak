# src/data/osm_api.py

import json
import time

import requests
import pandas as pd
import yaml

from src.config import RAW_DIR, CONFIG_DIR

OSM_BASE_URL = "https://nominatim.openstreetmap.org/search"

# Chargement config
def load_cities():
    """Charge la liste des villes depuis data/config/cities.json."""
    cities_path = CONFIG_DIR / "cities.json"
    with open(cities_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_parameters():
    """Charge les paramètres globaux depuis data/config/parameters.yml."""
    params_path = CONFIG_DIR / "parameters.yml"
    with open(params_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Appels API OSM
def fetch_osm_city(city, country, user_agent):
    """Appelle l'API OSM pour une ville et renvoie la liste de résultats JSON."""
    params = {
        "q": f"{city}, {country}",
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    }
    headers = {"User-Agent": user_agent}

    response = requests.get(OSM_BASE_URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_osm_cities(cities, country, sleep_seconds, user_agent):
    """
    Appelle OSM pour une liste de villes et renvoie un DataFrame
    avec city, lat, lon, display_name.
    """
    records = []

    for city in cities:
        try:
            results = fetch_osm_city(city, country=country, user_agent=user_agent)

            if not results:
                records.append(
                    {"city": city, "lat": None, "lon": None, "display_name": None}
                )
                continue

            best = results[0]
            records.append(
                {
                    "city": city,
                    "lat": float(best.get("lat")),
                    "lon": float(best.get("lon")),
                    "display_name": best.get("display_name"),
                }
            )

        except Exception as e:
            print(f"Erreur pour la ville '{city}': {e}")
            records.append(
                {"city": city, "lat": None, "lon": None, "display_name": None}
            )

        # Pour ne pas spammer OSM
        time.sleep(sleep_seconds)

    return pd.DataFrame(records)


# Utilitaires
def save_osm_df(df, filename="coord_gps_osm.csv"):
    """Sauvegarde le DataFrame dans data/raw/."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_DIR / filename, index=False)


def coords_to_dict(df):
    """
    Transforme le DataFrame en dictionnaire :
    { "Paris": {"lat": 48.85, "lon": 2.35}, ... }
    """
    return {
        row["city"]: {"lat": row["lat"], "lon": row["lon"]}
        for _, row in df.iterrows()
    }

# Exécution directe (test manuel)
if __name__ == "__main__":
    params = load_parameters()
    cities = load_cities()

    df = fetch_osm_cities(
        cities=cities,
        country=params["country"],
        sleep_seconds=params["osm"]["sleep_seconds"],
        user_agent=params["osm"]["user_agent"],
    )

    print(df.head())
    save_osm_df(df)

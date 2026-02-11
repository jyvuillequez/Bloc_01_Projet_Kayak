# src/data/openweather_api.py

import os
import time
from typing import Dict, Any

import requests
import pandas as pd
import yaml
from dotenv import load_dotenv, find_dotenv

from src.config import RAW_DIR, CONFIG_DIR


# Variables d'environnement
load_dotenv(find_dotenv(), override=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise RuntimeError("API Key OpenWeather manquante.")


# Chargement paramètres
def load_parameters() -> dict:
    """Charge les paramètres globaux depuis data/config/parameters.yml."""
    params_path = CONFIG_DIR / "parameters.yml"
    with open(params_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Appels API OpenWeather (One Call 3.0)
def fetch_daily_weather_for_coord(
    lat: float,
    lon: float,
    api_key: str,
    endpoint: str,
    units: str = "metric",
    lang: str = "fr",
    exclude: str = "current,minutely,hourly,alerts",
) -> Dict[str, Any]:
    """
    Appelle l'API OpenWeather One Call 3.0 pour une paire (lat, lon).
    On récupère 'daily' comme dans ton notebook.
    """
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,
        "lang": lang,
        "exclude": exclude,
    }

    response = requests.get(endpoint, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def daily_json_to_rows(data: Dict[str, Any], city: str) -> list[dict]:
    """
    Transforme la clé 'daily' de la réponse JSON en liste de lignes
    (c'est ce que tu faisais dans la boucle `for day in data["daily"]`).
    """
    if "daily" not in data:
        return []

    rows: list[dict] = []
    for day in data["daily"]:
        rows.append(
            {
                "city": city,
                "date": pd.to_datetime(day["dt"], unit="s", utc=True).date(),
                "temp_day": day["temp"]["day"],
                "temp_night": day["temp"]["night"],
                "humidity": day["humidity"],
                "pop": day.get("pop", 0),
                "rain": day.get("rain", 0),
            }
        )
    return rows


def fetch_daily_weather_for_cities(
    df_cities: pd.DataFrame,
    api_key: str,
    endpoint: str,
    units: str,
    lang: str,
    exclude: str,
    sleep_seconds: float = 1.0,
) -> pd.DataFrame:
    """
    Boucle :

    for _, row in df_cities.iterrows():
        data = get_weather(row["lat"], row["lon"])
        ...

    df_cities doit avoir au moins : ["city", "lat", "lon"]
    """
    all_rows: list[dict] = []

    for _, row in df_cities.iterrows():
        city = row["city"]
        lat = row["lat"]
        lon = row["lon"]

        if pd.isna(lat) or pd.isna(lon):
            print(f"Coordonnées manquantes pour {city}.")
            continue

        try:
            data = fetch_daily_weather_for_coord(
                lat=lat,
                lon=lon,
                api_key=api_key,
                endpoint=endpoint,
                units=units,
                lang=lang,
                exclude=exclude,
            )
            rows = daily_json_to_rows(data, city=city)
            all_rows.extend(rows)

        except Exception as e:
            print(f"Erreur pour la ville '{city}': {e}")

        time.sleep(sleep_seconds)

    if not all_rows:
        return pd.DataFrame()

    return pd.DataFrame(all_rows)


# Utilitaires
def load_osm_coords(filename: str = "coord_gps_osm.csv") -> pd.DataFrame:
    """
    Charge le fichier des coordonnées OSM produit par osm_api.py
    depuis data/raw/coord_gps_osm.csv.
    """
    path = RAW_DIR / filename
    return pd.read_csv(path)


def save_weather_df(df: pd.DataFrame, filename: str = "openweather_daily.csv") -> None:
    """Sauvegarde le DataFrame météo dans data/raw/openweather_daily.csv."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_DIR / filename, index=False)


# Exécution directe (test manuel)
if __name__ == "__main__":
    params = load_parameters()
    endpoint = params["weather"]["endpoint"]
    units = params["weather"]["units"]
    lang = params["weather"]["lang"]
    sleep_seconds = params["weather"]["sleep_seconds"]
    exclude = params["weather"]["exclude"]

    df_cities = load_osm_coords()  # lit data/raw/coord_gps_osm.csv
    print(df_cities.head())

    df_weather = fetch_daily_weather_for_cities(
        df_cities=df_cities,
        api_key=API_KEY,
        endpoint=endpoint,
        units=units,
        lang=lang,
        exclude=exclude,
        sleep_seconds=sleep_seconds,
    )

    print(df_weather.head())
    save_weather_df(df_weather)
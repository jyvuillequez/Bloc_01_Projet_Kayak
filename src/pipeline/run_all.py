# src/pipeline/run_all.py

from pathlib import Path
import sys

# "src" importable si fichier lancé directement ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Imports des modules du projet
from src.data.osm_api import load_cities, fetch_osm_cities, save_osm_df
from src.data.openweather_api import (
    load_parameters,
    load_osm_coords,
    fetch_daily_weather_for_cities,
    save_weather_df,
    API_KEY,
)
from src.features.join_osm_weather import run_join_step
from src.io.aws_s3 import upload_all

def main():
    # Charger les paramètres globaux (issus du fichier : data/config/parameters.yml)
    params = load_parameters()

    country = params["country"]

    osm_user_agent = params["osm"]["user_agent"]
    osm_sleep = params["osm"]["sleep_seconds"]

    endpoint = params["weather"]["endpoint"]
    units = params["weather"]["units"]
    lang = params["weather"]["lang"]
    exclude = params["weather"]["exclude"]
    weather_sleep = params["weather"]["sleep_seconds"]

    # Étape OSM : villes lat/lon
    cities = load_cities()
    df_osm = fetch_osm_cities(
        cities=cities,
        country=country,
        user_agent=osm_user_agent,
        sleep_seconds=osm_sleep,
    )
    save_osm_df(df_osm)  # data/raw/coord_gps_osm.csv

    # Étape OpenWeather : lat/lon + météo quotidienne
    df_cities = load_osm_coords()  # lecture de data/raw/coord_gps_osm.csv
    df_weather = fetch_daily_weather_for_cities(
        df_cities=df_cities,
        api_key=API_KEY,
        endpoint=endpoint,
        units=units,
        lang=lang,
        exclude=exclude,
        sleep_seconds=weather_sleep,
    )
    save_weather_df(df_weather)  # data/raw/openweather_daily.csv

    # Étape Join : OSM + météo
    run_join_step()

    # Étape S3 : upload des CSV raw + outputs
    upload_all()


if __name__ == "__main__":
    main()
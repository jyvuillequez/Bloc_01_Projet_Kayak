# src/features/join_osm_weather.py

from pathlib import Path
import sys

import pandas as pd

# --- Pour que "src" soit importable même si on lance ce fichier directement ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config import RAW_DIR, OUTPUT_DIR


def load_osm(filename: str = "coord_gps_osm.csv") -> pd.DataFrame:
    """Charge les coordonnées OSM depuis data/raw/."""
    path = RAW_DIR / filename
    return pd.read_csv(path)


def load_weather(filename: str = "openweather_daily.csv") -> pd.DataFrame:
    """Charge les données météo quotidiennes depuis data/raw/."""
    path = RAW_DIR / filename
    return pd.read_csv(path)


def join_osm_weather(
    df_osm: pd.DataFrame,
    df_weather: pd.DataFrame,
) -> pd.DataFrame:
    """
    Joint les coordonnées OSM avec la météo quotidienne.

    df_osm : colonnes attendues -> ['city', 'lat', 'lon', ...]
    df_weather : colonnes attendues -> ['city', 'date', 'temp_day', 'temp_night', 'humidity', 'pop', 'rain', ...]

    Retour : une ligne par (city, date) avec lat/lon + variables météo.
    """
    # On s'assure que 'city' est bien de type string des deux côtés
    df_osm["city"] = df_osm["city"].astype(str)
    df_weather["city"] = df_weather["city"].astype(str)

    df_join = df_weather.merge(
        df_osm[["city", "lat", "lon"]],
        on="city",
        how="left",
    )

    return df_join


def save_joined(df: pd.DataFrame, filename: str = "osm_weather_daily.csv") -> None:
    """Sauvegarde la table jointe dans data/outputs/."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DIR / filename, index=False)


def run_join_step():
    """Étape complète : chargement + jointure + sauvegarde."""
    df_osm = load_osm()
    df_weather = load_weather()
    df_join = join_osm_weather(df_osm, df_weather)
    save_joined(df_join)
    print(df_join.head())


if __name__ == "__main__":
    run_join_step()

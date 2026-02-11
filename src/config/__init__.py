# src/config/__init__.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CONFIG_DIR = DATA_DIR / "config"
OUTPUT_DIR = DATA_DIR / "outputs"

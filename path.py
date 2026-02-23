from pathlib import Path

BASE_PATH: Path = Path(__file__).resolve().parent
ICONS_PATH: Path = BASE_PATH / "icons"
MODELS_PATH: Path = BASE_PATH / "models"
DATA_PATH: Path = BASE_PATH / "data"
CACHE_PATH: Path = DATA_PATH / "cache"
SEGMENTATION_PATH: Path = DATA_PATH / "segmentation"
LOGS_PATH: Path = BASE_PATH / "logs"
STYLESHEET_PATH: Path = BASE_PATH / "stylesheet"

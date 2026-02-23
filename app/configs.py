from dataclasses import dataclass

from PySide6.QtCore import QSettings

from path import BASE_PATH


@dataclass
class AppConfig:
    width: int = 1500
    height: int = 1200
    theme: str = "dark"


class ConfigManager:
    _CONFIG_FILE = "config.ini"

    def __init__(self):
        config_path = BASE_PATH / self._CONFIG_FILE
        self._settings = QSettings(str(config_path), QSettings.IniFormat)

    def load(self) -> AppConfig:
        return AppConfig(
            width=int(self._settings.value("window/width", 1500)),
            height=int(self._settings.value("window/height", 1200)),
            theme=self._settings.value("window/theme", "dark"),
        )

    def save(self, config: AppConfig):
        self._settings.setValue("window/width", config.width)
        self._settings.setValue("window/height", config.height)
        self._settings.setValue("window/theme", config.theme)
        self._settings.sync()

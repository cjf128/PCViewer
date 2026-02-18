from dataclasses import dataclass
from PySide6.QtCore import QSettings

@dataclass
class AppConfig:
    theme: str = "dark"
    language: str = "zh"
    width: int = 900
    height: int = 600


class ConfigManager:
    def __init__(self):
        self._settings = QSettings("MyCompany", "MyApp")

    def load(self) -> AppConfig:
        return AppConfig(
            theme=self._settings.value("theme", "dark"),
            language=self._settings.value("language", "zh"),
            width=int(self._settings.value("window/width", 900)),
            height=int(self._settings.value("window/height", 600)),
        )

    def save(self, config: AppConfig):
        self._settings.setValue("theme", config.theme)
        self._settings.setValue("language", config.language)
        self._settings.setValue("window/width", config.width)
        self._settings.setValue("window/height", config.height)


from app.configs import ConfigManager
from widgets.MainWindow import MainWindow


class App:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load()

        self.main_window = MainWindow(self.config)

    def run(self):
        self.main_window.show()

    def shutdown(self):
        self.config_manager.save(self.config)

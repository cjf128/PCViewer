from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.app import App
from path import BASE_PATH
from scripts.logger import setup_logger, log_info, log_error

def main():
    setup_logger()
    log_info("应用程序启动")
    
    try:
        app = QApplication([])
        app.setWindowIcon(QIcon(str(BASE_PATH / "icons" / "logo.ico")))
        app.setStyle('Fusion')
        application = App()
        application.run()
        log_info("应用程序初始化完成")
        app.exec()
    except Exception as e:
        log_error(f"应用程序运行错误: {e}")
        raise
    finally:
        log_info("应用程序退出")

if __name__ == "__main__":
    main()

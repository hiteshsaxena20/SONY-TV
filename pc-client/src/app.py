import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SONY TV Remote")
    
    window = MainWindow()
    window.show()
    
    return app.exec()

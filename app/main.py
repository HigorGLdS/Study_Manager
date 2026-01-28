from PySide6.QtWidgets import QApplication
import sys

from ui.main_window import MainWindow
from ui.styles.theme import load_theme


def main():
    app = QApplication(sys.argv)
    load_theme(app, "dark")

    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
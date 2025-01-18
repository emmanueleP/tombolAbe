import sys
from PyQt5.QtWidgets import QApplication
from src.gui import TombolaApp

def main():
    app = QApplication(sys.argv)
    
    # Carica il file di stile
    with open('style.qss', 'r') as f:
        app.setStyleSheet(f.read())
    
    window = TombolaApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

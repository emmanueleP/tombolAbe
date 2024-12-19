from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informazioni")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        info_text = QLabel("""
            <h2>Tombola del Dono</h2>
            <p>Versione 1.0</p>
            <p>© 2024 - Emmanuele Pani. Under MIT License</p>
            <p>Un'applicazione per giocare a tombola in modo solidale e divertente durante le feste natalizie.</p>
            <p>Written with Python and PyQt5.</p>
        """)
        info_text.setTextFormat(Qt.RichText)
        info_text.setAlignment(Qt.AlignCenter)
        info_text.setWordWrap(True)
        
        layout.addWidget(info_text)
        
        # Pulsante OK
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout) 
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, 
    QSpinBox, QDialogButtonBox, QHBoxLayout, QFileDialog
)
import os

class GeneraCartelleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Genera Cartelle")
        self.logo_path = None  # Per memorizzare il percorso del logo
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Selezione logo
        logo_layout = QHBoxLayout()
        self.logo_label = QLabel("Nessun logo selezionato")
        self.logo_button = QPushButton("Seleziona Logo")
        self.logo_button.clicked.connect(self.seleziona_logo)
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.logo_button)
        layout.addLayout(logo_layout)

        # Numero di cartelle per foglio
        self.spin_cartelle = QSpinBox()
        self.spin_cartelle.setRange(1, 6)
        self.spin_cartelle.setValue(1)
        layout.addWidget(QLabel("Cartelle per foglio:"))
        layout.addWidget(self.spin_cartelle)

        # Numero totale di fogli
        self.spin_fogli = QSpinBox()
        self.spin_fogli.setRange(1, 100)
        self.spin_fogli.setValue(1)
        layout.addWidget(QLabel("Numero di fogli:"))
        layout.addWidget(self.spin_fogli)

        # Pulsanti
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton[text="OK"] {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton[text="Cancel"] {
                background-color: #f44336;
                color: white;
            }
        """)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def seleziona_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona Logo",
            "",
            "Immagini (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.logo_path = file_path
            self.logo_label.setText(os.path.basename(file_path))

    def get_logo_path(self):
        return self.logo_path 
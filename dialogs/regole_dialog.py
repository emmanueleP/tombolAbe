from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget
from PyQt5.QtCore import Qt

class RegoleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Come si gioca")
        self.setMinimumSize(1000, 800)  # Dimensione più ragionevole
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Crea un QScrollArea per gestire il contenuto scrollabile
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Widget contenitore per il testo
        content = QWidget()
        content.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        
        regole_text = QLabel("""
            <div style="max-width: 900px; margin: 0 auto; line-height: 1.6;">
                <h2 style="text-align: center; font-size: 32px; margin-bottom: 30px;">Regole Tombola</h2>
                
                <h3 style="font-size: 24px; color: #2c3e50; margin-top: 30px;">Materiale di gioco</h3>
                <ul style="font-size: 18px; margin-left: 20px;">
                    <li style="margin-bottom: 10px;">90 numeri (da 1 a 90)</li>
                    <li style="margin-bottom: 10px;">Cartelle con 15 numeri ciascuna</li>
                </ul>
                
                <h3 style="font-size: 24px; color: #2c3e50; margin-top: 30px;">Le Cartelle</h3>
                <p style="font-size: 18px;">Ogni cartella contiene:</p>
                <ul style="font-size: 18px; margin-left: 20px;">
                    <li style="margin-bottom: 10px;">3 righe</li>
                    <li style="margin-bottom: 10px;">9 colonne</li>
                    <li style="margin-bottom: 10px;">15 numeri in totale (5 numeri per riga)</li>
                </ul>
                
                <h3 style="font-size: 24px; color: #2c3e50; margin-top: 30px;">Distribuzione dei numeri</h3>
                <p style="font-size: 18px;">I numeri sono distribuiti nelle colonne secondo questo schema:</p>
                <ul style="font-size: 18px; margin-left: 20px;">
                    <li style="margin-bottom: 10px;">Prima colonna: numeri da 1 a 9</li>
                    <li style="margin-bottom: 10px;">Seconda colonna: numeri da 10 a 19</li>
                    <li style="margin-bottom: 10px;">Terza colonna: numeri da 20 a 29</li>
                    <li style="margin-bottom: 10px;">Quarta colonna: numeri da 30 a 39</li>
                    <li style="margin-bottom: 10px;">Quinta colonna: numeri da 40 a 49</li>
                    <li style="margin-bottom: 10px;">Sesta colonna: numeri da 50 a 59</li>
                    <li style="margin-bottom: 10px;">Settima colonna: numeri da 60 a 69</li>
                    <li style="margin-bottom: 10px;">Ottava colonna: numeri da 70 a 79</li>
                    <li style="margin-bottom: 10px;">Nona colonna: numeri da 80 a 90</li>
                </ul>
                
                <h3 style="font-size: 24px; color: #2c3e50; margin-top: 30px;">Vincite</h3>
                <p style="font-size: 18px;">Durante il gioco si possono realizzare diverse combinazioni vincenti:</p>
                <ul style="font-size: 18px; margin-left: 20px;">
                    <li style="margin-bottom: 10px;"><b>Ambo</b>: due numeri sulla stessa riga</li>
                    <li style="margin-bottom: 10px;"><b>Terno</b>: tre numeri sulla stessa riga</li>
                    <li style="margin-bottom: 10px;"><b>Quaterna</b>: quattro numeri sulla stessa riga</li>
                    <li style="margin-bottom: 10px;"><b>Cinquina</b>: tutti e cinque i numeri di una riga</li>
                    <li style="margin-bottom: 10px;"><b>Tombola</b>: tutti i 15 numeri della cartella</li>
                </ul>
                
                <h3 style="font-size: 24px; color: #2c3e50; margin-top: 30px;">Come si gioca</h3>
                <ol style="font-size: 18px; margin-left: 20px;">
                    <li style="margin-bottom: 10px;">I giocatori acquistano una o più cartelle</li>
                    <li style="margin-bottom: 10px;">Il banco estrae un numero alla volta</li>
                    <li style="margin-bottom: 10px;">I giocatori controllano se il numero estratto è presente nelle loro cartelle</li>
                    <li style="margin-bottom: 10px;">Se presente, il numero viene segnato sulla cartella</li>
                    <li style="margin-bottom: 10px;">Quando un giocatore realizza una combinazione vincente, deve dichiararlo</li>
                    <li style="margin-bottom: 10px;">Il gioco continua fino alla tombola</li>
                </ol>
                
                <h3 style="font-size: 24px; color: #2c3e50; margin-top: 30px;">Utilizzo dell'applicazione</h3>
                <ul style="font-size: 18px; margin-left: 20px;">
                    <li style="margin-bottom: 10px;">Usa il menu "Partita > Estrai Numero" o premi Ctrl+W per estrarre un numero</li>
                    <li style="margin-bottom: 10px;">Puoi anche cliccare direttamente sui numeri per selezionarli</li>
                    <li style="margin-bottom: 10px;">Usa il tasto destro del mouse per deselezionare un numero</li>
                    <li style="margin-bottom: 10px;">Usa Ctrl+Z per annullare l'ultima azione</li>
                    <li style="margin-bottom: 10px;">Usa il menu "Partita > Nuova Partita" o premi Ctrl+N per iniziare una nuova partita</li>
                    <li style="margin-bottom: 10px;">Puoi generare cartelle dal menu "File > Genera Cartelle"</li>
                </ul>
            </div>
        """)
        regole_text.setTextFormat(Qt.RichText)
        regole_text.setWordWrap(True)
        content_layout.addWidget(regole_text)
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Pulsante Chiudi
        close_button = QPushButton("Chiudi")
        close_button.setFixedSize(120, 40)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout) 
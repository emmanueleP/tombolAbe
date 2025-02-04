from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QGridLayout,
    QMenuBar, QAction, QFileDialog, QToolBar, QDialog, QHBoxLayout,
    QDesktopWidget, QScrollArea
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QKeySequence, QColor
from .core.logic import Tombola
from .dialogs.info_dialog import InfoDialog
from .dialogs.regole_dialog import RegoleDialog
from .dialogs.genera_cartelle_dialog import GeneraCartelleDialog
from .dialogs.cronologia_dialog import CronologiaDialog
from .database import TombolaDB
from .animations import anima_numero
from .core.cartelle_pdf_manager import CartellePDFManager
import os
from datetime import datetime

class TombolaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tombola del Dono")
        
        # Ottieni le dimensioni dello schermo
        desktop = QDesktopWidget().availableGeometry()
        self.setGeometry(0, 0, desktop.width(), desktop.height())

        # Inizializza logica della tombola
        self.tombola = Tombola()

        # Crea la toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Aggiungi menu
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        file_menu = self.menu_bar.addMenu("File")

        # Aggiungi l'azione per generare cartelle
        genera_action = QAction("Genera Cartelle", self)
        genera_action.triggered.connect(self.mostra_dialogo_cartelle)
        file_menu.addAction(genera_action)

        # Aggiungi menu Strumenti
        strumenti_menu = self.menu_bar.addMenu("Strumenti")
        cronologia_action = QAction("Cronologia", self)
        cronologia_action.triggered.connect(self.mostra_cronologia)
        strumenti_menu.addAction(cronologia_action)

        # Aggiungi menu Partita
        partita_menu = self.menu_bar.addMenu("Partita")
        
        # Azione Nuova Partita
        nuova_partita_action = QAction("Nuova Partita", self)
        nuova_partita_action.setShortcut(QKeySequence("Ctrl+N"))
        nuova_partita_action.triggered.connect(self.reset_partita)
        partita_menu.addAction(nuova_partita_action)
        
        # Azione Estrai Numero
        estrai_action = QAction("Estrai Numero", self)
        estrai_action.setShortcut(QKeySequence("Ctrl+W"))
        estrai_action.triggered.connect(self.estrai_numero)
        partita_menu.addAction(estrai_action)
        
        # Azione Annulla
        annulla_action = QAction("Annulla", self)
        annulla_action.setShortcut(QKeySequence.Undo)
        annulla_action.triggered.connect(self.annulla_ultima_azione)
        partita_menu.addAction(annulla_action)

        # Aggiungi l'azione per lo schermo intero nel menu File
        schermo_intero_action = QAction("Schermo Intero", self)
        schermo_intero_action.setShortcut(QKeySequence("Ctrl+T"))
        schermo_intero_action.triggered.connect(self.toggle_schermo_intero)
        file_menu.addAction(schermo_intero_action)

        # Aggiungi menu Aiuto
        aiuto_menu = self.menu_bar.addMenu("Aiuto")
        
        info_action = QAction("Info", self)
        info_action.triggered.connect(self.mostra_info)
        aiuto_menu.addAction(info_action)
        
        regole_action = QAction("Come si gioca", self)
        regole_action.triggered.connect(self.mostra_regole)
        aiuto_menu.addAction(regole_action)

        # Flag per tenere traccia dello stato schermo intero
        self.is_fullscreen = False

        # Configura interfaccia
        self.setup_ui()

        # Aggiungi questa proprietà
        self.numeri_estratti = []

        # Inizializza database
        self.db = TombolaDB()
        self.partita_corrente = None
        self.ordine_estrazione = 0
        self.ultimo_numero_estratto = None  # Per tenere traccia dell'ultimo numero estratto

        # Lista per tenere traccia delle azioni per l'annullamento
        self.azioni = []

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principale con margini proporzionali
        self.layout = QVBoxLayout(self.central_widget)
        margin = int(self.width() * 0.02)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(margin)

        # Numero estratto con dimensioni proporzionali
        self.numero_estratto_label = QLabel("--", self)
        self.numero_estratto_label.setAlignment(Qt.AlignCenter)
        self.numero_estratto_label.setStyleSheet("""
            font-size: 180px;
            color: red;
            font-weight: bold;
            margin: 30px;
            min-height: 200px;
        """)
        self.layout.addWidget(self.numero_estratto_label)

        # Container per la griglia dei numeri
        grid_container = QWidget()
        grid_container.setObjectName("grid_container")
        self.numeri_layout = QGridLayout(grid_container)
        
        # Calcola dimensioni ottimali in modo dinamico
        def calculate_sizes(self):
            available_width = self.width() - (margin * 4)
            available_height = self.height() - self.numero_estratto_label.height() - (margin * 4)
            
            # Calcola dimensioni ottimali per una griglia 9x10
            button_size = min(
                available_width // 15,  # 15 colonne
                available_height // 6,  # 6 righe
                90  # Dimensione massima
            )
            
            spacing = max(button_size // 8, 4)
            
            return button_size, spacing

        button_size, spacing = calculate_sizes(self)

        # Configura il layout della griglia
        self.numeri_layout.setSpacing(spacing)
        self.numeri_layout.setContentsMargins(spacing * 2, spacing * 2, spacing * 2, spacing * 2)

        # Inizializza griglia numeri in una disposizione 15x6
        self.numeri_label = {}
        for i in range(1, 91):
            btn = QPushButton(str(i))
            btn.setFixedSize(button_size, button_size)
            font_size = int(button_size * 0.4)
            btn.setFont(QFont('Arial', font_size))
            btn.clicked.connect(lambda checked, num=i: self.numero_selezionato(num))
            btn.setContextMenuPolicy(Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, num=i: self.deseleziona_numero(num))
            
            # Calcola riga e colonna per una disposizione 15x6
            row = (i - 1) // 15  # 15 numeri per riga
            col = (i - 1) % 15   # 15 colonne
            self.numeri_layout.addWidget(btn, row, col)
            self.numeri_label[i] = btn

        # Aggiungi bottoni vuoti per completare la griglia
        for i in range(91, 91 + (15 * 6 - 90)):  # Aggiungi bottoni vuoti per completare la griglia
            btn = QPushButton("")
            btn.setFixedSize(button_size, button_size)
            btn.setEnabled(False)
            btn.setStyleSheet("background: transparent; border: none;")
            row = (i - 1) // 15
            col = (i - 1) % 15
            self.numeri_layout.addWidget(btn, row, col)

        self.layout.addWidget(grid_container, alignment=Qt.AlignCenter)
        self.calculate_sizes = calculate_sizes

    def deseleziona_numero(self, numero):
        if numero in self.numeri_estratti:
            self.numeri_estratti.remove(numero)
            self.numeri_label[numero].setStyleSheet("")
            self.aggiorna_display_estratti()
            
            # Salva l'azione di deselezione nel database
            if self.partita_corrente is None:
                self.partita_corrente = self.db.nuova_partita()
            self.ordine_estrazione += 1
            self.db.salva_estrazione(
                self.partita_corrente,
                numero,
                self.ordine_estrazione,
                "deselezionato"
            )
            
            # Aggiungi l'azione alla lista per l'annullamento
            self.azioni.append(("deseleziona", numero))

    def numero_selezionato(self, numero):
        if numero not in self.numeri_estratti:
            self.numeri_estratti.append(numero)
            self.ultimo_numero_estratto = numero
            self.numero_estratto_label.setText(str(numero))
            self.numeri_label[numero].setStyleSheet("""
                background-color: #db5e35;
                color: white;
                border-radius: 30px;
            """)
            self.aggiorna_display_estratti()
            
            if self.partita_corrente is None:
                self.partita_corrente = self.db.nuova_partita()
            self.ordine_estrazione += 1
            self.db.salva_estrazione(
                self.partita_corrente,
                numero,
                self.ordine_estrazione,
                "selezione_manuale"
            )
            
            # Aggiungi l'azione alla lista per l'annullamento
            self.azioni.append(("seleziona", numero))

    def aggiorna_display_estratti(self):
        numeri_str = " ".join(str(n) for n in self.numeri_estratti)
        if not hasattr(self, 'label_estratti'):
            self.label_estratti = QLabel(self)
            self.label_estratti.setStyleSheet("font-size: 16px;")
            self.toolbar.addWidget(self.label_estratti)
        self.label_estratti.setText(f"Numeri estratti: {numeri_str}")

    def estrai_numero(self):
        if self.partita_corrente is None:
            self.partita_corrente = self.db.nuova_partita()
            
        numero = self.tombola.estrai_numero()
        if numero is None:
            QMessageBox.information(self, "Tombola", "Tutti i numeri sono stati estratti!")
            self.db.aggiorna_stato_partita(self.partita_corrente, "completata")
            return

        self.ordine_estrazione += 1
        self.db.salva_estrazione(
            self.partita_corrente, 
            numero, 
            self.ordine_estrazione,
            "estrazione"
        )
        
        self.numero_estratto_label.setText(str(numero))
        self.numeri_label[numero].setStyleSheet("""
            background-color: #db5e35;
            color: white;
            border-radius: 30px;
        """)
        if numero not in self.numeri_estratti:
            self.numeri_estratti.append(numero)
            self.aggiorna_display_estratti()

        # Aggiungi l'azione alla lista per l'annullamento
        self.azioni.append(("estrai", numero))

    def annulla_ultima_azione(self):
        if not self.azioni:
            return
            
        ultima_azione, numero = self.azioni.pop()
        
        if ultima_azione in ["seleziona", "estrai"]:
            # Annulla selezione/estrazione
            if numero in self.numeri_estratti:
                self.numeri_estratti.remove(numero)
                self.numeri_label[numero].setStyleSheet("")
                if numero == self.ultimo_numero_estratto:
                    self.numero_estratto_label.setText("--")
                self.aggiorna_display_estratti()
                
                # Registra l'annullamento nel database
                self.ordine_estrazione += 1
                self.db.salva_estrazione(
                    self.partita_corrente,
                    numero,
                    self.ordine_estrazione,
                    "annullato"
                )
                
        elif ultima_azione == "deseleziona":
            # Ripristina la selezione
            if numero not in self.numeri_estratti:
                self.numeri_estratti.append(numero)
                self.numeri_label[numero].setStyleSheet("""
                    background-color: #db5e35;
                    color: white;
                    border-radius: 30px;
                """)
                self.aggiorna_display_estratti()
                
                # Registra il ripristino nel database
                self.ordine_estrazione += 1
                self.db.salva_estrazione(
                    self.partita_corrente,
                    numero,
                    self.ordine_estrazione,
                    "ripristinato"
                )

    def reset_partita(self):
        if self.partita_corrente is not None:
            self.db.aggiorna_stato_partita(self.partita_corrente, "annullata")
            self.ordine_estrazione += 1
            self.db.salva_estrazione(
                self.partita_corrente,
                0,
                self.ordine_estrazione,
                "reset"
            )
        
        self.tombola.resetta()
        self.numero_estratto_label.setText("--")
        self.numeri_estratti = []
        self.partita_corrente = None
        self.ordine_estrazione = 0
        self.azioni = []  # Pulisci la lista delle azioni
        if hasattr(self, 'label_estratti'):
            self.label_estratti.setText("Numeri estratti: ")
        for i in range(1, 91):
            self.numeri_label[i].setStyleSheet("")

    def mostra_dialogo_cartelle(self):
        self.dialog = GeneraCartelleDialog(self)  # Salva il riferimento al dialogo
        if self.dialog.exec_() == QDialog.Accepted:
            num_cartelle = self.dialog.spin_cartelle.value()
            num_fogli = self.dialog.spin_fogli.value()
            self.genera_cartelle(num_cartelle, num_fogli)

    def genera_cartelle(self, cartelle_per_foglio, num_fogli):
        save_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Salva Cartelle", 
            "", 
            "PDF Files (*.pdf)"
        )
        if save_path:
            try:
                logo_path = self.dialog.get_logo_path()
                CartellePDFManager.genera_pdf(
                    save_path, 
                    cartelle_per_foglio * num_fogli,
                    logo_path
                )
                QMessageBox.information(
                    self, 
                    "Tombola", 
                    f"Cartelle create e salvate in:\n{save_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Errore", 
                    f"Errore durante la generazione delle cartelle:\n{str(e)}"
                )

    def mostra_cronologia(self):
        dialog = CronologiaDialog(self)
        dialog.exec_()

    def toggle_schermo_intero(self):
        if self.is_fullscreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self.is_fullscreen = not self.is_fullscreen

    def keyPressEvent(self, event):
        # Gestisci il tasto Esc per uscire dalla modalità schermo intero
        if event.key() == Qt.Key_Escape and self.is_fullscreen:
            self.toggle_schermo_intero()
        super().keyPressEvent(event)

    def mostra_info(self):
        info_dialog = InfoDialog(self)
        info_dialog.exec_()

    def mostra_regole(self):
        regole_dialog = RegoleDialog(self)
        regole_dialog.exec_()

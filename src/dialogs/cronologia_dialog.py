from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QColor
from datetime import datetime

class CronologiaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cronologia Partite")
        self.setMinimumSize(1000, 600)
        
        layout = QVBoxLayout()
        
        # Lista partite
        self.lista_partite = QTreeWidget()
        self.lista_partite.setHeaderLabels([
            "Data/Ora",
            "Stato",
            "Numeri Estratti",
            "Statistiche",
            "Primo/Ultimo"
        ])
        self.lista_partite.setAlternatingRowColors(True)
        
        # Imposta le larghezze delle colonne
        self.lista_partite.setColumnWidth(0, 150)  # Data/Ora
        self.lista_partite.setColumnWidth(1, 100)  # Stato
        self.lista_partite.setColumnWidth(2, 400)  # Numeri
        self.lista_partite.setColumnWidth(3, 200)  # Statistiche
        self.lista_partite.setColumnWidth(4, 100)  # Primo/Ultimo
        
        layout.addWidget(self.lista_partite)
        
        # Legenda
        legenda = QLabel(
            "Legenda: E = Estrazione automatica, M = Selezione manuale, "
            "D = Deselezione, A = Annullamento, R = Reset"
        )
        legenda.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(legenda)
        
        self.setLayout(layout)
        self.carica_cronologia()
    
    def carica_cronologia(self):
        cronologia = self.parent().db.get_cronologia()
        for partita in cronologia:
            item = QTreeWidgetItem()
            
            # Data e ora
            data_ora = datetime.strptime(partita[1], "%Y-%m-%d %H:%M:%S")
            item.setText(0, data_ora.strftime("%d/%m/%Y %H:%M"))
            
            # Stato
            stato = partita[2]
            item.setText(1, stato.replace('_', ' ').title())
            
            # Eventi
            eventi = partita[3] if partita[3] else ""
            item.setText(2, eventi)
            
            # Statistiche
            stats = (
                f"Estrazioni: {partita[4]}, "
                f"Manuali: {partita[5]}, "
                f"Deselezioni: {partita[6]}, "
                f"Annullamenti: {partita[7]}"
            )
            item.setText(3, stats)
            
            # Primo/Ultimo numero
            primo = partita[8] if partita[8] is not None else "-"
            ultimo = partita[9] if partita[9] is not None else "-"
            item.setText(4, f"{primo} → {ultimo}")
            
            # Colore in base allo stato
            if stato == 'in_corso':
                item.setBackground(1, QColor('#fff3cd'))
            elif stato == 'completata':
                item.setBackground(1, QColor('#d4edda'))
            elif stato == 'annullata':
                item.setBackground(1, QColor('#f8d7da'))
            
            self.lista_partite.addTopLevelItem(item) 
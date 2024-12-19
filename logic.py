import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os

class Tombola:
    def __init__(self):
        self.numeri_disponibili = list(range(1, 91))
        self.numeri_estratti = []

    def estrai_numero(self):
        if not self.numeri_disponibili:
            return None
        numero = random.choice(self.numeri_disponibili)
        self.numeri_disponibili.remove(numero)
        self.numeri_estratti.append(numero)
        return numero

    def resetta(self):
        self.numeri_disponibili = list(range(1, 91))
        self.numeri_estratti = []


def genera_cartella():
    """
    Genera una cartella della tombola rispettando le regole:
    - 3 righe, 9 colonne
    - 5 numeri per riga
    - Numeri ordinati per colonna secondo le regole specificate
    """
    cartella = [[0] * 9 for _ in range(3)]
    numeri_usati = set()
    
    # Range per ogni colonna
    ranges_colonne = [
        range(1, 10),     # Prima colonna: 1-9
        range(10, 20),    # Seconda colonna: 10-19
        range(20, 30),    # Terza colonna: 20-29
        range(30, 40),    # ecc.
        range(40, 50),
        range(50, 60),
        range(60, 70),
        range(70, 80),
        range(80, 91)     # Ultima colonna: 80-90
    ]
    
    # Assegna 5 numeri per ogni riga
    for riga in range(3):
        # Seleziona 5 colonne casuali diverse per questa riga
        colonne_disponibili = list(range(9))
        colonne_selezionate = random.sample(colonne_disponibili, 5)
        
        for colonna in colonne_selezionate:
            # Prendi i numeri disponibili per questa colonna
            numeri_disponibili = [n for n in ranges_colonne[colonna] 
                                if n not in numeri_usati]
            if numeri_disponibili:
                numero = random.choice(numeri_disponibili)
                cartella[riga][colonna] = numero
                numeri_usati.add(numero)
    
    # Ordina i numeri all'interno di ogni colonna
    for col in range(9):
        numeri_colonna = [cartella[row][col] for row in range(3) if cartella[row][col] != 0]
        numeri_colonna.sort()
        
        idx = 0
        for row in range(3):
            if cartella[row][col] != 0:
                cartella[row][col] = numeri_colonna[idx]
                idx += 1
    
    return cartella

def genera_foglio(num_cartelle):
    """
    Genera un foglio con il numero specificato di cartelle,
    assicurandosi che siano tutte diverse tra loro.
    """
    cartelle = []
    tentativi = 0
    max_tentativi = 1000  # Per evitare loop infiniti
    
    while len(cartelle) < num_cartelle and tentativi < max_tentativi:
        nuova_cartella = genera_cartella()
        # Verifica che la cartella sia unica
        if not any(cartella_uguale(nuova_cartella, c) for c in cartelle):
            cartelle.append(nuova_cartella)
        tentativi += 1
    
    if len(cartelle) < num_cartelle:
        raise ValueError(f"Impossibile generare {num_cartelle} cartelle uniche")
    
    return cartelle

def cartella_uguale(c1, c2):
    """Verifica se due cartelle sono uguali"""
    return all(c1[i][j] == c2[i][j] for i in range(3) for j in range(9))

def genera_cartelle_pdf(save_path, numero_cartelle=6, logo_path=None):
    """Genera un file PDF con le cartelle della tombola."""
    c = canvas.Canvas(save_path, pagesize=A4)
    width, height = A4
    margine_x, margine_y = 50, 50
    spazio_cartelle = 150
    font_size = 12

    # Funzione per aggiungere il logo in ogni pagina
    def aggiungi_logo():
        if logo_path and os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                # Ridimensiona il logo mantenendo l'aspect ratio
                max_logo_width = width - 2 * margine_x
                max_logo_height = 100  # Altezza massima del logo
                img_width, img_height = img.size
                ratio = min(max_logo_width/img_width, max_logo_height/img_height)
                new_width = img_width * ratio
                new_height = img_height * ratio
                
                # Posiziona il logo in alto al centro
                x = (width - new_width) / 2
                y = height - margine_y - new_height
                
                c.drawImage(logo_path, x, y, new_width, new_height)
                return new_height + 20  # Ritorna lo spazio occupato dal logo
            except Exception as e:
                print(f"Errore nel caricamento del logo: {e}")
                return 0
        return 0

    cartelle = genera_foglio(numero_cartelle)
    cartelle_per_pagina = 2
    pagina_corrente = 0

    for i, cartella in enumerate(cartelle):
        if i % cartelle_per_pagina == 0:
            if i > 0:
                c.showPage()
            c.setFont("Helvetica", font_size)
            logo_height = aggiungi_logo()
            pagina_corrente = 0

        y_start = height - margine_y - logo_height - (pagina_corrente * spazio_cartelle)
        
        # Disegna la cartella
        for riga_idx, riga in enumerate(cartella):
            for col_idx, numero in enumerate(riga):
                x = margine_x + col_idx * 30
                y = y_start - riga_idx * 20
                c.rect(x, y, 30, 20)
                if numero != 0:
                    c.drawString(x + 5, y + 5, str(numero))

        pagina_corrente += 1

    c.save()

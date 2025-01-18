from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os
from .cartelle_logic import genera_cartella

class CartellePDFManager:
    @staticmethod
    def genera_pdf(save_path, numero_cartelle=6, logo_path=None):
        """Genera un file PDF con le cartelle della tombola."""
        c = canvas.Canvas(save_path, pagesize=A4)
        width, height = A4
        margine_x, margine_y = 50, 50
        spazio_cartelle = 150
        font_size = 12

        def aggiungi_logo():
            if logo_path and os.path.exists(logo_path):
                try:
                    img = Image.open(logo_path)
                    max_logo_width = width - 2 * margine_x
                    max_logo_height = 100
                    img_width, img_height = img.size
                    ratio = min(max_logo_width/img_width, max_logo_height/img_height)
                    new_width = img_width * ratio
                    new_height = img_height * ratio
                    
                    x = (width - new_width) / 2
                    y = height - margine_y - new_height
                    
                    c.drawImage(logo_path, x, y, new_width, new_height)
                    return new_height + 20
                except Exception as e:
                    print(f"Errore nel caricamento del logo: {e}")
                    return 0
            return 0

        cartelle_per_pagina = 2
        pagina_corrente = 0

        for i in range(numero_cartelle):
            if i % cartelle_per_pagina == 0:
                if i > 0:
                    c.showPage()
                c.setFont("Helvetica", font_size)
                logo_height = aggiungi_logo()
                pagina_corrente = 0

            cartella = genera_cartella()
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
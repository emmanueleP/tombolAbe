import random
from .cartelle_logic import genera_cartella, genera_cartelle_pdf

__all__ = ['Tombola', 'genera_cartella', 'genera_cartelle_pdf']

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

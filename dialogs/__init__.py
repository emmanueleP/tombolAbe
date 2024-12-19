# Questo file rende la cartella dialogs un package Python
# Può rimanere vuoto o contenere codice di inizializzazione del package

from .info_dialog import InfoDialog
from .regole_dialog import RegoleDialog

__all__ = ['InfoDialog', 'RegoleDialog'] 
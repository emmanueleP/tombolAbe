# Questo file rende la cartella dialogs un package Python
# Può rimanere vuoto o contenere codice di inizializzazione del package

from .info_dialog import InfoDialog
from .regole_dialog import RegoleDialog
from .genera_cartelle_dialog import GeneraCartelleDialog
from .cronologia_dialog import CronologiaDialog

__all__ = ['InfoDialog', 'RegoleDialog', 'GeneraCartelleDialog', 'CronologiaDialog'] 
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush

class NumeroAnimato(QLabel):
    def __init__(self, numero, parent=None):
        super().__init__(str(numero), parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                font-size: 48px;
                color: black;
                background: transparent;
            }
        """)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Disegna il cerchio
        pen = QPen(QColor("black"), 2)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor("white")))
        painter.drawEllipse(self.rect().adjusted(2, 2, -2, -2))
        
        # Disegna il numero
        super().paintEvent(event)

def anima_numero(numero, parent_widget):
    # Crea il label animato
    label = NumeroAnimato(numero, parent_widget)
    
    # Dimensione iniziale e finale
    size_start = 60
    size_end = 120
    
    # Posizione centrale del widget parent
    center_x = parent_widget.width() // 2 - size_end // 2
    center_y = parent_widget.height() // 2 - size_end // 2
    
    # Configura l'animazione della geometria
    anim = QPropertyAnimation(label, b"geometry")
    anim.setDuration(1000)  # 1 secondo
    anim.setStartValue(QRect(center_x + size_end//4, center_y + size_end//4, 
                            size_start, size_start))
    anim.setEndValue(QRect(center_x, center_y, size_end, size_end))
    
    # Aggiungi un effetto di easing per rendere l'animazione più fluida
    anim.setEasingCurve(QEasingCurve.OutBack)
    
    # Mostra il label e avvia l'animazione
    label.show()
    anim.start()
    
    # Connetti il segnale finished per rimuovere il label
    anim.finished.connect(lambda: label.deleteLater())
    
    return anim 
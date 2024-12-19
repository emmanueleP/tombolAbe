import sqlite3
import os
from datetime import datetime
import platform

class TombolaDB:
    def __init__(self):
        # Determina il percorso della directory Documenti
        if platform.system() == "Windows":
            docs_path = os.path.join(os.path.expanduser("~"), "Documents")
        else:
            docs_path = os.path.join(os.path.expanduser("~"), "Documenti")
        
        # Crea la directory tombolA se non esiste
        self.tombola_dir = os.path.join(docs_path, "tombolA")
        os.makedirs(self.tombola_dir, exist_ok=True)
        
        # Crea un nuovo file database per ogni giorno
        today = datetime.now().strftime("%Y%m%d")
        counter = 1
        while True:
            self.db_path = os.path.join(self.tombola_dir, f"cronologia_tombola_n_{counter}_{today}.db")
            if not os.path.exists(self.db_path):
                break
            counter += 1
        
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS partite (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_ora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    stato TEXT DEFAULT 'in_corso'  -- in_corso, completata, annullata
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estrazioni (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partita_id INTEGER,
                    numero INTEGER,
                    ordine INTEGER,
                    tipo_evento TEXT,  -- estrazione, selezione_manuale, deselezione, annullamento, reset
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (partita_id) REFERENCES partite(id)
                )
            ''')
            conn.commit()
    
    def nuova_partita(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO partite DEFAULT VALUES')
            return cursor.lastrowid
    
    def salva_estrazione(self, partita_id, numero, ordine, tipo_evento):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO estrazioni (partita_id, numero, ordine, tipo_evento)
                VALUES (?, ?, ?, ?)
            ''', (partita_id, numero, ordine, tipo_evento))
            conn.commit()
    
    def aggiorna_stato_partita(self, partita_id, stato):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE partite
                SET stato = ?
                WHERE id = ?
            ''', (stato, partita_id))
            conn.commit()
    
    def get_cronologia(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    p.id,
                    p.data_ora,
                    p.stato,
                    GROUP_CONCAT(
                        e.numero || ' (' || 
                        CASE e.tipo_evento
                            WHEN 'estrazione' THEN 'E'
                            WHEN 'selezione_manuale' THEN 'M'
                            WHEN 'deselezione' THEN 'D'
                            WHEN 'annullamento' THEN 'A'
                            WHEN 'reset' THEN 'R'
                        END || ')',
                        ', '
                    ) as eventi,
                    COUNT(CASE WHEN e.tipo_evento = 'estrazione' THEN 1 END) as num_estrazioni,
                    COUNT(CASE WHEN e.tipo_evento = 'selezione_manuale' THEN 1 END) as num_manuali,
                    COUNT(CASE WHEN e.tipo_evento = 'deselezione' THEN 1 END) as num_deselezioni,
                    COUNT(CASE WHEN e.tipo_evento = 'annullamento' THEN 1 END) as num_annullamenti,
                    MIN(CASE WHEN e.tipo_evento IN ('estrazione', 'selezione_manuale') THEN e.numero END) as primo_numero,
                    MAX(CASE WHEN e.tipo_evento IN ('estrazione', 'selezione_manuale') THEN e.numero END) as ultimo_numero
                FROM partite p
                LEFT JOIN estrazioni e ON p.id = e.partita_id
                GROUP BY p.id
                ORDER BY p.data_ora DESC
            ''')
            return cursor.fetchall() 
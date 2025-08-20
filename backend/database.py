import sqlite3
import os

DB_PATH = 'teleinfo.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Crear tabla de guías si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS guides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            filename TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_guides():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM guides ORDER BY category, name')
    guides = [dict(row) for row in c.fetchall()]
    
    conn.close()
    return guides

def get_guide(guide_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM guides WHERE id = ?', (guide_id,))
    guide = c.fetchone()
    
    conn.close()
    return dict(guide) if guide else None

def add_guide(name, category, filename):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('INSERT INTO guides (name, category, filename) VALUES (?, ?, ?)',
              (name, category, filename))
    guide_id = c.lastrowid
    
    conn.commit()
    conn.close()
    return guide_id

def delete_guide(guide_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('DELETE FROM guides WHERE id = ?', (guide_id,))
    
    conn.commit()
    conn.close()
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash  # Añade check_password_hash

def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

def crear_base_de_datos():
    conn = get_db_connection()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                telefono TEXT,
                email TEXT NOT NULL UNIQUE,
                rol TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Verificar si ya existe el usuario admin
        cursor = conn.execute('SELECT id FROM usuarios WHERE email = "admin@odontosmile.com"')
        if not cursor.fetchone():
            hashed_pw = generate_password_hash('admin123')
            conn.execute('''
                INSERT INTO usuarios (nombres, apellidos, telefono, email, rol, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('Admin', 'OdontoSmile', '123456789', 'admin@odontosmile.com', 'admin', hashed_pw))
        
        conn.commit()
    finally:
        conn.close()

def agregar_usuario(nombres, apellidos, telefono, email, rol, password):
    conn = get_db_connection()
    try:
        hashed_pw = generate_password_hash(password)  # Hashea la contraseña antes de guardarla
        conn.execute('''
            INSERT INTO usuarios (nombres, apellidos, telefono, email, rol, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombres, apellidos, telefono, email, rol, hashed_pw))
        conn.commit()
    finally:
        conn.close()

def validar_usuario(email, password):
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            return user  # Devuelve el usuario completo, no solo True
        return None
    finally:
        conn.close()
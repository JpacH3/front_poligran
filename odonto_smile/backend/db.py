import sqlite3

def crear_base_de_datos():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''
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
    conn.commit()
    conn.close()

def agregar_usuario(nombres, apellidos, telefono, email, rol, password):
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO usuarios (nombres, apellidos, telefono, email, rol, password)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombres, apellidos, telefono, email, rol, password))
    conn.commit()
    conn.close()

def validar_usuario(email, password):
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE email = ? AND password = ?', (email, password))
    user = c.fetchone()
    conn.close()
    return user is not None

#crear_base_de_datos()
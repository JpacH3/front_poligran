import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_path():
    """Obtiene la ruta absoluta y garantiza que el directorio exista"""
    # Ruta absoluta al directorio del archivo db.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(base_dir, 'database')  # Subdirectorio para la BD
    os.makedirs(db_dir, exist_ok=True)  # Crea el directorio si no existe
    return os.path.join(db_dir, 'usuarios.db')

def get_db_connection():
    """Establece conexión a la base de datos con verificación de errores"""
    db_path = get_db_path()
    print(f"🔌 Conectando a base de datos en: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        # Activar claves foráneas
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error de conexión SQLite: {str(e)}")
        raise

def crear_base_de_datos():
    """Crea la estructura inicial de la base de datos"""
    db_path = get_db_path()
    print(f"\n🛠️ Creando base de datos en: {db_path}")
    
    # Verificar si el archivo ya existe
    if os.path.exists(db_path):
        print(f"⚠️ Archivo de base de datos ya existe en: {db_path}")
        print(f"📏 Tamaño actual: {os.path.getsize(db_path)} bytes")
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas_existentes = [t[0] for t in cursor.fetchall()]
        print(f"📊 Tablas existentes: {tablas_existentes or 'Ninguna'}")
        
        # Crear tabla usuarios si no existe
        if 'usuarios' not in tablas_existentes:
            cursor.execute('''
                CREATE TABLE usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    telefono TEXT,
                    email TEXT NOT NULL UNIQUE,
                    rol TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            print("✅ Tabla 'usuarios' creada exitosamente")
        
        # Crear tabla citas si no existe
        if 'citas' not in tablas_existentes:
            cursor.execute('''
                CREATE TABLE citas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    tratamiento TEXT NOT NULL,
                    sede TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    tipo_paciente TEXT NOT NULL,
                    edad INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES usuarios (id)
                )
            ''')
            print("✅ Tabla 'citas' creada exitosamente")
        
        # Insertar usuario admin si no existe
        cursor.execute('SELECT id FROM usuarios WHERE email = "admin@odontosmile.com"')
        if not cursor.fetchone():
            hashed_pw = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO usuarios (nombres, apellidos, telefono, email, rol, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('Admin', 'OdontoSmile', '123456789', 'admin@odontosmile.com', 'admin', hashed_pw))
            print("👨‍⚕️ Usuario administrador creado")
        
        conn.commit()
        print(f"🏁 Base de datos inicializada correctamente en: {db_path}")
        print(f"📏 Tamaño final: {os.path.getsize(db_path)} bytes")
        
    except sqlite3.Error as e:
        print(f"❌ Error crítico en SQL: {str(e)}")
        # Forzar eliminación del archivo corrupto si es necesario
        if conn is None and os.path.exists(db_path):
            print("⚠️ Eliminando archivo corrupto...")
            os.remove(db_path)
        raise
    finally:
        if conn:
            conn.close()

def agregar_usuario(nombres, apellidos, telefono, email, rol, password):
    """Agrega un nuevo usuario a la base de datos"""
    conn = None
    try:
        conn = get_db_connection()
        hashed_pw = generate_password_hash(password)
        conn.execute('''
            INSERT INTO usuarios (nombres, apellidos, telefono, email, rol, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombres, apellidos, telefono, email, rol, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("El correo electrónico ya está registrado")
    except sqlite3.Error as e:
        print(f"Error al agregar usuario: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def validar_usuario(email, password):
    """Valida las credenciales del usuario"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            return dict(user)  # Convertir a dict para mejor manejo
        return None
    except sqlite3.Error as e:
        print(f"Error al validar usuario: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

# Verificación al importar el módulo
if __name__ == '__main__':
    print("🔍 Ejecutando verificación independiente de la base de datos...")
    crear_base_de_datos()
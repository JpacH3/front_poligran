from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'odonto'  # Puedes cambiarla por seguridad

# Conexión a la base de datos
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'usuarios.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Rutas
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get['usuario']
        password = request.form.get['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ? AND password = ?', (usuario, password)).fetchone()
        conn.close()

        if user:
            return redirect(url_for('appointment'))
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombres = request.form.get('nombres')
            apellidos = request.form.get('apellidos')
            telefono = request.form.get('telefono')
            email = request.form.get('email')
            rol = request.form.get('rol')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm-password')
            age_verification = request.form.get('age-verification')

            # Validaciones
            if not all([nombres, apellidos, email, rol, password, confirm_password]):
                flash('Todos los campos son obligatorios')
                return redirect(url_for('register'))
                
            if password != confirm_password:
                flash('Las contraseñas no coinciden')
                return redirect(url_for('register'))
                
            if len(password) < 6:
                flash('La contraseña debe tener al menos 6 caracteres')
                return redirect(url_for('register'))
                
            if not age_verification:
                flash('Debes aceptar que eres mayor de 18 años')
                return redirect(url_for('register'))

            # Conexión a la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar si el email ya existe
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
            if cursor.fetchone():
                flash('Este correo electrónico ya está registrado')
                conn.close()
                return redirect(url_for('register'))
            
            # Hash de la contraseña
            hashed_password = generate_password_hash(password)
            
            # Insertar nuevo usuario
            cursor.execute('''
                INSERT INTO usuarios (nombres, apellidos, telefono, email, rol, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombres, apellidos, telefono, email, rol, hashed_password))
            
            conn.commit()
            conn.close()
            
            flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('login'))
            
        except sqlite3.IntegrityError as e:
            flash('Error: El correo electrónico ya está registrado', 'error')
            if 'conn' in locals():
                conn.close()
            return redirect(url_for('register'))
        except Exception as e:
            flash(f'Error al registrar: {str(e)}', 'error')
            if 'conn' in locals():
                conn.close()
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

if __name__ == '__main__':
    app.run(debug=True)

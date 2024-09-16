from sqlite4 import SQLite4
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)  # Crear una instancia de la aplicación Flask
app.secret_key = 'supersecretkey'  # Necesario para manejar sesiones y CSRF
csrf = CSRFProtect(app)  # Habilitar protección CSRF

app.config.update(  # Configuración de la aplicación
    DEBUG=True,  # Es mala práctica dejar activado esto en producción.
    SECRET_KEY="supersecretkey",
)

# Inicializar el gestor de inicio de sesión
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    database.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
    user = database.fetchone()
    if user:
        return User(username=user[0], password=user[1])
    return None

# Conexión a la base de datos SQLite4
database = SQLite4("usuarios.db")
database.connect()

# Crear tabla de usuarios si no existe
database.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
''')

# Ruta principal para mostrar la página de registro/login
@app.route('/')
def index():
    return render_template('index.html')
    # Renderiza la página principal de la aplicación, que contiene los formularios de registro y login.

# Ruta para el registro
@app.route('/register', methods=['POST'])
def register():
    username = request.form['new_username']
    password = request.form['new_password']
    # Obtiene el nombre de usuario y la contraseña del formulario de registro.

    # Verificar si el usuario ya existe
    database.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
    if database.fetchone():
        flash('El usuario ya existe. Intenta con otro.')
    else:
        # Insertar el nuevo usuario en la base de datos
        database.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
        database.execute('COMMIT')
        flash('Usuario registrado exitosamente. Ahora puedes hacer login.')

    return redirect(url_for('index'))
    # Redirige al usuario a la página principal después del registro.

# Ruta para el login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Obtiene el nombre de usuario y la contraseña del formulario de inicio de sesión.

    # Verificar las credenciales del usuario
    database.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))
    user = database.fetchone()
    if user:
        user_obj = User(username=user[0], password=user[1])
        login_user(user_obj)
        flash('¡Has iniciado sesión exitosamente!')
        return redirect(url_for('dashboard'))
    else:
        flash('Usuario o contraseña incorrectos. Intenta nuevamente.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    # Ejecuta la aplicación en modo de depuración si el script se ejecuta directamente.

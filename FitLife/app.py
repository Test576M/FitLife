from sqlite4 import SQLite4
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user
from flask_wtf.csrf import CSRFProtect
import re 

app = Flask(__name__)  #1 Crear una instancia de la aplicación Flask
app.secret_key = 'supersecretkey'  #1 Necesario para manejar sesiones y CSRF
csrf = CSRFProtect(app)  #1 Habilitar protección CSRF

app.config.update(  #1 Configuración de la aplicación
    DEBUG=True,  #1 Es mala práctica dejar activado esto en producción.
    SECRET_KEY="supersecretkey",
)

#1 Inicializar el gestor de inicio de sesión
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

#1 Conexión a la base de datos SQLite4
database = SQLite4("usuarios.db")
database.connect()

#1 Crear tabla de usuarios si no existe
database.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
''')

#1 Ruta principal para mostrar la página de registro/login
@app.route('/')
def index():
    return render_template('index.html')
    #1 Renderiza la página principal de la aplicación, que contiene los formularios de registro y login.


#2 definimos las nuevas validaciones de usuario y password
def validar_username(username):
    #2 El nombre de usuario debe tener entre 5 y 18 caracteres alfanuméricos
    regex = r'^[a-zA-Z0-9]{5,18}$'
    return re.match(regex, username)

def validar_password(password):
    #2 La contraseña debe tener entre 6 y 18 caracteres, al menos una letra mayúscula, una minúscula, un número y un carácter especial
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,18}$'
    return re.match(regex, password)

#1 Ruta para el registro
@app.route('/register', methods=['POST'])
def register():
    username = request.form['new_username']
    password = request.form['new_password']
    #1 Obtiene el nombre de usuario y la contraseña del formulario de registro.

    #2 Validar el nombre de usuario
    if not validar_username(username):
        flash('El nombre de usuario debe tener entre 3 y 20 caracteres alfanuméricos.')
        return redirect(url_for('index'))
    
    #2 Validar la contraseña
    if not validar_password(password):
        flash('La contraseña debe tener entre 6 y 20 caracteres, al menos una letra mayúscula, una minúscula, un número y un carácter especial.')
        return redirect(url_for('index'))
    
    #1 Verificar si el usuario ya existe
    database.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
    if database.fetchone():
        flash('El usuario ya existe. Intenta con otro.')
    else:
        #1 Insertar el nuevo usuario en la base de datos
        database.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
        database.execute('COMMIT')
        flash('Usuario registrado exitosamente. Ahora puedes hacer login.')

    return redirect(url_for('index'))

    #1 Redirige al usuario a la página principal después del registro.

#1 Ruta para el login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    #2 Validar el nombre de usuario
    if not validar_username(username):
        flash('Nombre de usuario inválido.')
        return redirect(url_for('index'))
    
    #2 Validar la contraseña
    if not validar_password(password):
        flash('Contraseña inválida.')
        return redirect(url_for('index'))
    
    #1 Verificar las credenciales del usuario
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
    #1 Ejecuta la aplicación en modo de depuración si el script se ejecuta directamente.

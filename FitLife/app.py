from sqlite4 import SQLite4
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from datetime import timedelta, datetime
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'
csrf = CSRFProtect(app)

app.config.update(
    DEBUG=True,
    SECRET_KEY="supersecretkey",
    SESSION_TYPE='sqlalchemy',
    SESSION_SQLALCHEMY=SQLite4("sessions.db"),
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_COOKIE_HTTPONLY=True
)

Session(app)

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

database = SQLite4("usuarios.db")
database.connect()

database.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0,
    lockout_time DATETIME
)
''')

@app.route('/')
def index():
    return render_template('index.html')

def validar_username(username):
    regex = r'^[a-zA-Z0-9]{5,18}$'
    return re.match(regex, username)

def validar_password(password):
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,18}$'
    return re.match(regex, password)

def detectar_inyeccion_sql(input_string):
    patrones_inyeccion = ["'", '"', ";", "--", "/*", "*/", "xp_"]
    for patron in patrones_inyeccion:
        if patron in input_string:
            flash('Posible ataque de inyección SQL detectado.')
            return True
    return False

@app.route('/register', methods=['POST'])
def register():
    username = request.form['new_username']
    password = request.form['new_password']

    if detectar_inyeccion_sql(username) or detectar_inyeccion_sql(password):
        return redirect(url_for('index'))

    if not validar_username(username):
        flash('El nombre de usuario debe tener entre 3 y 20 caracteres alfanuméricos.')
        return redirect(url_for('index'))
    
    if not validar_password(password):
        flash('La contraseña debe tener entre 6 y 20 caracteres, al menos una letra mayúscula, una minúscula, un número y un carácter especial.')
        return redirect(url_for('index'))
    
    database.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
    if database.fetchone():
        flash('El usuario ya existe. Intenta con otro.')
    else:
        database.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (username, password))
        database.execute('COMMIT')
        flash('Usuario registrado exitosamente. Ahora puedes hacer login.')

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if detectar_inyeccion_sql(username) or detectar_inyeccion_sql(password):
        return redirect(url_for('index'))

    if not validar_username(username):
        flash('Nombre de usuario inválido.')
        return redirect(url_for('index'))
    
    if not validar_password(password):
        flash('Contraseña inválida.')
        return redirect(url_for('index'))
    
    database.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
    user = database.fetchone()
    
    if user:
        failed_attempts = user[2]
        lockout_time = user[3]
        
        if lockout_time and datetime.now() < lockout_time:
            flash('Cuenta bloqueada temporalmente. Intenta nuevamente más tarde.')
            return redirect(url_for('index'))
        
        if user[1] == password:
            user_obj = User(username=user[0], password=user[1])
            session.clear()
            login_user(user_obj)
            session.permanent = True
            database.execute('UPDATE usuarios SET failed_attempts = 0, lockout_time = NULL WHERE username = ?', (username,))
            database.execute('COMMIT')
            flash('¡Has iniciado sesión exitosamente!')
            return redirect(url_for('dashboard'))
        else:
            failed_attempts += 1
            if failed_attempts >= 5:
                lockout_time = datetime.now() + timedelta(minutes=15)
                database.execute('UPDATE usuarios SET failed_attempts = ?, lockout_time = ? WHERE username = ?', (failed_attempts, lockout_time, username))
            else:
                database.execute('UPDATE usuarios SET failed_attempts = ? WHERE username = ?', (failed_attempts, username))
            database.execute('COMMIT')
            flash('Usuario o contraseña incorrectos. Intenta nuevamente.')
    else:
        flash('Usuario o contraseña incorrectos. Intenta nuevamente.')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
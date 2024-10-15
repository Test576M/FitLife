from sqlite4 import SQLite4
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from datetime import timedelta
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
    password TEXT NOT NULL
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

@app.route('/register', methods=['POST'])
def register():
    username = request.form['new_username']
    password = request.form['new_password']

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
    
    if not validar_username(username):
        flash('Nombre de usuario inválido.')
        return redirect(url_for('index'))
    
    if not validar_password(password):
        flash('Contraseña inválida.')
        return redirect(url_for('index'))
    
    database.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))
    user = database.fetchone()
    if user:
        user_obj = User(username=user[0], password=user[1])
        session.clear() 
        login_user(user_obj)
        session.permanent = True  
        flash('¡Has iniciado sesión exitosamente!')
        return redirect(url_for('dashboard'))
    else:
        flash('Usuario o contraseña incorrectos. Intenta nuevamente.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

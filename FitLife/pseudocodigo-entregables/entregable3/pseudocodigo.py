IMPORTAR de "datetime" - "timedelta"
IMPORTAR de "flask-session" - "session"

AGREGAR en app.config.update(
    SESSION type = sqlalchemy
    SESSION_ALCHEMY = usar version SQLite4 ("session.db")
    SESSION_LIFETIME = timedelta ( 30 minutos)
    SESSION_COOKIE = solo HTTP
)

INICIALIZAR flask_session en la APP

#en ruta /login
IF user:
    session.clear() #para regenerar id de session
    session.permanent = true #para al salir de la pestaña se guarde la sesion

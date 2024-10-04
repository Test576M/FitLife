INICIAR aplicación
# Inicia la aplicación principal

CONFIGURAR clave_secreta = 'supersecretkey'
# Configura una clave secreta para la aplicación, utilizada para firmar cookies y otros datos

HABILITAR protección CSRF
# Habilita la protección contra ataques CSRF (Cross-Site Request Forgery)

CONFIGURAR aplicación:
    DEBUG = verdadero
    # Activa el modo de depuración para la aplicación, útil durante el desarrollo
    SECRET_KEY = "supersecretkey"
    # Establece la clave secreta para la aplicación

INICIAR gestor_de_login
# Inicia el gestor de inicio de sesión para manejar la autenticación de usuarios

CLASE Usuario:
    FUNCIÓN __init__(nombre_usuario, contraseña):
        ASIGNAR nombre_usuario
        # Asigna el nombre de usuario al atributo de la clase
        ASIGNAR contraseña
        # Asigna la contraseña al atributo de la clase

    FUNCIÓN obtener_id():
        RETORNAR nombre_usuario
        # Retorna el nombre de usuario como identificador único

FUNCIÓN cargar_usuario(nombre_usuario):
    EJECUTAR consulta SQL 'SELECT * FROM usuarios WHERE username = nombre_usuario'
    # Ejecuta una consulta SQL para buscar un usuario por su nombre de usuario
    SI usuario encontrado:
        RETORNAR Usuario(nombre_usuario, contraseña)
        # Si se encuentra el usuario, retorna una instancia de la clase Usuario
    SINO:
        RETORNAR nulo
        # Si no se encuentra el usuario, retorna nulo

CONECTAR a base_de_datos "usuarios.db"
# Conecta a la base de datos llamada "usuarios.db"

EJECUTAR consulta SQL '''
    CREATE TABLE IF NOT EXISTS usuarios (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
'''
# Ejecuta una consulta SQL para crear la tabla "usuarios" si no existe, con columnas para el nombre de usuario y la contraseña

RUTA '/login' MÉTODO POST
# Define una ruta para el inicio de sesión que acepta solicitudes POST

FUNCIÓN iniciar_sesión():
    OBTENER nombre_usuario de formulario
    # Obtiene el nombre de usuario del formulario de inicio de sesión
    OBTENER contraseña de formulario
    # Obtiene la contraseña del formulario de inicio de sesión

    EJECUTAR consulta SQL 'SELECT * FROM usuarios WHERE username = nombre_usuario AND password = contraseña'
    # Ejecuta una consulta SQL para verificar las credenciales del usuario
    SI usuario encontrado:
        CREAR objeto_usuario Usuario(nombre_usuario, contraseña)
        # Si se encuentra el usuario, crea un objeto de la clase Usuario
        INICIAR sesión con objeto_usuario
        # Inicia sesión con el objeto de usuario
        MOSTRAR mensaje '¡Has iniciado sesión exitosamente!'
        # Muestra un mensaje de éxito
        REDIRIGIR a 'tablero'
        # Redirige al usuario al tablero principal
    SINO:
        MOSTRAR mensaje 'Usuario o contraseña incorrectos. Intenta nuevamente.'
        # Muestra un mensaje de error si las credenciales son incorrectas
        REDIRIGIR a 'índice'
        # Redirige al usuario a la página de inicio

SI __name__ == '__main__':
    EJECUTAR aplicación en modo debug
    # Ejecuta la aplicación en modo de depuración si este archivo es el principal

Ejercicio Interactivo de Desarrollo de Software Seguro: Creando una Aplicación para "FitLife"
Contexto del Proyecto
Imagina que eres parte del equipo de desarrollo de "FitLife", una empresa ficticia que ofrece una aplicación web para ayudar a las personas a llevar un estilo de vida saludable. La aplicación permite a los usuarios registrarse, iniciar sesión, seguir sus rutinas de ejercicio y gestionar su dieta. Como parte del equipo, tu responsabilidad es asegurar que la aplicación sea segura y proteja la información sensible de los usuarios.
Objetivo del Ejercicio
El objetivo de este ejercicio es que los estudiantes aprendan a aplicar los principios de OWASP en el desarrollo de una aplicación web, utilizando pseudocódigo y código Python para implementar las mejores prácticas de seguridad.
Entregas Parciales
Entrega 1: Análisis de Riesgos y Diseño Seguro (Clase 1)
Tarea: Investigar y discutir en grupos los 10 principales riesgos de OWASP. Cada grupo seleccionará uno o dos riesgos que podrían afectar a la aplicación "FitLife".
Entregable: Un breve informe que describa los riesgos seleccionados y sus posibles impactos en la aplicación.
Pseudocódigo y Python: Crear un pseudocódigo y código Python básico de las funciones de registro e inicio de sesión, incorporando medidas de seguridad basadas en OWASP.
Ejemplo de Pseudocódigo
text
función registrarUsuario(nombre, correo, contraseña):
    validarEntrada(nombre, correo, contraseña)
    hashContraseña = hashear(contraseña)
    guardarEnBaseDeDatos(nombre, correo, hashContraseña)

función iniciarSesion(correo, contraseña):
    usuario = obtenerUsuarioPorCorreo(correo)
    si usuario existe y verificarContraseña(contraseña, usuario.hashContraseña):
        iniciarSesión(usuario)
    sino:
        mostrarError("Credenciales inválidas")

Ejemplo de Código Python
python
def registrar_usuario(nombre, correo, contraseña):
    validar_entrada(nombre, correo, contraseña)
    hash_contraseña = hashear(contraseña)
    guardar_en_base_de_datos(nombre, correo, hash_contraseña)

def iniciar_sesion(correo, contraseña):
    usuario = obtener_usuario_por_correo(correo)
    if usuario and verificar_contraseña(contraseña, usuario.hash_contraseña):
        iniciar_sesion(usuario)
    else:
        mostrar_error("Credenciales inválidas")
------------------------------------------------------------------------------------------------------------------------
Entrega 2: Validación y Sanitización (Clase 2)
Tarea: Implementar funciones de validación y sanitización de entradas de usuario.
Entregable: Código de las funciones de validación y un informe sobre la importancia de la validación de entradas.
Pseudocódigo y Python: Crear pseudocódigo y código Python para la validación de entradas.
Ejemplo de Pseudocódigo
text
función validarEntrada(nombre, correo, contraseña):
    si no esValido(nombre):
        mostrarError("Nombre inválido")
    si no esValidoCorreo(correo):
        mostrarError("Correo inválido")
    si no esValidoContraseña(contraseña):
        mostrarError("Contraseña demasiado débil")

Ejemplo de Código Python
python
def validar_entrada(nombre, correo, contraseña):
    if not es_valido(nombre):
        mostrar_error("Nombre inválido")
    if not es_valido_correo(correo):
        mostrar_error("Correo inválido")
    if not es_valido_contraseña(contraseña):
        mostrar_error("Contraseña demasiado débil")

Entrega 3: Autenticación y Manejo de Sesiones (Clase 3)
Tarea: Implementar un sistema de autenticación seguro y manejo de sesiones.
Entregable: Código de las funciones de autenticación y un informe sobre las mejores prácticas de gestión de sesiones.
Pseudocódigo y Python: Crear pseudocódigo y código Python para el manejo de sesiones.
Ejemplo de Pseudocódigo
text
función iniciarSesión(usuario):
    sesiónID = generarIDUnico()
    guardarEnMemoria(sesiónID, usuario)
    establecerCookie(sesiónID)

función verificarSesión(sesiónID):
    retornar obtenerUsuarioPorSesión(sesiónID) != nulo

Ejemplo de Código Python
python
def iniciar_sesion(usuario):
    sesion_id = generar_id_unico()
    guardar_en_memoria(sesion_id, usuario)
    establecer_cookie(sesion_id)

def verificar_sesion(sesion_id):
    return obtener_usuario_por_sesion(sesion_id) is not None

Entrega 4: Pruebas de Seguridad (Clase 4)
Tarea: Realizar pruebas de seguridad en la aplicación "FitLife" y documentar las vulnerabilidades encontradas.
Entregable: Informe de pruebas con resultados y correcciones implementadas.
Pseudocódigo y Python: Estrategias de pruebas de seguridad.
Ejemplo de Pseudocódigo
text
función pruebaInyecciónSQL():
    entradaMaliciosa = "' OR '1'='1"
    resultado = ejecutarConsulta(entradaMaliciosa)
    si resultado tiene datos:
        reportarVulnerabilidad("Posible inyección SQL")

Ejemplo de Código Python
python
def prueba_inyeccion_sql():
    entrada_maliciosa = "' OR '1'='1"
    resultado = ejecutar_consulta(entrada_maliciosa)
    if resultado:
        reportar_vulnerabilidad("Posible inyección SQL")

Entrega 5: Implementación de Medidas de Seguridad (Clase 5)
Tarea: Implementar medidas de seguridad adicionales basadas en los aprendizajes de las clases anteriores.
Entregable: Código de las medidas de seguridad implementadas y un informe sobre cómo estas medidas ayudan a mitigar los riesgos de seguridad.
Pseudocódigo y Python: Crear pseudocódigo y código Python para las medidas de seguridad adicionales.
Ejemplo de Pseudocódigo
text
función hashear(contraseña):
    sal = generarSal()
    hashContraseña = aplicarHash(contraseña + sal)
    guardarSalEnBaseDeDatos(sal)
    retornar hashContraseña

Ejemplo de Código Python
python
def hashear(contraseña):
    sal = generar_sal()
    hash_contraseña = aplicar_hash(contraseña + sal)
    guardar_sal_en_base_de_datos(sal)
    return hash_contraseña

Entrega Final: Aplicación Funcional y Segura (Clase 6)
Tarea: Entregar la aplicación "FitLife" completa, funcional y segura, implementando todas las medidas de seguridad aprendidas.
Entregable: Código Python de la aplicación "FitLife" que incluya todas las funcionalidades y prácticas de seguridad basadas en OWASP.
Evaluación
Los estudiantes serán evaluados en función de:
La calidad de sus entregables.
La aplicación de prácticas de seguridad basadas en OWASP.
La claridad y lógica del pseudocódigo y código Python.
La funcionalidad y seguridad de la aplicación final.
La colaboración y participación en las actividades grupales.
Conclusión
Este ejercicio interactivo no solo permite a los estudiantes aprender sobre OWASP y las vulnerabilidades comunes en aplicaciones web, sino que también les brinda la oportunidad de aplicar este conocimiento en un contexto práctico y colaborativo. Al trabajar en un proyecto realista como "FitLife" y utilizar tanto pseudocódigo como código Python, los estudiantes desarrollarán habilidades críticas para su futura carrera en el desarrollo de software seguro.

Requisitos:
Carátula, índice, cuerpo, conclusiones, referencias (APA)

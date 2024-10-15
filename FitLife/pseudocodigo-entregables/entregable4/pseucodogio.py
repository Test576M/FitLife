FUNCIÓN detectar_inyección_sql (string_digitado):
    patrones_más_usados = ["copiar y pegar los más usados"]
    for patron in string_digitado:
        if patron in string_digitado:
            alerta "posible injeccion"
            return True
    return false 

@ruta registro AND @ruta login
if detectar_inyeccion_sql(password o username) = True
    return redirect 

-------------------

import flask_limiter
definimos valores por defecto a 200 por día, 50 por hora
agregamos @limiter("10 por minuto") en la ruta @register y @login antes de cada Def register/login

-------------------

en @ruta login
if usuario :
    intentos fallidos = usuario(x)
    tiempo de bloqueo = usuario(z)

    if tiempo de bloqueo y hora actual < mayor que < tiempo de bloqueo
        alerta = "cuenta bloqueada temporalmente"
    
    corroborar que el login se haya dado correctamente
else:
    intentos fallido +=1
    if intento fallidos >= 5
    aumentas tiempo de bloqueo + 15 minutos
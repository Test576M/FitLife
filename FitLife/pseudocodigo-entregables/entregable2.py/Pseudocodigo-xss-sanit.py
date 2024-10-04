IMPORTAR "re"

DEFINIR validar_username(username) y validar_password (password) usando regex

MODIFICAR ruta /register con los agregados de validaciones
if not validar_username(username):
return "alerta usuario no cumple requisitos"
if not validar_password(password):
return "alerta password no cunple requisitos"

MODIFICAR ruta /login con los agregados de validacionesif not validar_username(username):
return "alerta usuario no cumple requisitos"
if not validar_password(password):
return "alerta password no cunple requisitos"


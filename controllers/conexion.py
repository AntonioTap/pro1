import pymysql

# Configuración de la base de datos
db_host = '127.0.0.1'
db_user = 'root'
db_password = ''
db_name = 'papeleria'

# Función para conectar con la base de datos
def conectar_bd():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

# Función para validar las credenciales del usuario
def validar_credenciales(correo, contraseña):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Consultar la base de datos para verificar las credenciales del usuario
    consulta = f"SELECT id_rol FROM usuario WHERE correo = %s AND contraseña = %s"
    cursor.execute(consulta, (correo, contraseña))

    # Obtener el resultado de la consulta
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    # Si se encuentra un usuario con las credenciales proporcionadas, devolver el id_rol
    return resultado

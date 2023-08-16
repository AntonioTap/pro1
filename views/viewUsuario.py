# views/viewInicio.py
from flask import render_template, request, redirect, flash
from controllers.conexion import conectar_bd

# Función para obtener la lista de usuarios desde la base de datos
def mostrar_lista_usuarios():
    # Obtener la lista de usuarios desde la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Consulta para obtener el nombre del rol en lugar del ID del rol
    consulta = "SELECT u.id_usuario, u.nombre, u.correo, r.Descripcion AS rol FROM usuario u JOIN roles r ON u.id_rol = r.id_rol"
    cursor.execute(consulta)

    usuarios_tuplas = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Convertir cada tupla en un diccionario con claves adecuadas
    usuarios = [{'id': usuario[0], 'nombre': usuario[1], 'correo': usuario[2], 'rol': usuario[3]} for usuario in usuarios_tuplas]

    return usuarios

# Función para agregar un nuevo usuario a la base de datos
def agregar_usuario():
    # Lógica para agregar un nuevo usuario a la base de datos
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        apet_pat = request.form['apet_pat']
        ape_mat = request.form['ape_mat']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        id_rol = request.form['id_rol']

        # Realizar la inserción en la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = "INSERT INTO usuario (nombre, apet_pat, ape_mat, telefono, direccion, correo, contraseña, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(consulta, (nombre, apet_pat, ape_mat, telefono, direccion, correo, contraseña, id_rol))
        conexion.commit()
        cursor.close()
        conexion.close()

        # Redirigir a la lista de usuarios después de agregar uno nuevo
        return redirect('/lista_usuarios')

    # Renderizar el formulario si el método de solicitud es GET
    return render_template('nuevo_usuario.html')

# Función para obtener la información de un usuario por su ID
def obtener_usuario_por_id(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "SELECT * FROM usuario WHERE id_usuario = %s"
    cursor.execute(consulta, (id,))
    usuario_tupla = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario_tupla:
        usuario = {
            'id_usuario': usuario_tupla[0],
            'nombre': usuario_tupla[1],
            'apet_pat': usuario_tupla[2],
            'ape_mat': usuario_tupla[3],
            'telefono': usuario_tupla[4],
            'direccion': usuario_tupla[5],
            'correo': usuario_tupla[6],
            'contraseña': usuario_tupla[7],
            'id_rol': usuario_tupla[8]
        }
        return usuario
    else:
        return None

# Función para eliminar un usuario por su ID
def eliminar_usuario(id):
    # Lógica para eliminar el usuario con el ID especificado de la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Realizar la eliminación en la base de datos
    consulta = "DELETE FROM usuario WHERE id_usuario=%s"
    cursor.execute(consulta, (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    # Redirigir a la lista de usuarios después de eliminar uno
    return redirect('/lista_usuarios')

# Función para editar un usuario por su ID
def editar_usuario(id):
    if request.method == 'POST':
        if 'confirmar' in request.form:
            # Eliminar el usuario antiguo por su ID
            eliminar_usuario(id)

            # Obtener los valores del formulario para el nuevo usuario
            nombre = request.form['nombre']
            apet_pat = request.form['apet_pat']
            ape_mat = request.form['ape_mat']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            correo = request.form['correo']
            contraseña = request.form['contraseña']
            id_rol = request.form['id_rol']

            # Insertar el nuevo usuario en la base de datos
            conexion = conectar_bd()
            cursor = conexion.cursor()
            consulta = "INSERT INTO usuario (nombre, apet_pat, ape_mat, telefono, direccion, correo, contraseña, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(consulta, (nombre, apet_pat, ape_mat, telefono, direccion, correo, contraseña, id_rol))
            conexion.commit()
            cursor.close()
            conexion.close()

            # Mostrar mensaje de éxito
            flash('Usuario actualizado exitosamente.', 'success')
            return redirect('/lista_usuarios')
        elif 'cancelar' in request.form:
            # Redirigir al usuario nuevamente a la lista de usuarios si decide cancelar la actualización
            return redirect('/lista_usuarios')
        


    # Obtener los datos del usuario por su ID y mostrarlos en el formulario para editar
    usuario = obtener_usuario_por_id(id)
    return render_template('editar_usuario.html', usuario=usuario)

def guardar_cambios_usuario(id, nombre, apet_pat, ape_mat, telefono, direccion, correo, contraseña, id_rol):
    # Obtener el usuario actual por su ID
    usuario_actual = obtener_usuario_por_id(id)

    # Eliminar el usuario actual de la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta_eliminar = "DELETE FROM usuario WHERE id_usuario = %s"
    cursor.execute(consulta_eliminar, (id,))
    conexion.commit()
    cursor.close()
    conexion.close()

    # Insertar el nuevo usuario con los datos actualizados
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta_insertar = "INSERT INTO usuario (id_usuario, nombre, apet_pat, ape_mat, telefono, direccion, correo, contraseña, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(consulta_insertar, (id, nombre, apet_pat, ape_mat, telefono, direccion, correo, contraseña, id_rol))
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return redirect('/lista_usuarios')
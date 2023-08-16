from flask import render_template, request, redirect
from controllers.conexion import conectar_bd

def mostrar_lista_marcas():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM marca"
    cursor.execute(consulta)
    marcas_tuplas = cursor.fetchall()
    cursor.close()
    conexion.close()
    marcas = [{'id': marca[0], 'nombre': marca[1], 'contacto': marca[2]} for marca in marcas_tuplas]
    return marcas

def agregar_marca():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']

        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = "INSERT INTO marca (nombre, contacto) VALUES (%s, %s)"
        cursor.execute(consulta, (nombre, contacto))
        conexion.commit()
        cursor.close()
        conexion.close()

        return redirect('/lista_marcas')

    return render_template('nueva_marca.html')

def obtener_marca_por_id(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM marca WHERE id_marca = %s"
    cursor.execute(consulta, (id,))
    marca_tupla = cursor.fetchone()
    cursor.close()
    conexion.close()

    if marca_tupla:
        marca = {
            'id': marca_tupla[0],
            'nombre': marca_tupla[1],
            'contacto': marca_tupla[2]
        }
        return marca
    else:
        return None

def eliminar_marca(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "DELETE FROM marca WHERE id_marca = %s"
    cursor.execute(consulta, (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect('/lista_marcas')

def guardar_cambios_marca(id, nombre, contacto):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "UPDATE marca SET nombre = %s, contacto = %s WHERE id_marca = %s"
    cursor.execute(consulta, (nombre, contacto, id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect('/lista_marcas')
from flask import render_template, request, redirect
from controllers.conexion import conectar_bd

def obtener_categoria_por_id(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM categoria WHERE id_categoria = %s"
    cursor.execute(consulta, (id,))
    categoria_tupla = cursor.fetchone()
    cursor.close()
    conexion.close()

    if categoria_tupla:
        categoria = {
            'id': categoria_tupla[0],
            'nombre': categoria_tupla[1],
            'descripcion': categoria_tupla[2]
        }
        return categoria
    else:
        return None

def eliminar_categoria(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "DELETE FROM categoria WHERE id_categoria = %s"
    cursor.execute(consulta, (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    # Redirigir a la lista de categorías después de eliminar una
    return redirect('/lista_categorias')

# Función para guardar los cambios en una categoría
def guardar_cambios_categoria(id, nombre, descripcion):
    # Realizar la actualización en la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "UPDATE categoria SET nombre = %s, descripcion = %s WHERE id_categoria = %s"
    cursor.execute(consulta, (nombre, descripcion, id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return True
    # Redirigir a la lista de categorías después de guardar los cambios
    #return redirect('/lista_categorias')

def obtener_lista_nombres_categoria():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "SELECT nombre FROM categoria"
    cursor.execute(consulta)

    nombres_categorias = [categoria[0] for categoria in cursor.fetchall()]

    cursor.close()
    conexion.close()

    return nombres_categorias 

# Función para agregar una nueva categoría a la base de datos
def agregar_categoria():
    # Lógica para agregar una nueva categoría a la base de datos
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
  

        # Realizar la inserción en la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = "INSERT INTO categoria (nombre, descripcion) VALUES (%s, %s)"
        cursor.execute(consulta, (nombre, descripcion))
        conexion.commit()
        cursor.close()
        conexion.close()

        # Redirigir a la lista de categorías después de agregar una nueva
        return redirect('/lista_categorias')

    # Renderizar el formulario si el método de solicitud es GET
    return render_template('nueva_categoria.html')

# Función para obtener la lista de categorías desde la base de datos
def mostrar_lista_categoria():
    # Obtener la lista de categorías desde la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "SELECT id_categoria, nombre, descripcion FROM categoria"
    cursor.execute(consulta)

    categorias_tuplas = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Convertir cada tupla en un diccionario con claves adecuadas
    categorias = [{'id': categoria[0], 'nombre': categoria[1], 'descripcion': categoria[2]} for categoria in categorias_tuplas]

    return categorias
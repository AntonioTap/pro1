# viewProducto.py
from flask import render_template, request, redirect
from controllers.conexion import conectar_bd

def obt_producto_por_id(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM productos WHERE id_producto = %s"
    cursor.execute(consulta, (id,))
    producto_tupla = cursor.fetchone()
    cursor.close()
    conexion.close()

    if producto_tupla:
        producto = {
            'id': producto_tupla[0],
            'nombre': producto_tupla[1],
            'precio': producto_tupla[2],
            'categoria': producto_tupla[3],
            'marca': producto_tupla[4],
        }
        return producto
    else:
        return None

def eli_producto(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "DELETE FROM productos WHERE id_producto = %s"
    cursor.execute(consulta, (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect('/lista_productos')

def gua_cambios_producto(id, nombre, precio, categoria, marca):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "UPDATE productos SET nombre = %s, precio = %s, categoria = %s, marca = %s WHERE id_producto = %s"
    cursor.execute(consulta, (nombre, precio, categoria, marca, id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect('/lista_productos')

def obt_lista_nombres_marca():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT nombre FROM marca"
    cursor.execute(consulta)
    nombres_marcas = [marca[0] for marca in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return nombres_marcas

def obt_lista_nombres_categoria():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_categoria, nombre FROM categoria"
    cursor.execute(consulta)
    nombres_categorias = [(categoria[0], categoria[1] ) for categoria in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return nombres_categorias

def obt_id_categoria_por_nombre(nombre_categoria):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_categoria FROM categoria WHERE nombre = %s"
    cursor.execute(consulta, (nombre_categoria,))
    id_categoria = cursor.fetchone()
    cursor.close()
    conexion.close()
    return id_categoria[0] if id_categoria else None

def obt_id_marca_por_nombre(nombre_marca):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_marca FROM marca WHERE nombre = %s"
    cursor.execute(consulta, (nombre_marca,))
    id_marca = cursor.fetchone()
    cursor.close()
    conexion.close()
    return id_marca[0] if id_marca else None

def agre_producto():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        marca = request.form['marca']

        # Obtener los IDs de categoría y marca
        id_categoria = obt_id_categoria_por_nombre(categoria)
        id_marca = obt_id_marca_por_nombre(marca)

        # Insertar el nuevo producto en la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = "INSERT INTO productos (nombre, precio, categoria, marca) VALUES (%s, %s, %s, %s)"
        cursor.execute(consulta, (nombre, precio, id_categoria, id_marca))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect('/lista_productos')

    # Obtener la lista de nombres de categorías y marcas para mostrar en el formulario
    nombres_marcas = obt_lista_nombres_marca()
    nombres_categorias = obt_lista_nombres_categoria()
    return render_template('nuevo_producto.html', nombres_marcas=nombres_marcas, nombres_categorias=nombres_categorias)

def mos_lista_productos():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_producto, nombre, precio, categoria, marca FROM productos"
    cursor.execute(consulta)
    productos_tuplas = cursor.fetchall()
    cursor.close()
    conexion.close()
    productos = [{
        'id': producto[0],
        'nombre': producto[1],
        'precio': producto[2],
        'categoria': producto[3],
        'marca': producto[4],
    } for producto in productos_tuplas]
    return productos

def edi_producto_route(id):
    # Obtener el producto por su ID
    producto = obt_producto_por_id(id)

    if not producto:
        return "Producto no encontrado"

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        marca = request.form['marca']

        # Obtener los IDs de categoría y marca
        id_categoria = obt_id_categoria_por_nombre(categoria)
        id_marca = obt_id_marca_por_nombre(marca)

        # Guardar los cambios del producto en la base de datos
        gua_cambios_producto(id, nombre, precio, id_categoria, id_marca)
        return redirect('/lista_productos')

    # Obtener la lista de nombres de categorías y marcas para mostrar en el formulario
    nombres_marcas = obt_lista_nombres_marca()
    nombres_categorias = obt_lista_nombres_categoria()

    return render_template('editar_producto.html', producto=producto, nombres_marcas=nombres_marcas, nombres_categorias=nombres_categorias)

    
def obt_lista_nombres_marca():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_marca, nombre FROM marca"
    cursor.execute(consulta)
    nombres_marcas = [(marca[0], marca[1]) for marca in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return nombres_marcas

def agr_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        marca = request.form['marca']

        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = "INSERT INTO productos (nombre, precio, categoria, marca) VALUES (%s, %s, %s, %s)"
        cursor.execute(consulta, (nombre, precio, categoria, marca))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect('/lista_productos')

    nombres_marcas = obt_lista_nombres_marca()
    nombres_categorias = obt_lista_nombres_categoria()
    return render_template('nuevo_producto.html', nombres_marcas=nombres_marcas, nombres_categorias=nombres_categorias)
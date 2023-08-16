from flask import render_template, request, redirect
from controllers.conexion import conectar_bd

def obtener_compra_por_id(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT * FROM compras WHERE id_compra = %s"
    cursor.execute(consulta, (id,))
    compra_tupla = cursor.fetchone()
    cursor.close()
    conexion.close()

    if compra_tupla:
        compra = {
            'id_compra': compra_tupla[0],
            'id_producto': compra_tupla[1],
            'fechaCompra': compra_tupla[2],
            'cantidad': compra_tupla[3],
            'precioCompra': compra_tupla[4],
        }
        return compra
    else:
        return None

def guardar_cambios_compra(id_compra, id_producto, fechaCompra, cantidad, precioCompra):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    #consulta = "UPDATE compras SET id_producto = %s, fechaCompra = %s, cantidad = %s, precioCompra = %s, gananciaPorcentaje = %s WHERE id_compra = %s"
    consulta = "UPDATE compras SET id_producto = {}, fechaCompra = {}, cantidad = {}, precioCompra = {} WHERE id_compra = {}"
    consulta = consulta.format(id_producto, fechaCompra, cantidad, precioCompra, id_compra)
    print(consulta)
    cursor.execute(consulta)
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect('/lista_compras')

def obtener_lista_nombres_productos():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_producto, nombre FROM productos"
    cursor.execute(consulta)
    nombres_productos = [(producto[0], producto[1]) for producto in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return nombres_productos

def obtener_id_producto_por_nombre(nombre_producto):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_producto FROM productos WHERE nombre = %s"
    cursor.execute(consulta, (nombre_producto,))
    id_producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return id_producto[0] if id_producto else None

def agregar_compra():
    if request.method == 'POST':
        id_producto = request.form['producto']
        fechaCompra = request.form['fechaCompra']
        cantidad = int(request.form['cantidad'])
        precioCompra = float(request.form['precioCompra'])
        



        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = "INSERT INTO compras (id_producto, fechaCompra, cantidad, precioCompra) VALUES (%s, %s, %s, %s  )"
        cursor.execute(consulta, (id_producto, fechaCompra, cantidad, precioCompra))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect('/lista_compras')

    nombres_productos = obtener_lista_nombres_productos()
    return render_template('nueva_compra.html', nombres_productos=nombres_productos)


def mostrar_lista_compras():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT c.id_compra, p.nombre, c.fechaCompra, c.cantidad, c.precioCompra FROM compras c JOIN productos p ON c.id_producto = p.id_producto"
    cursor.execute(consulta)
    compras_tuplas = cursor.fetchall()
    cursor.close()
    conexion.close()
    compras = [{
        'id_compra': compra[0],
        'nombre_producto': compra[1],
        'fechaCompra': compra[2],
        'cantidad': compra[3],
        'precioCompra': compra[4],
 
    } for compra in compras_tuplas]
    return compras

def editar_compra_route(id):
    compra = obtener_compra_por_id(id)

    if not compra:
        return "Compra no encontrada"

    if request.method == 'POST':
        id_producto = request.form['producto']
        fechaCompra = request.form['fechaCompra']
        cantidad = int(request.form['cantidad'])
        precioCompra = float(request.form['precioCompra'])



        guardar_cambios_compra(id, id_producto, fechaCompra, cantidad, precioCompra)
        return redirect('/lista_compras')

    nombres_productos = obtener_lista_nombres_productos()
    return render_template('editar_compra.html', compra=compra, nombres_productos=nombres_productos)

def eliminar_compra_por_id(id_compra):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "DELETE FROM compras WHERE id_compra = %s"
    cursor.execute(consulta, (id_compra,))
    conexion.commit()
    cursor.close()
    conexion.close()

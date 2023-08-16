from flask import render_template, request, redirect
from controllers.conexion import conectar_bd

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

def obtener_lista_nombres_marca():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT nombre FROM marca"
    cursor.execute(consulta)
    nombres_marcas = [marca[0] for marca in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return nombres_marcas

def obtener_lista_nombres_categoria():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_categoria, nombre FROM categoria"
    cursor.execute(consulta)
    nombres_categorias = [(categoria[0], categoria[1] ) for categoria in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return nombres_categorias

def obtener_id_categoria_por_nombre(nombre_categoria):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_categoria FROM categoria WHERE nombre = %s"
    cursor.execute(consulta, (nombre_categoria,))
    id_categoria = cursor.fetchone()
    cursor.close()
    conexion.close()
    return id_categoria[0] if id_categoria else None

def obtener_id_marca_por_nombre(nombre_marca):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "SELECT id_marca FROM marca WHERE nombre = %s"
    cursor.execute(consulta, (nombre_marca,))
    id_marca = cursor.fetchone()
    cursor.close()
    conexion.close()
    return id_marca[0] if id_marca else None
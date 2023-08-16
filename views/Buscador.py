from flask import Blueprint, render_template, request
from controllers.conexion import conectar_bd

buscador_bp = Blueprint('buscador', __name__)

@buscador_bp.route('/buscar_productos', methods=['POST'])
def buscar_productos():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    categoria = request.form.get('categoria')
    marca = request.form.get('marca')
    precio_max = float(request.form.get('precio_max'))

    consulta = "SELECT * FROM productos WHERE categoria = %s AND marca = %s AND precio <= %s"
    cursor.execute(consulta, (categoria, marca, precio_max))

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template('resultado_busqueda.html', productos=productos)


#app.py
from flask import Flask, render_template, redirect, request, url_for, session
from views.viewUsuario import mostrar_lista_usuarios, agregar_usuario, eliminar_usuario, obtener_usuario_por_id, guardar_cambios_usuario
from views.viewCompra import eliminar_compra_por_id, obtener_compra_por_id, guardar_cambios_compra, agregar_compra, mostrar_lista_compras, obtener_id_producto_por_nombre,obtener_lista_nombres_productos
from views.viewProducto import eliminar_producto, obtener_producto_por_id, guardar_cambios_producto, agregar_producto, mostrar_lista_productos,obtener_lista_nombres_categoria,obtener_lista_nombres_marca
from views.viewMarca import mostrar_lista_marcas, agregar_marca, eliminar_marca, obtener_marca_por_id, guardar_cambios_marca
from views.viewCategoria import eliminar_categoria, obtener_categoria_por_id, guardar_cambios_categoria, agregar_categoria, mostrar_lista_categoria
from controllers.conexion import validar_credenciales 
#from flask_login import LoginManager, login_user, logout_user, login_required
from views.Buscador import buscador_bp


app = Flask(__name__, template_folder="templates")

app.register_blueprint(buscador_bp, ) 


# Configuración para utilizar sesiones
app.secret_key = 'mi_clave_secreta'

# Rutas y lógica de la aplicación
@app.route('/')
def inicio():
    marcas = obtener_lista_nombres_marca()
    categorias = obtener_lista_nombres_categoria()
    
    return render_template('inicio.html', marcas=marcas, categorias=categorias)


@app.route('/login', methods=['GET', 'POST'])
#@login_required
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        resultado = validar_credenciales(correo, contraseña)

        if resultado:
            id_rol = resultado[0]
            if id_rol == 1:  # Si el rol es 1, redirigir a la página del administrador
                session['rol'] = 'administrador'
                session['user']= resultado
                return redirect('/admin')
            elif id_rol == 2:  # Si el rol es 2, redirigir a la página del cajero
                session['user']= resultado
                session['rol'] = 'cajero'
                return redirect('/cajero')

    # Renderizar el formulario si el método de solicitud es GET
    return render_template('login.html')


@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/admin')
#@login_required
def admin():
    # Verificar si el usuario tiene permiso para acceder a la página de administrador
    if 'rol' in session and session['rol'] == 'administrador':
        return render_template('admin.html')
    else:
        return redirect('/login')


#usuarios
@app.route('/nuevo_usuario', methods=['GET', 'POST'])
def nuevo_usuario():
    return agregar_usuario()

#lista usuarios
@app.route('/lista_usuarios')
def lista_usuarios():
    usuarios = mostrar_lista_usuarios()  # Obtener la lista de usuarios desde la función de vista
    return render_template('lista_usuarios.html', usuarios=usuarios)

#editar usuarios
@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario_route(id):
    usuario = obtener_usuario_por_id(id)
    
    if request.method == 'POST':
        # Obtener los valores del formulario
        nombre = request.form['nombre']
        apet_pat = request.form['apet_pat']
        ape_mat = request.form['ape_mat']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        id_rol = request.form['id_rol']

        # Llamar a la función para guardar los cambios en el usuario
        guardar_cambios_usuario(id, nombre, apet_pat, ape_mat, telefono, direccion, correo, contraseña, id_rol)
        return redirect('/lista_usuarios')

    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario_route(id):
    return eliminar_usuario(id)

@app.route('/nueva_compra', methods=['GET', 'POST'])
def nueva_compra():
    return agregar_compra()

@app.route('/lista_compras')
def lista_compras():
    compras = mostrar_lista_compras()
    return render_template('lista_compras.html', compras=compras)

@app.route('/editar_compra/<int:id>', methods=['GET', 'POST'])
def editar_compra(id):
    compra = obtener_compra_por_id(id)
    if not compra:
        return "Compra no encontrada"

    if request.method == 'POST':
        id_producto_nuevo = request.form['producto']
        fechaCompra = request.form['fechaCompra']
        cantidad = int(request.form['cantidad'])
        precioCompra = float(request.form['precioCompra'])
        gananciaPorcentaje = float(request.form['gananciaPorcentaje'])



        guardar_cambios_compra(id, id_producto_nuevo, fechaCompra, cantidad, precioCompra, gananciaPorcentaje)
        return redirect('/lista_compras')

    nombres_productos = obtener_lista_nombres_productos()
    return render_template('editar_compra.html', compra=compra, nombres_productos=nombres_productos)


@app.route('/eliminar_compra/<int:id_compra>')
def eliminar_compra(id_compra):
    eliminar_compra_por_id(id_compra)
    return redirect('/lista_compras')


# Rutas para Productos
@app.route('/nuevo_producto', methods=['GET', 'POST'])
def nuevo_producto():
    return agregar_producto()

@app.route('/lista_productos')
def lista_productos():
    productos = mostrar_lista_productos()
    return render_template('lista_productos.html', productos=productos)

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto_route(id):
    producto = obtener_producto_por_id(id)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        marca = request.form['marca']
        guardar_cambios_producto(id, nombre, precio, categoria, marca)
        return redirect('/lista_productos')

    nombres_marcas = obtener_lista_nombres_marca()
    nombres_categorias = obtener_lista_nombres_categoria()
    return render_template('editar_producto.html', producto=producto, nombres_marcas=nombres_marcas, nombres_categorias=nombres_categorias)

@app.route('/eliminar_producto/<int:id>')
def eliminar_producto_route(id):
    return eliminar_producto(id)

# Categorias
@app.route('/nueva_categoria', methods=['GET', 'POST'])
def nueva_categoria():
    return agregar_categoria()

@app.route('/lista_categorias')
def lista_categorias():
    categorias = mostrar_lista_categoria()
    return render_template('lista_categorias.html', categorias=categorias)

# Editar Categoria
@app.route('/editar_categoria/<int:id>', methods=['GET', 'POST'])
def editar_categoria_route(id):
    categoria = obtener_categoria_por_id(id)
    
    if request.method == 'POST':
        # Obtener los valores del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        # Llamar a la función para guardar los cambios en la categoría
        guardar_cambios_categoria(id, nombre, descripcion)
        return redirect(url_for('lista_categorias'))

    return render_template('editar_categoria.html', categoria=categoria)

@app.route('/eliminar_categoria/<int:id>')
def eliminar_categoria_route(id):
    return eliminar_categoria(id)

# Marcas
@app.route('/nueva_marca', methods=['GET', 'POST'])
def nueva_marca():
    return agregar_marca()


@app.route('/lista_marcas')
def lista_marcas():
    marcas = mostrar_lista_marcas()
    return render_template('lista_marcas.html', marcas=marcas)


@app.route('/editar_marca/<int:id>', methods=['GET', 'POST'])
def editar_marca_route(id):
    marca = obtener_marca_por_id(id)

    if request.method == 'POST':
        # Obtener los valores del formulario
        nombre = request.form['nombre']
        contacto = request.form['contacto']

        # Llamar a la función para guardar los cambios en la marca
        guardar_cambios_marca(id, nombre, contacto)
        return redirect('/lista_marcas')

    return render_template('editar_marca.html', marca=marca)


@app.route('/eliminar_marca/<int:id>')
def eliminar_marca_route(id):
    return eliminar_marca(id)


# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    # Lógica para cerrar sesión
    session.clear()
    return redirect(url_for('inicio'))

#cajero
@app.route('/cajero')
#@login_required
def cajero():
    # Verificar si el usuario tiene permiso para acceder a la página del cajero
    if 'rol' in session and session['rol'] == 'cajero':
        return render_template('cajero.html')
    else:
        return redirect('/login') 
    
@app.route('/inventario1')
def inventario1():
    return render_template('inventario1.html')  

@app.route('/inventario2')
def inventario2():
    return render_template('inventario2.html')  

@app.route('/n_venta')
def n_venta():
    return render_template('n_venta.html')  

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/vender')
def vender():
    return render_template('vender.html')  

@app.route('/nueva_venta', methods=['GET', 'POST'])
def nueva_venta():
    return render_template ('nueva_venta.html')

@app.route('/Nueva_cotizar', methods=['GET', 'POST'])
def Nueva_cotizar():
    return render_template ('Nueva_cotizar.html')

if __name__ == '__main__':
    app.run(debug=True)

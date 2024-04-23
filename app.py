from flask import Flask, redirect, render_template, request, jsonify, url_for
import requests
from spyne.protocol.soap import Soap11
from spyne.client.http import HttpClient

app = Flask(__name__)

# URL base de la API REST
REST_BASE_URL = 'http://localhost:5001/api/'

# URL base del servicio SOAP
SOAP_BASE_URL = 'http://localhost:8000/'

cliente_soap = HttpClient(url=SOAP_BASE_URL, app=Soap11)


class Producto:
    def __init__(self, ids,  nombre, imagen_url, precio):
        self.id = ids
        self.nombre = nombre
        self.imagen_url = imagen_url
        self.precio = precio

# Ruta para mostrar los productos en tu aplicación web utilizando REST


@app.route('/')
def mostrar_productos():
    try:
        # Realizar una solicitud GET a la API REST para obtener los productos
        response = requests.get(REST_BASE_URL + 'productos')
        if response.status_code == 200:
            # Procesar la respuesta JSON de la API REST
            productos = response.json()
            return render_template('productos.html', productos=productos, api_type='REST')
        else:
            raise Exception("Error al obtener productos de la API REST")
    except Exception as ex:
        # Manejar cualquier excepción que pueda ocurrir durante la solicitud
        return render_template('error.html', error=str(ex))

# Ruta para agregar un producto utilizando REST


@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        nombre = request.form['nombre']
        precio = request.form['precio']
        imagen_url = request.form['imagen_url']

        # Realizar una solicitud POST a la API REST para agregar el producto
        response = requests.post(REST_BASE_URL + 'productos', json={
                                 'nombre': nombre, 'precio': precio, 'imagen_url': imagen_url})
        if response.status_code == 201:
            # Redirigir a la página principal después de agregar exitosamente
            return redirect(url_for('mostrar_productos'))
        else:
            raise Exception("Error al agregar el producto")
    except Exception as ex:
        return render_template('error.html', error=str(ex))

# Ruta para eliminar un producto utilizando REST


@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto_rest():
    try:
        id_producto = request.form['id_producto_eliminar']
        # Realizar una solicitud DELETE a la API REST para eliminar el producto
        response = requests.delete(REST_BASE_URL + 'productos/' + id_producto)
        if response.status_code == 200:
            # Redirigir a la página principal después de eliminar exitosamente
            return redirect(url_for('mostrar_productos'))
        else:
            raise Exception("Error al eliminar el producto")
    except Exception as ex:
        return render_template('error.html', error=str(ex))

# Ruta para editar un producto utilizando REST


@app.route('/editar_producto', methods=['POST'])
def editar_producto_rest():
    try:
        producto_id = request.form['id_producto']
        nuevo_nombre = request.form['nombre_edit']
        nueva_imagen_url = request.form['imagen_url_edit']
        nuevo_precio = request.form['precio_edit']

        # Realizar una solicitud PUT a la API REST para editar el producto
        response = requests.put(REST_BASE_URL + f'productos/{producto_id}', json={
                                'nombre': nuevo_nombre, 'imagen_url': nueva_imagen_url, 'precio': nuevo_precio})
        if response.status_code == 200:
            # Redirigir a la página principal después de editar exitosamente
            return redirect(url_for('mostrar_productos'))
        else:
            raise Exception("Error al editar el producto")
    except Exception as ex:
        return render_template('error.html', error=str(ex))

# Ruta para mostrar los productos en tu aplicación web utilizando SOAP


# Ruta para mostrar los productos en tu aplicación web utilizando SOAP
@app.route('/mostrar_productos_soap')
def mostrar_productos_soap():
    try:
        # Realizar una solicitud SOAP para obtener los productos
        productos_soap = cliente_soap.service.obtener_productos()
        # Convertir los productos SOAP en objetos Producto
        productos_list = []
        for producto in productos_soap:
            producto_obj = Producto(
                producto['ids'], producto['nombre'], producto['imagen'], producto['precio'])
            productos_list.append(producto_obj)
        return render_template('productos.html', productos=productos_list)
    except Exception as ex:
        # Manejar cualquier excepción que pueda ocurrir durante la solicitud
        return render_template('error.html', error=str(ex))

# Ruta para agregar un producto utilizando SOAP


@app.route('/agregar_producto_soap', methods=['POST'])
def agregar_producto_soap():
    try:
        nombre = request.form['nombre']
        precio = request.form['precio']
        imagen_url = request.form['imagen_url']
        # Realizar una solicitud SOAP para agregar el producto
        response = cliente_soap.service.agregar_producto(
            nombre, imagen_url, precio)
        if response == "Producto agregado correctamente":
            # Redirigir a la página principal después de agregar exitosamente
            return redirect(url_for('mostrar_productos'))
        else:
            raise Exception(response)
    except Exception as ex:
        return render_template('error.html', error=str(ex))

# Ruta para eliminar un producto utilizando SOAP


@app.route('/eliminar_producto_soap', methods=['POST'])
def eliminar_producto_soap():
    try:
        id_producto = request.form['id_producto_eliminar']
        # Realizar una solicitud SOAP para eliminar el producto
        response = cliente_soap.service.eliminar_producto(id_producto)
        if response == "Producto eliminado correctamente":
            # Redirigir a la página principal después de eliminar exitosamente
            return redirect(url_for('mostrar_productos'))
        else:
            raise Exception(response)
    except Exception as ex:
        return render_template('error.html', error=str(ex))

# Ruta para editar un producto utilizando SOAP


@app.route('/editar_producto_soap', methods=['POST'])
def editar_producto_soap():
    try:
        producto_id = request.form['id_producto']
        nuevo_nombre = request.form['nombre_edit']
        nueva_imagen_url = request.form['imagen_url_edit']
        nuevo_precio = request.form['precio_edit']
        # Realizar una solicitud SOAP para editar el producto

        response = cliente_soap.service.actualizar_producto(
            producto_id, nuevo_nombre, nueva_imagen_url, nuevo_precio)
        if response == "Producto actualizado correctamente":
            # Redirigir a la página principal después de editar exitosamente
            return redirect(url_for('mostrar_productos'))
        else:
            raise Exception(response)
    except Exception as ex:
        return render_template('error.html', error=str(ex))


if __name__ == '__main__':
    app.run(debug=True, port=5100)

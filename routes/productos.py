from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.producto import Producto
from utils.db import db

productos = Blueprint("productos", __name__)


@productos.route("/stock")
def index():
    data = Producto.query.all()
    return render_template("stock.html", productos=data)


@productos.route("/add_products", methods=["POST"])
def add_products():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        medida = request.form["medida"]
        precio = request.form["precio"]
        vencimiento = request.form["vencimiento"]
        proveedor = request.form["proveedor"]
        new_product = Producto(nombre, cantidad, medida, precio, vencimiento, proveedor)
        db.session.add(new_product)
        db.session.commit()
        flash("Producto agregado satisfactoriamente")
        return redirect(url_for("productos.index"))


@productos.route("/update/<id>", methods=["POST", "GET"])
def update(id):
    producto = Producto.query.get(id)

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.cantidad = request.form["cantidad"]
        producto.medida = request.form["medida"]
        producto.precio = request.form["precio"]
        producto.vencimiento = request.form["vencimiento"]
        producto.proveedor = request.form["proveedor"]

        db.session.commit()

        return redirect(url_for("productos.index"))  # min 1.09.55

    flash("Producto editado exitosamente")
    return render_template("update.html", producto=producto)


@productos.route("/delete/<id>")
def delete(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    flash("Producto borrado exitosamente")
    return redirect(url_for("productos.index"))

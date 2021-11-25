from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuario import Usuario
from utils.db import db

usuarios = Blueprint("usuarios", __name__)

@usuarios.route("/update/<id>", methods=["POST", "GET"])
def update(id):
    usuario = Usuario.query.get(id)

    if request.method == "POST":
        usuario.nombre = request.form["nombre"]
        usuario.email = request.form["email"]
        usuario.password = request.form["password"]

        db.session.commit()

        return redirect(url_for("usuarios.index"))

    flash("Usuario editado exitosamente")
    return render_template("update.html", usuario=usuario)


@usuarios.route("/delete/<id>")
def delete(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario borrado exitosamente")
    return redirect(url_for("usuarios.index"))

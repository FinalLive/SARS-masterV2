from flask import g, Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuario import Usuario
from utils.db import db
import bcrypt


auth = Blueprint("auth", __name__)
seed = bcrypt.gensalt()


@auth.route("/")
def index():
    return render_template('index.html')

@auth.route("/index", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.pop('usuario_id', None)

        email = request.form["email"]
        password = request.form["password"]
        password_encode = password.encode("utf-8")
        password_encrypted = bcrypt.hashpw(password_encode, seed)
        exists = db.session.query(Usuario.id).where(Usuario.email=email).first() is not None
        
        if email and password_encrypted in exists: 
                session['usuario_id'] = Usuario.id

                flash('Me alegra que estes aqui de nuevo')
                return redirect(url_for('dashboard'))
        
        flash('El usuario no existe')
        return redirect(url_for('auth.login'))

@auth.route("/registrar", methods=["POST", "GET"])
def registrar():
    if request.method == "POST":
        session.pop('usuario_id', None)

        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]
        password_encode = password.encode("utf-8")
        password_encrypted = bcrypt.hashpw(password_encode, seed)
        exists = db.session.query(Usuario.id).where(Usuario.email=email).scalar() is not None
        
        if nombre and password_encrypted in exists:#passencode - 2passencrypted 
            session['usuario_id'] = Usuario.id
            return redirect(url_for('auth.dashboard'))

        new_user = Usuario(email, password_encrypted, nombre)
        db.session.add(new_user)
        db.session.commit()

        flash("Usuario creado satisfactoriamente")
        return redirect(url_for("auth.dashboard"))
    flash("Las credenciales ya estan siendo usadas")
    return render_template('index.html')

@auth.route('/logout')
def logout():
    
    return redirect(url_for('auth.index'))

@auth.route('/dashboard')
def dashboard():
    if g.usuario.id:
        return render_template('dashboard.html', usuario=session[Usuario.id])

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import traceback
from app.infrastructure.repositories.auth_repository_impl import AuthRepositoryImpl
from app.infrastructure.auth.password_hasher import PasswordHasher
from app.application.login_user import LoginUser
from app.decorators.protection import login_required
from app.infrastructure.repositories.user.usuario_repository_impl import (
    TipoUsuarioRepositoryImpl, UserRepositoryImpl)
from app.application.user.user_services import TypeUserServices, UserServices

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

# Instancias compartidas
auth_repository = AuthRepositoryImpl()
password_hasher = PasswordHasher()
tipo_usuario_repository = TipoUsuarioRepositoryImpl()
user_repository = UserRepositoryImpl()

login_use_case = LoginUser(auth_repository, password_hasher)
listar_tipos_usuario = TypeUserServices(tipo_usuario_repository)
user_services = UserServices(user_repository,password_hasher)
  

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username") 
        password = request.form.get("password")

        try:
            user = login_use_case.execute(username, password) 
            session["user_id"] = user.usuario_id
            return redirect(url_for("auth.dashboard"))
        except ValueError as e:
            flash(str(e))
 
    return render_template("login.html")

@auth_bp.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

@auth_bp.route("/user" ,methods=["GET", "POST"])
@login_required
def user_create():
    print("llegue!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if request.method == "POST":
        nombres = request.form.get("nombres")
        ap_paterno = request.form.get("ap_paterno")
        ap_materno = request.form.get("ap_materno")
        usuario = request.form.get("usuario")
        contrasena = request.form.get("contrasena")
        repetir_contrasena = request.form.get("repetir_contrasena")
        tipo_usuario_id = int(request.form.get("tipo_usuario"))

        # validacion de la contraseña
        if contrasena != repetir_contrasena:
            print("Las contraseñas no coinciden")
            flash("Las contraseñas no coinciden")
            return redirect(url_for("auth.user_create"))

        try:
            print("usuario creado*******************************************")
            user_services.register_user(
                nombres=nombres,
                ap_paterno=ap_paterno,
                ap_materno=ap_materno,
                usuario=usuario,
                contrasena=contrasena,
                tipo_usuario_id=tipo_usuario_id
            )
            
            flash("Usuario creado correctamente", "success")
            return redirect(url_for("auth.dashboard"))
        except Exception as e:
            print("error al registrar usuario:", e)
            traceback.print_exc()
            flash(f"Error al crear el usuario: {str(e)}", "danger")
            

    tipos_usuario = listar_tipos_usuario.execute()
    return render_template("user_create.html", tipos_usuario=tipos_usuario)

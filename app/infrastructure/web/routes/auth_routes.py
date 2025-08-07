from flask import Blueprint, render_template, redirect, url_for, request, flash,session

from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.auth.password_hasher import PasswordHasher
from app.application.register_user import RegisterUser
from app.application.login_user import LoginUser
from app.decorators.protection import login_required


auth_bp = Blueprint("auth", __name__, template_folder="../templates")

# Instancias compartidas (podrías moverlas a un contenedor de dependencias en el futuro)
user_repository = UserRepositoryImpl()
password_hasher = PasswordHasher()

register_use_case = RegisterUser(user_repository, password_hasher)
login_use_case = LoginUser(user_repository, password_hasher)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            user = login_use_case.execute(email, password)
            session["user_id"] = user.id
            return redirect(url_for("auth.dashboard"))
        except ValueError as e:
            flash(str(e))
 
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        try: 
            user = register_use_case.execute(username, email, password)
            return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e))

    return render_template("register.html")

@auth_bp.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

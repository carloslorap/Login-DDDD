from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Debes iniciar sesión primero.")
            return redirect(url_for("auth.login"))  # Cambia 'auth.login' por el nombre correcto
        return f(*args, **kwargs)
    return decorated_function

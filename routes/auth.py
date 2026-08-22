from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash

from models import Admin

auth_bp = Blueprint("auth", __name__)


# =====================================
# Admin Login
# =====================================

@auth_bp.route("/admin/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):

            login_user(admin)

            return redirect(url_for("admin.dashboard"))

        flash("Invalid username or password.")

    return render_template("admin/login.html")
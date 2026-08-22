from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Contact

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        new_contact = Contact(
            full_name=request.form.get("full_name"),
            email=request.form.get("email"),
            subject=request.form.get("subject"),
            message=request.form.get("message")
        )

        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for("contact.contact"))

    return render_template("contact.html")
from werkzeug.security import generate_password_hash

from app import app
from models import db, Admin


with app.app_context():

    username = "admin"

    existing_admin = Admin.query.filter_by(username=username).first()

    if existing_admin:
        print("Admin account already exists.")
        print("No changes were made.")

    else:
        password = input("Enter the initial admin password: ").strip()

        if len(password) < 8:
            raise ValueError(
                "Password must contain at least 8 characters."
            )

        hashed_password = generate_password_hash(password)

        admin = Admin(
            username=username,
            password=hashed_password
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin account created successfully!")
        print("Username:", username)
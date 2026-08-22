from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

import os

load_dotenv()


# =====================================
# Configuration
# =====================================

from config import Config

from models import (
    db,
    Admin,
    SiteSettings
)


# =====================================
# Routes
# =====================================

from routes.home import home_bp
from routes.about import about_bp
from routes.programs import programs_bp
from routes.news import news_bp
from routes.contact import contact_bp
from routes.volunteer import volunteer_bp
from routes.donate import donate_bp
from routes.admin import admin_bp
from routes.auth import auth_bp



# =====================================
# Flask Application
# =====================================

app = Flask(__name__)

app.config.from_object(Config)


# =====================================
# Upload Folder
# =====================================

app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "uploads"
)


# =====================================
# Database
# =====================================

db.init_app(app)

migrate = Migrate(
    app,
    db
)


# =====================================
# Flask-Login
# =====================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):

    return Admin.query.get(
        int(user_id)
    )


# =====================================
# Site Settings
# =====================================

@app.context_processor
def inject_settings():

    return {
        "settings": SiteSettings.query.first()
    }


# =====================================
# Register Blueprints
# =====================================

app.register_blueprint(home_bp)
app.register_blueprint(about_bp)
app.register_blueprint(programs_bp)
app.register_blueprint(news_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(volunteer_bp)
app.register_blueprint(donate_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)


# =====================================
# Database Initialization
# =====================================

with app.app_context():

    db.create_all()


# =====================================
# Show Registered Routes
# =====================================

print("\n===== REGISTERED ROUTES =====")

for rule in app.url_map.iter_rules():

    print(rule)

print("=============================\n")


# =====================================
# Run Application
# =====================================

if __name__ == "__main__":

    app.run()
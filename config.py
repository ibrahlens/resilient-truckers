import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    # =====================================
    # Flask Secret Key
    # =====================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-only-change-me"
    )

    # =====================================
    # Database
    # =====================================

    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )
    else:
        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///"
            + os.path.join(
                BASE_DIR,
                "instance",
                "foundation.db"
            )
        )

    # =====================================
    # SQLAlchemy
    # =====================================

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =====================================
    # Upload Folder
    # =====================================

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    # =====================================
    # Maximum Upload Size
    # =====================================

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # =====================================
    # Allowed Image Extensions
    # =====================================

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp"
    }

    # =====================================
    # Email Configuration
    # =====================================

    RESEND_API_KEY = os.getenv(
        "RESEND_API_KEY"
    )

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER"
    )

    SITE_URL = os.getenv(
        "SITE_URL",
        "http://127.0.0.1:5000"
    )
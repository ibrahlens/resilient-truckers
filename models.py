from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
# =====================================
# Database Initialization
# =====================================

db = SQLAlchemy()


# =====================================
# Contact Model
# =====================================

class Contact(db.Model):

    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        nullable=False
    )

    subject = db.Column(
        db.String(150),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    def __repr__(self):
        return f"<Contact {self.full_name}>"


# =====================================
# Admin Model
# =====================================

class Admin(UserMixin, db.Model):

    __tablename__ = "admins"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def __repr__(self):
        return f"<Admin {self.username}>"
        
# =====================================
# News Model
# =====================================

class News(db.Model):

    __tablename__ = "news"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    summary = db.Column(
        db.String(300),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    author = db.Column(
        db.String(100),
        default="Resilient Truckers Foundation"
    )

    category = db.Column(
        db.String(100),
        default="General"
    )

    image = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )

    def __repr__(self):
        return f"<News {self.title}>"


# =====================================
# Member Model
# =====================================

class Member(db.Model):

    __tablename__ = "members"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    county = db.Column(
        db.String(100),
        nullable=False
    )

    occupation = db.Column(
        db.String(100),
        nullable=False
    )

    is_driver = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    vehicle_registration = db.Column(
        db.String(20),
        nullable=True
    )

    driving_license = db.Column(
        db.String(50),
        nullable=True
    )

    company = db.Column(
        db.String(150),
        nullable=True
    )

    experience = db.Column(
        db.String(50),
        nullable=True
    )

    joining_reason = db.Column(
        db.String(100),
        nullable=False
    )

    reason = db.Column(
        db.Text,
        nullable=True
    )

    # =====================================
    # Membership Status
    # =====================================

    status = db.Column(
        db.String(20),
        default="Pending",
        nullable=False
    )

    # =====================================
    # Official RTF Registration Number
    # =====================================

    member_id = db.Column(
        db.String(20),
        unique=True,
        nullable=True,
        index=True
    )

    # =====================================
    # Date Joined
    # =====================================

    created_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<Member {self.full_name}>"



# Donation Model
# =====================================

class Donation(db.Model):

    __tablename__ = "donations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================
    # Donor Information
    # =====================================

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False
    )

    phone = db.Column(
        db.String(30),
        nullable=False
    )

    # =====================================
    # Donation Information
    # =====================================

    amount = db.Column(
        db.Float,
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=True
    )

    payment_method = db.Column(
        db.String(50),
        nullable=True,
        default="Manual"
    )

    # =====================================
    # Status
    # =====================================

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )

    # =====================================
    # Timestamp
    # =====================================

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):

        return (
            f"<Donation "
            f"{self.full_name} "
            f"- KSh {self.amount}>"
        )
# =====================================
# Site Settings Model
# =====================================

class SiteSettings(db.Model):

    __tablename__ = "site_settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Foundation Information
    foundation_name = db.Column(
        db.String(150),
        default="Resilient Truckers Foundation"
    )

    short_name = db.Column(
        db.String(50),
        default="RTF"
    )

    email = db.Column(
        db.String(120)
    )

    phone = db.Column(
        db.String(30)
    )

    alternative_phone = db.Column(
        db.String(30)
    )

    address = db.Column(
        db.String(255)
    )

    website = db.Column(
        db.String(255)
    )

    # Social Media
    facebook = db.Column(
        db.String(255)
    )

    instagram = db.Column(
        db.String(255)
    )

    twitter = db.Column(
        db.String(255)
    )

    linkedin = db.Column(
        db.String(255)
    )

    youtube = db.Column(
        db.String(255)
    )

    whatsapp= db.Column(
        db.String(250)
    )

    whatsapp_link = db.Column(
        db.String(255)
    )

    # M-Pesa
    mpesa_paybill = db.Column(
        db.String(50)
    )

    mpesa_account = db.Column(
        db.String(100)
    )

    # SEO
    meta_title = db.Column(
        db.String(255)
    )

    meta_description = db.Column(
        db.Text
    )

    # Footer
    copyright = db.Column(
        db.String(255)
    )

    # Donation Settings
    currency = db.Column(
        db.String(10),
        default="KES"
    )

    minimum_donation = db.Column(
        db.Float,
        default=100
    )

    donations_enabled = db.Column(
        db.Boolean,
        default=True
    )

    # Branding
    logo = db.Column(
        db.String(255)
    )

    favicon = db.Column(
        db.String(255)
    )

    # Homepage
    hero_title = db.Column(
        db.String(255)
    )

    hero_subtitle = db.Column(
        db.Text
    )

    # Maintenance Mode
    maintenance_mode = db.Column(
        db.Boolean,
        default=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<SiteSettings {self.foundation_name}>"


# =====================================
# Programs
# =====================================

class Program(db.Model):

    __tablename__ = "programs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    short_description = db.Column(
        db.Text,
        nullable=False
    )

    full_description = db.Column(
        db.Text
    )

    icon = db.Column(
        db.String(100),
        default="fa-solid fa-truck"
    )

    image = db.Column(
        db.String(255)
    )

    display_order = db.Column(
        db.Integer,
        default=1
    )

    featured = db.Column(
        db.Boolean,
        default=False
    )

    status = db.Column(
        db.String(20),
        default="Published"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
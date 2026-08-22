import os

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    current_app
)

from flask_login import (
    login_required,
    logout_user,
    current_user
)

from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from models import (
    db,
    Admin,
    Contact,
    News,
    Member,
    Donation,
    SiteSettings,
    Program
)
# =====================================
# Admin Blueprint
# =====================================

admin_bp = Blueprint(
    "admin",
    __name__
)





# =====================================
# Dashboard
# =====================================

@admin_bp.route("/admin")
@login_required
def dashboard():

    total_messages = Contact.query.count()

    total_news = News.query.count()

    total_members = Member.query.filter_by(
    status="Approved"
).count()
    approved_members = Member.query.filter_by(
        status="Approved"
    ).count()

    pending_members = Member.query.filter_by(
        status="Pending"
    ).count()

    rejected_members = Member.query.filter_by(
        status="Rejected"
    ).count()

    received_donations = Donation.query.filter_by(
        status="Received"
    ).count()
    
    pending_donations = Donation.query.filter_by(
        status="Pending"
    ).count()
    
    rejected_donations = Donation.query.filter_by(
    status="Rejected"
    ).count()

    total_donations = sum(
        donation.amount
        for donation in Donation.query.filter_by(
            status="Received"
        ).all()
    )

    recent_messages = (
        Contact.query
        .order_by(Contact.id.desc())
        .limit(5)
        .all()
    )
    return render_template(
    "admin/dashboard.html",
    total_messages=total_messages,
    total_news=total_news,
    total_members=total_members,
    total_donations=total_donations,
    approved_members=approved_members,
    pending_members=pending_members,
    rejected_members=rejected_members,
    received_donations=received_donations,
    pending_donations=pending_donations,
    rejected_donations=rejected_donations,
    recent_messages=recent_messages
)
# =====================================
# Messages
# =====================================

@admin_bp.route("/admin/messages")
@login_required
def messages():

    messages = (
        Contact.query
        .order_by(Contact.id.desc())
        .all()
    )

    return render_template(
        "admin/messages.html",
        messages=messages
    )


# =====================================
# View Message
# =====================================

@admin_bp.route("/admin/message/<int:id>")
@login_required
def view_message(id):

    message = Contact.query.get_or_404(id)

    return render_template(
        "admin/view_message.html",
        message=message
    )


# =====================================
# Delete Message
# =====================================

@admin_bp.route("/admin/message/delete/<int:id>")
@login_required
def delete_message(id):

    message = Contact.query.get_or_404(id)

    db.session.delete(message)
    db.session.commit()

    flash("Message deleted successfully.")

    return redirect(url_for("admin.messages"))



# =====================================
# News
# =====================================

@admin_bp.route("/admin/news")
@login_required
def news():

    articles = (
        News.query
        .order_by(News.created_at.desc())
        .all()
    )

    return render_template(
        "admin/news.html",
        articles=articles
    )


# =====================================
# Add News
# =====================================

@admin_bp.route(
    "/admin/news/add",
    methods=["GET", "POST"]
)
@login_required
def add_news():

    if request.method == "POST":

        title = request.form.get("title")
        category = request.form.get("category")
        summary = request.form.get("summary")
        content = request.form.get("content")

        image = request.files.get("image")

        filename = None

        if image and image.filename:

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        article = News(
            title=title,
            category=category,
            summary=summary,
            content=content,
            image=filename
        )

        db.session.add(article)
        db.session.commit()

        flash("News article published successfully.")

        return redirect(
            url_for("admin.news")
        )

    return render_template(
        "admin/add_news.html"
    )
# =====================================
# Edit News
# =====================================

@admin_bp.route(
    "/admin/news/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_news(id):

    article = News.query.get_or_404(id)

    if request.method == "POST":

        article.title = request.form.get("title")
        article.content = request.form.get("content")

        db.session.commit()

        flash("Article updated successfully.")

        return redirect(
            url_for("admin.news")
        )

    return render_template(
        "admin/edit_news.html",
        article=article
    )


# =====================================
# Delete News
# =====================================

@admin_bp.route("/admin/news/delete/<int:id>")
@login_required
def delete_news(id):

    article = News.query.get_or_404(id)

    db.session.delete(article)

    db.session.commit()

    flash("Article deleted successfully.")

    return redirect(
        url_for("admin.news")
    )


# =====================================
# Members
# =====================================

@admin_bp.route("/admin/volunteers")
@login_required
def volunteers():

    members = (
        Member.query
        .order_by(Member.created_at.desc())
        .all()
    )

    return render_template(
        "admin/volunteers.html",
        members=members
    )


# =====================================
# View Member
# =====================================

@admin_bp.route("/admin/member/<int:id>")
@login_required
def view_member(id):

    member = Member.query.get_or_404(id)

    return render_template(
        "admin/view_member.html",
        member=member
    )
# =====================================
# Approve Member
# =====================================

@admin_bp.route("/admin/member/approve/<int:id>")
@login_required
def approve_member(id):

    member = Member.query.get_or_404(id)

    member.status = "Approved"

    db.session.commit()

    flash(
        "Member approved successfully.",
        "success"
    )

    return redirect(
        url_for("admin.view_member", id=id)
    )


# =====================================
# Reject Member
# =====================================

@admin_bp.route("/admin/member/reject/<int:id>")
@login_required
def reject_member(id):

    member = Member.query.get_or_404(id)

    member.status = "Rejected"

    db.session.commit()

    flash(
        "Member rejected.",
        "warning"
    )

    return redirect(
        url_for("admin.view_member", id=id)
    )
# =====================================
# Delete Member
# =====================================

@admin_bp.route("/admin/member/delete/<int:id>")
@login_required
def delete_member(id):

    member = Member.query.get_or_404(id)

    db.session.delete(member)

    db.session.commit()

    flash(
        "Member deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.volunteers")
    )


# =====================================
# Donations
# =====================================

from sqlalchemy import func, extract
from datetime import datetime


@admin_bp.route("/admin/donations")
@login_required
def donations():

    donations = (
        Donation.query
        .order_by(
            Donation.created_at.desc()
        )
        .all()
    )

    # =====================================
    # Overview Statistics
    # =====================================

    total_amount = (
        db.session.query(
            func.sum(Donation.amount)
        )
        .filter(
            Donation.status == "Received"
        )
        .scalar()
        or 0
    )

    total_received = (
        Donation.query
        .filter_by(
            status="Received"
        )
        .count()
    )

    total_pending = (
        Donation.query
        .filter_by(
            status="Pending"
        )
        .count()
    )

    total_rejected = (
        Donation.query
        .filter_by(
            status="Rejected"
        )
        .count()
    )

    total_donors = (
        db.session.query(
            func.count(
                func.distinct(
                    Donation.phone
                )
            )
        )
        .scalar()
        or 0
    )

    average_donation = (
        db.session.query(
            func.avg(Donation.amount)
        )
        .filter(
            Donation.status == "Received"
        )
        .scalar()
        or 0
    )

    largest_donation = (
        db.session.query(
            func.max(Donation.amount)
        )
        .filter(
            Donation.status == "Received"
        )
        .scalar()
        or 0
    )

    # =====================================
    # Current Month
    # =====================================

    now = datetime.now()

    monthly_total = (
        db.session.query(
            func.sum(Donation.amount)
        )
        .filter(
            Donation.status == "Received",
            func.strftime(
                "%m",
                Donation.created_at
            ) == now.strftime("%m"),
            func.strftime(
                "%Y",
                Donation.created_at
            ) == now.strftime("%Y")
        )
        .scalar()
        or 0
    )

    # =====================================
    # Monthly Trend
    # =====================================

    monthly_data = (
        db.session.query(
            extract(
                "month",
                Donation.created_at
            ).label("month"),

            func.sum(
                Donation.amount
            ).label("total")
        )
        .filter(
            Donation.status == "Received"
        )
        .group_by(
            extract(
                "month",
                Donation.created_at
            )
        )
        .order_by(
            extract(
                "month",
                Donation.created_at
            )
        )
        .all()
    )

    month_labels = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    monthly_labels = []

    monthly_totals = []

    for row in monthly_data:

        monthly_labels.append(
            month_labels[
                int(row.month) - 1
            ]
        )

        monthly_totals.append(
            float(row.total)
        )

    return render_template(
        "admin/donations.html",

        donations=donations,

        total_amount=total_amount,

        total_received=total_received,

        total_pending=total_pending,

        total_rejected=total_rejected,

        total_donors=total_donors,

        average_donation=average_donation,

        largest_donation=largest_donation,

        monthly_total=monthly_total,

        monthly_labels=monthly_labels,

        monthly_totals=monthly_totals
    )
# =====================================
# View Donation
# =====================================

@admin_bp.route("/admin/donation/<int:id>")
@login_required
def view_donation(id):

    donation = Donation.query.get_or_404(id)

    return render_template(
        "admin/view_donation.html",
        donation=donation
    )




# =====================================
# Mark Donation as Received
# =====================================

@admin_bp.route("/admin/donation/receive/<int:id>")
@login_required
def receive_donation(id):

    donation = Donation.query.get_or_404(id)

    donation.status = "Received"

    db.session.commit()

    flash(
        "Donation marked as received successfully.",
        "success"
    )

    return redirect(
        url_for("admin.donations")
    )


# =====================================
# Delete Donation
# =====================================

@admin_bp.route("/admin/donation/delete/<int:id>")
@login_required
def delete_donation(id):

    donation = Donation.query.get_or_404(id)

    db.session.delete(donation)

    db.session.commit()

    flash(
        "Donation deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.donations")
    )



# =====================================
# Settings
# =====================================
@admin_bp.route(
    "/admin/settings",
    methods=["GET", "POST"]
)
@login_required
def settings():

    settings = SiteSettings.query.first()

    if not settings:

        settings = SiteSettings()

        db.session.add(settings)

        db.session.commit()

    if request.method == "POST":

        try:

            # =====================================
            # Foundation Information
            # =====================================

            settings.foundation_name = request.form.get(
                "foundation_name"
            )

            settings.short_name = request.form.get(
                "short_name"
            )

            settings.email = request.form.get(
                "email"
            )

            settings.phone = request.form.get(
                "phone"
            )

            settings.alternative_phone = request.form.get(
                "alternative_phone"
            )

            settings.website = request.form.get(
                "website"
            )

            settings.address = request.form.get(
                "address"
            )

            # =====================================
            # Social Media
            # =====================================

            settings.facebook = request.form.get(
                "facebook"
            )

            settings.instagram = request.form.get(
                "instagram"
            )

            settings.twitter = request.form.get(
                "twitter"
            )

            settings.linkedin = request.form.get(
                "linkedin"
            )

            settings.youtube = request.form.get(
                "youtube"
            )

            settings.whatsapp_link = request.form.get(
                "whatsapp_link"
            )

            # =====================================
            # M-Pesa
            # =====================================

            settings.mpesa_paybill = request.form.get(
                "mpesa_paybill"
            )

            settings.mpesa_account = request.form.get(
                "mpesa_account"
            )

            # =====================================
            # SEO
            # =====================================

            settings.meta_title = request.form.get(
                "meta_title"
            )

            settings.meta_description = request.form.get(
                "meta_description"
            )

            # =====================================
            # Footer
            # =====================================

            settings.copyright = request.form.get(
                "copyright"
            )

            # =====================================
            # Remove Logo
            # =====================================

            if request.form.get("remove_logo"):

                if settings.logo:

                    path = os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        settings.logo
                    )

                    if os.path.exists(path):
                        os.remove(path)

                    settings.logo = None

            # =====================================
            # Upload Logo
            # =====================================

            logo = request.files.get("logo")

            if logo and logo.filename:

                filename = secure_filename(
                    logo.filename
                )

                logo.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )

                settings.logo = filename

            # =====================================
            # Remove Favicon
            # =====================================

            if request.form.get("remove_favicon"):

                if settings.favicon:

                    path = os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        settings.favicon
                    )

                    if os.path.exists(path):
                        os.remove(path)

                    settings.favicon = None

            # =====================================
            # Upload Favicon
            # =====================================

            favicon = request.files.get("favicon")

            if favicon and favicon.filename:

                filename = secure_filename(
                    favicon.filename
                )

                favicon.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )

                settings.favicon = filename

            # =====================================
            # Admin Login Details
            # =====================================

            current_password = request.form.get(
                "current_password",
                ""
            ).strip()

            new_username = request.form.get(
                "new_username",
                ""
            ).strip()

            new_password = request.form.get(
                "new_password",
                ""
            ).strip()

            confirm_password = request.form.get(
                "confirm_password",
                ""
            ).strip()

            # =====================================
            # Security Validation
            # =====================================

            security_change_requested = (
                current_password
                or new_username
                or new_password
                or confirm_password
            )

            if security_change_requested:

                admin = db.session.get(
                    Admin,
                    current_user.id
                )

                if not admin:

                    raise ValueError(
                        "Administrator account could not be found."
                    )

                # ---------------------------------
                # Verify Current Password
                # ---------------------------------

                if not current_password:

                    raise ValueError(
                        "Enter your current password to change "
                        "your login details."
                    )

                if not check_password_hash(
                    admin.password,
                    current_password
                ):

                    raise ValueError(
                        "Current password is incorrect."
                    )

                # ---------------------------------
                # Username
                # ---------------------------------

                if new_username:

                    existing_admin = Admin.query.filter(
                        Admin.username == new_username,
                        Admin.id != admin.id
                    ).first()

                    if existing_admin:

                        raise ValueError(
                            "That username is already in use."
                        )

                    admin.username = new_username

                # ---------------------------------
                # Password
                # ---------------------------------

                if new_password:

                    if len(new_password) < 8:

                        raise ValueError(
                            "New password must contain at least "
                            "8 characters."
                        )

                    if new_password != confirm_password:

                        raise ValueError(
                            "New passwords do not match."
                        )

                    admin.password = generate_password_hash(
                        new_password
                    )

            # =====================================
            # Save Everything
            # =====================================

            db.session.commit()

            flash(
                "Settings updated successfully.",
                "success"
            )

            return redirect(
                url_for("admin.settings")
            )

        # =====================================
        # Validation Error
        # =====================================

        except ValueError as e:

            db.session.rollback()

            flash(
                str(e),
                "danger"
            )

            return redirect(
                url_for("admin.settings")
            )

        # =====================================
        # Unexpected Error
        # =====================================

        except Exception as e:

            db.session.rollback()

            print(
                "\n========== SETTINGS ERROR =========="
            )

            print(e)

            import traceback

            traceback.print_exc()

            print(
                "====================================\n"
            )

            flash(
                "Something went wrong while saving "
                "your settings. Please try again.",
                "danger"
            )

            return redirect(
                url_for("admin.settings")
            )

    return render_template(
        "admin/settings.html",
        settings=settings
    )
# =====================================
# Programs
# =====================================

@admin_bp.route("/admin/programs")
@login_required
def programs():

    programs = Program.query.order_by(
        Program.display_order.asc()
    ).all()

    return render_template(
        "admin/programs.html",
        programs=programs
    )



# =====================================
# Add Program
# =====================================

@admin_bp.route(
    "/admin/programs/add",
    methods=["GET", "POST"]
)
@login_required
def add_program():

    if request.method == "POST":

        # =========================
        # Upload Image
        # =========================

        image = request.files.get("image")

        filename = None

        if image and image.filename:

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        # =========================
        # Create Program
        # =========================

        program = Program(

            title=request.form.get("title"),

            short_description=request.form.get(
                "short_description"
            ),

            full_description=request.form.get(
                "full_description"
            ),

            icon=request.form.get("icon")
                or "fa-solid fa-truck",

            image=filename,

            display_order=int(
                request.form.get("display_order") or 1
            ),

            featured=bool(
                request.form.get("featured")
            ),

            status=request.form.get("status")
                or "Published"

        )

        db.session.add(program)

        db.session.commit()

        flash(
            "Program created successfully.",
            "success"
        )

        return redirect(
            url_for("admin.programs")
        )

    return render_template(
        "admin/add_program.html"
    )



# =====================================
# Edit Program
# =====================================

@admin_bp.route(
    "/admin/programs/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_program(id):

    program = Program.query.get_or_404(id)

    if request.method == "POST":

        # =========================
        # Update Text Fields
        # =========================

        program.title = request.form.get("title")

        program.short_description = request.form.get(
            "short_description"
        )

        program.full_description = request.form.get(
            "full_description"
        )

        program.display_order = int(
            request.form.get("display_order") or 1
        )

        program.status = request.form.get("status")

        program.featured = bool(
            request.form.get("featured")
        )

        # =========================
        # Replace Image (Optional)
        # =========================

        image = request.files.get("image")

        if image and image.filename:

            # Delete old image
            if program.image:

                old_path = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    program.image
                )

                if os.path.exists(old_path):
                    os.remove(old_path)

            # Save new image
            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            program.image = filename

        db.session.commit()

        flash(
            "Program updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin.programs")
        )

    return render_template(
        "admin/edit_program.html",
        program=program
    )


# =====================================
# Delete Program
# =====================================

@admin_bp.route(
    "/admin/programs/delete/<int:id>"
)
@login_required
def delete_program(id):

    program = Program.query.get_or_404(id)

    db.session.delete(program)

    db.session.commit()

    flash(
        "Program deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.programs")
    )

# =====================================
# Logout
# =====================================

@admin_bp.route("/admin/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.")

    return redirect(
        url_for("auth.login")
    )
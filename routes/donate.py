from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from models import db, Donation,SiteSettings

from services.utils import (
    is_valid_phone_number
)


# =====================================
# Donation Blueprint
# =====================================

donate_bp = Blueprint(
    "donate",
    __name__
)


# =====================================
# Donation
# =====================================

@donate_bp.route(
    "/donate",
    methods=["GET", "POST"]
)
def donate():

    if request.method == "POST":

        try:

            # =====================================
            # Get Form Data
            # =====================================

            full_name = request.form.get(
                "full_name",
                ""
            ).strip()

            email = request.form.get(
                "email",
                ""
            ).strip()

            phone = request.form.get(
                "phone",
                ""
            ).strip()

            message = request.form.get(
                "message",
                ""
            ).strip()

            amount_text = request.form.get(
                "amount",
                ""
            ).strip()

            # =====================================
            # Validation
            # =====================================

            if not full_name:

                raise ValueError(
                    "Full name is required."
                )

            if not email:

                raise ValueError(
                    "Email address is required."
                )

            if not phone:

                raise ValueError(
                    "Phone number is required."
                )

            if not is_valid_phone_number(phone):

                raise ValueError(
                    "Please enter a valid Kenyan phone number."
                )

            if not amount_text:

                raise ValueError(
                    "Donation amount is required."
                )

            try:

                amount = float(
                    amount_text
                )

            except ValueError:

                raise ValueError(
                    "Please enter a valid donation amount."
                )

            if amount < 1:

                raise ValueError(
                    "Donation amount must be at least KSh 1."
                )

            # =====================================
            # Create Donation
            # =====================================

            donation = Donation(

                full_name=full_name,

                email=email,

                phone=phone,

                amount=amount,

                message=message,

                status="Pending"

            )

            # =====================================
            # Save Donation
            # =====================================

            db.session.add(
                donation
            )

            db.session.commit()

            # =====================================
            # Success
            # =====================================

            flash(
                "Thank you for supporting the "
                "Resilient Truckers Foundation. "
                "Your donation has been submitted successfully.",
                "success"
            )

            return redirect(
                url_for("donate.donate")
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
                url_for("donate.donate")
            )

        # =====================================
        # Unexpected Error
        # =====================================

        except Exception as e:

            db.session.rollback()

            print(
                "\n========== DONATION ERROR =========="
            )

            print(e)

            import traceback

            traceback.print_exc()

            print(
                "====================================\n"
            )

            flash(
                "Something went wrong while submitting "
                "your donation. Please try again.",
                "danger"
            )

            return redirect(
                url_for("donate.donate")
            )

    # =====================================
    # Display Donation Form
    # =====================================
    settings = SiteSettings.query.first()
    return render_template(
        "donate.html",
        settings=settings
    )
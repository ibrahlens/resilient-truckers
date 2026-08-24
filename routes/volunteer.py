from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from models import (
    db,
    Member
)


volunteer_bp = Blueprint(
    "volunteer",
    __name__
)


# =====================================
# Become a Member
# =====================================

@volunteer_bp.route(
    "/volunteer",
    methods=["GET", "POST"]
)
def volunteer():

    if request.method == "POST":

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
        ).strip().lower()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        county = request.form.get(
            "county",
            ""
        ).strip()

        occupation = request.form.get(
            "occupation",
            ""
        ).strip()

        is_driver = bool(
            request.form.get("is_driver")
        )

        vehicle_registration = request.form.get(
            "vehicle_registration",
            ""
        ).strip()

        driving_license = request.form.get(
            "driving_license",
            ""
        ).strip()

        company = request.form.get(
            "company",
            ""
        ).strip()

        experience = request.form.get(
            "experience",
            ""
        ).strip()

        joining_reason = request.form.get(
            "joining_reason",
            ""
        ).strip()

        reason = request.form.get(
            "reason",
            ""
        ).strip()

        # =====================================
        # Basic Validation
        # =====================================

        if not full_name or not email or not phone:
            flash(
                "Please complete all required fields.",
                "warning"
            )

            return redirect(
                url_for("volunteer.volunteer")
            )

        if not county or not occupation:
            flash(
                "Please complete all required fields.",
                "warning"
            )

            return redirect(
                url_for("volunteer.volunteer")
            )

        if not joining_reason:
            flash(
                "Please select your primary interest.",
                "warning"
            )

            return redirect(
                url_for("volunteer.volunteer")
            )

        # =====================================
        # Driver Validation
        # =====================================

        if is_driver:

            if not vehicle_registration:
                flash(
                    "Vehicle registration is required for drivers.",
                    "warning"
                )

                return redirect(
                    url_for("volunteer.volunteer")
                )

            if not driving_license:
                flash(
                    "Driving licence information is required for drivers.",
                    "warning"
                )

                return redirect(
                    url_for("volunteer.volunteer")
                )

        # =====================================
        # Check Existing Email
        # =====================================

        existing_member = Member.query.filter_by(
            email=email
        ).first()

        if existing_member:

            flash(
                "A member with this email already exists.",
                "warning"
            )

            return redirect(
                url_for("volunteer.volunteer")
            )

        # =====================================
        # Create Member
        # =====================================

        member = Member(

            full_name=full_name,

            email=email,

            phone=phone,

            county=county,

            occupation=occupation,

            is_driver=is_driver,

            vehicle_registration=(
                vehicle_registration
                if is_driver
                else None
            ),

            driving_license=(
                driving_license
                if is_driver
                else None
            ),

            company=company,

            experience=experience,

            joining_reason=joining_reason,

            reason=reason,

            # ---------------------------------
            # Important:
            # New applications are always
            # Pending.
            # ---------------------------------

            status="Pending",

            # ---------------------------------
            # Important:
            # Registration number remains empty
            # until an administrator approves
            # the member.
            # ---------------------------------

            member_id=None
        )

        db.session.add(member)
        db.session.commit()

        # =====================================
        # Success Message
        # =====================================

        flash(
            "Your membership application has been "
            "submitted successfully. Your application "
            "will be reviewed by our team.",
            "success"
        )

        return redirect(
            url_for("volunteer.volunteer")
        )

    # =====================================
    # Display Registration Form
    # =====================================

    return render_template(
        "volunteers.html"
    )
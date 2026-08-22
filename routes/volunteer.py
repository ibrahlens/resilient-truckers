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

        # Check if email already exists
        existing_member = Member.query.filter_by(
            email=request.form.get("email")
        ).first()

        if existing_member:

            flash(
                "A member with this email already exists.",
                "warning"
            )

            return redirect(
                url_for("volunteer.volunteer")
            )

        member = Member(
    full_name=request.form.get("full_name"),
    email=request.form.get("email"),
    phone=request.form.get("phone"),
    county=request.form.get("county"),
    occupation=request.form.get("occupation"),
    is_driver=bool(request.form.get("is_driver")),
    vehicle_registration=request.form.get("vehicle_registration"),
    driving_license=request.form.get("driving_license"),
    company=request.form.get("company"),
    experience=request.form.get("experience"),
    joining_reason=request.form.get("joining_reason"),
    reason=request.form.get("reason")
)

        db.session.add(member)
        db.session.commit()

        flash(
            "Your membership application has been submitted successfully!",
            "success"
        )

        return redirect(
            url_for("volunteer.volunteer")
        )

    return render_template(
        "volunteers.html"
    )
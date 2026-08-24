from flask import (
    Blueprint,
    render_template,
    request
)

from models import Member


verify_bp = Blueprint(
    "verify",
    __name__
)


# =====================================
# Verify Driver
# =====================================

@verify_bp.route(
    "/verify",
    methods=["GET", "POST"]
)
def verify_driver():

    searched_id = ""
    member = None

    if request.method == "POST":

        searched_id = request.form.get(
            "member_id",
            ""
        ).strip().upper()

        if searched_id:

            member = Member.query.filter_by(
                member_id=searched_id,
                status="Approved",
                is_driver=True
            ).first()

    return render_template(
        "verify_driver.html",
        member=member,
        searched_id=searched_id
    )
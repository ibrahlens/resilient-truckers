from flask import Blueprint, render_template

from models import Program

programs_bp = Blueprint(
    "programs",
    __name__
)


@programs_bp.route("/programs")
def programs():

    programs = Program.query.filter_by(
        status="Published"
    ).order_by(
        Program.display_order.asc()
    ).all()

    return render_template(
        "programs.html",
        programs=programs
    )
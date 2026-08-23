"""Restore payment_method column to donations

Revision ID: restore_payment_method
Revises: 8106a6060b59
Create Date: 2026-08-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "restore_payment_method"
down_revision = "8106a6060b59"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = [
        column["name"]
        for column in inspector.get_columns("donations")
    ]

    if "payment_method" not in columns:
        op.add_column(
            "donations",
            sa.Column(
                "payment_method",
                sa.String(length=50),
                nullable=True,
                server_default="Manual"
            )
        )


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = [
        column["name"]
        for column in inspector.get_columns("donations")
    ]

    if "payment_method" in columns:
        op.drop_column("donations", "payment_method")
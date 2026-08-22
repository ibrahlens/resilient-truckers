"""Add Daraja payment fields

Revision ID: 855d34d66675
Revises:
Create Date: 2026-07-21 14:08:46.819030
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = "855d34d66675"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("donations") as batch_op:

        batch_op.add_column(
            sa.Column("merchant_request_id", sa.String(100), nullable=True)
        )

        batch_op.add_column(
            sa.Column("checkout_request_id", sa.String(100), nullable=True)
        )

        batch_op.add_column(
            sa.Column("mpesa_receipt_number", sa.String(50), nullable=True)
        )

        batch_op.add_column(
            sa.Column("transaction_date", sa.String(30), nullable=True)
        )

        batch_op.add_column(
            sa.Column("result_code", sa.Integer(), nullable=True)
        )

        batch_op.add_column(
            sa.Column("result_description", sa.String(255), nullable=True)
        )

        batch_op.create_unique_constraint(
            "uq_donations_checkout_request_id",
            ["checkout_request_id"]
        )

        batch_op.create_unique_constraint(
            "uq_donations_mpesa_receipt_number",
            ["mpesa_receipt_number"]
        )


def downgrade():

    with op.batch_alter_table("donations") as batch_op:

        batch_op.drop_constraint(
            "uq_donations_mpesa_receipt_number",
            type_="unique"
        )

        batch_op.drop_constraint(
            "uq_donations_checkout_request_id",
            type_="unique"
        )

        batch_op.drop_column("result_description")

        batch_op.drop_column("result_code")

        batch_op.drop_column("transaction_date")

        batch_op.drop_column("mpesa_receipt_number")

        batch_op.drop_column("checkout_request_id")

        batch_op.drop_column("merchant_request_id")
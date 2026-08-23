"""Add WhatsApp link column

Revision ID: 8106a6060b59
Revises: 8e9a056fb428
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8106a6060b59"
down_revision = "8e9a056fb428"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "site_settings",
        sa.Column("whatsapp_link", sa.String(length=255), nullable=True)
    )


def downgrade():
    op.drop_column("site_settings", "whatsapp_link")
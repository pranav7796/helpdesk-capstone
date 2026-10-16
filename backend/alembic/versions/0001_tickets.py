"""Create the support ticket lifecycle schema."""
from alembic import op
import sqlalchemy as sa

revision = "0001_tickets"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("tickets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("subject", sa.String(180), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requester", sa.String(120), nullable=False),
        sa.Column("assignee", sa.String(120), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("priority", sa.String(10), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("status IN ('OPEN','IN_PROGRESS','RESOLVED')", name="ticket_status"),
        sa.CheckConstraint("priority IN ('LOW','MEDIUM','HIGH','URGENT')", name="ticket_priority"),
    )
    op.create_index("ix_tickets_status", "tickets", ["status"])

def downgrade():
    op.drop_index("ix_tickets_status", table_name="tickets")
    op.drop_table("tickets")

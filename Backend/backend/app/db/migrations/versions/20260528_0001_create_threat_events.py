"""create threat events

Revision ID: 20260528_0001
Revises:
Create Date: 2026-05-28
"""

from alembic import op
import sqlalchemy as sa


revision = "20260528_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "threat_events",
        sa.Column("session_id", sa.String(length=128), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("decision", sa.String(length=16), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("signals", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_threat_events_category"), "threat_events", ["category"], unique=False)
    op.create_index(op.f("ix_threat_events_decision"), "threat_events", ["decision"], unique=False)
    op.create_index(op.f("ix_threat_events_id"), "threat_events", ["id"], unique=False)
    op.create_index(op.f("ix_threat_events_risk_score"), "threat_events", ["risk_score"], unique=False)
    op.create_index(op.f("ix_threat_events_session_id"), "threat_events", ["session_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_threat_events_session_id"), table_name="threat_events")
    op.drop_index(op.f("ix_threat_events_risk_score"), table_name="threat_events")
    op.drop_index(op.f("ix_threat_events_id"), table_name="threat_events")
    op.drop_index(op.f("ix_threat_events_decision"), table_name="threat_events")
    op.drop_index(op.f("ix_threat_events_category"), table_name="threat_events")
    op.drop_table("threat_events")

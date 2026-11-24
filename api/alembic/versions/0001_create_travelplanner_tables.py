"""Create the five TravelPlanner tables."""
from alembic import op
import sqlalchemy as sa

revision = "0001_travelplanner"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "destinations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )
    op.create_index("ix_destinations_id", "destinations", ["id"])

    op.create_table(
        "trips",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(150), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("budget", sa.Numeric(10, 2), nullable=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("destination_id", sa.Integer(), sa.ForeignKey("destinations.id"), nullable=False),
    )
    op.create_index("ix_trips_id", "trips", ["id"])

    op.create_table(
        "trip_days",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("trip_id", sa.Integer(), sa.ForeignKey("trips.id", ondelete="CASCADE"), nullable=False),
        sa.Column("day_date", sa.Date(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
    )
    op.create_index("ix_trip_days_id", "trip_days", ["id"])

    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("trip_day_id", sa.Integer(), sa.ForeignKey("trip_days.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("start_time", sa.String(5), nullable=True),
        sa.Column("estimated_cost", sa.Numeric(10, 2), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
    )
    op.create_index("ix_activities_id", "activities", ["id"])

def downgrade():
    op.drop_index("ix_activities_id", table_name="activities")
    op.drop_table("activities")
    op.drop_index("ix_trip_days_id", table_name="trip_days")
    op.drop_table("trip_days")
    op.drop_index("ix_trips_id", table_name="trips")
    op.drop_table("trips")
    op.drop_index("ix_destinations_id", table_name="destinations")
    op.drop_table("destinations")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")

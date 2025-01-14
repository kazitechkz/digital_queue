"""Added final order and queue tables 30 total

Revision ID: 4321be3ae536
Revises: eecc875f981b
Create Date: 2024-12-26 17:25:50.993458

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4321be3ae536"
down_revision: Union[str, None] = "eecc875f981b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "asv_weights",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("weighting_id", sa.Integer(), nullable=False),
        sa.Column("date_weighted", sa.DateTime(), nullable=False),
        sa.Column("car_number", sa.String(length=256), nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=False),
        sa.Column("sender_name", sa.String(length=256), nullable=False),
        sa.Column("receiver_id", sa.Integer(), nullable=False),
        sa.Column("receiver_name", sa.String(length=256), nullable=False),
        sa.Column("sap_mat_number", sa.Integer(), nullable=False),
        sa.Column("system_name", sa.String(length=256), nullable=False),
        sa.Column("gross_weight_kg", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("tare_weight", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("netto_weight", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("invoice_id", sa.Integer(), nullable=True),
        sa.Column("invoice_name", sa.String(length=256), nullable=True),
        sa.Column("invoice_receiver_id", sa.Integer(), nullable=True),
        sa.Column("invoice_receiver_name", sa.String(length=256), nullable=True),
        sa.Column("supply_name", sa.String(length=256), nullable=True),
        sa.Column("card_number", sa.String(length=256), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sap_transfers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("zakaz", sa.String(length=256), nullable=False),
        sa.Column("matnr", sa.String(length=256), nullable=True),
        sa.Column("zavod", sa.String(length=256), nullable=True),
        sa.Column("sklad", sa.String(length=256), nullable=True),
        sa.Column("quan", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("tr_nr", sa.String(length=256), nullable=True),
        sa.Column("date_weighted", sa.Date(), nullable=True),
        sa.Column("time_weighted", sa.Time(), nullable=True),
        sa.Column("status", sa.String(length=256), nullable=True),
        sa.Column("dlvr", sa.String(length=256), nullable=True),
        sa.Column("text", sa.String(length=256), nullable=True),
        sa.Column("date_transfer", sa.Date(), nullable=True),
        sa.Column("time_transfer", sa.Time(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "operations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("value", sa.String(length=256), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column("role_value", sa.String(length=256), nullable=False),
        sa.Column("role_keycloak_value", sa.String(length=256), nullable=True),
        sa.Column("is_first", sa.Boolean(), nullable=False),
        sa.Column("is_last", sa.Boolean(), nullable=False),
        sa.Column("prev_id", sa.Integer(), nullable=True),
        sa.Column("next_id", sa.Integer(), nullable=True),
        sa.Column("can_cancel", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["next_id"], ["operations.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["prev_id"], ["operations.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["role_id"], ["roles.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_operations_role_keycloak_value"),
        "operations",
        ["role_keycloak_value"],
        unique=False,
    )
    op.create_index(
        op.f("ix_operations_role_value"), "operations", ["role_value"], unique=False
    )
    op.create_index(op.f("ix_operations_value"), "operations", ["value"], unique=True)
    op.create_table(
        "verified_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("iin", sa.String(length=256), nullable=True),
        sa.Column("sid", sa.String(length=256), nullable=True),
        sa.Column("verified_at", sa.DateTime(), nullable=True),
        sa.Column("will_act_at", sa.DateTime(), nullable=True),
        sa.Column("is_waiting_for_response", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("is_rejected", sa.Boolean(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("response", sa.Text(), nullable=True),
        sa.Column("verified_by", sa.String(length=256), nullable=True),
        sa.Column("verified_by_sid", sa.String(length=256), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], onupdate="cascade", ondelete="set null"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_verified_users_iin"), "verified_users", ["iin"], unique=False
    )
    op.create_index(
        op.f("ix_verified_users_sid"), "verified_users", ["sid"], unique=False
    )
    op.create_index(
        op.f("ix_verified_users_verified_by"),
        "verified_users",
        ["verified_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_verified_users_verified_by_sid"),
        "verified_users",
        ["verified_by_sid"],
        unique=False,
    )
    op.create_table(
        "employee_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("organization_full_name", sa.String(length=256), nullable=True),
        sa.Column("organization_bin", sa.String(length=256), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.Column("owner_name", sa.String(length=256), nullable=False),
        sa.Column("owner_sid", sa.String(length=256), nullable=True),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("employee_name", sa.String(length=256), nullable=False),
        sa.Column("employee_email", sa.String(length=256), nullable=False),
        sa.Column("employee_sid", sa.String(length=256), nullable=True),
        sa.Column("status", sa.Integer(), nullable=True),
        sa.Column("requested_at", sa.DateTime(), nullable=False),
        sa.Column("decided_at", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_employee_requests_employee_sid"),
        "employee_requests",
        ["employee_sid"],
        unique=False,
    )
    op.create_index(
        op.f("ix_employee_requests_owner_sid"),
        "employee_requests",
        ["owner_sid"],
        unique=False,
    )
    op.create_table(
        "workshop_schedules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workshop_id", sa.Integer(), nullable=True),
        sa.Column("workshop_sap_id", sa.String(length=256), nullable=False),
        sa.Column("date_start", sa.Date(), nullable=False),
        sa.Column("date_end", sa.Date(), nullable=False),
        sa.Column("start_at", sa.Time(), nullable=False),
        sa.Column("end_at", sa.Time(), nullable=False),
        sa.Column("car_service_min", sa.Integer(), nullable=False),
        sa.Column("break_between_service_min", sa.Integer(), nullable=False),
        sa.Column("machine_at_one_time", sa.Integer(), nullable=False),
        sa.Column("can_earlier_come", sa.Integer(), nullable=False),
        sa.Column("can_late_come", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["workshop_id"], ["workshops.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_workshop_schedules_workshop_sap_id"),
        "workshop_schedules",
        ["workshop_sap_id"],
        unique=False,
    )
    op.create_table(
        "base_weights",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=True),
        sa.Column("car_number", sa.String(length=256), nullable=False),
        sa.Column("vehicle_tara_kg", sa.Integer(), nullable=False),
        sa.Column("measured_at", sa.DateTime(), nullable=False),
        sa.Column("measured_to", sa.DateTime(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["vehicle_id"], ["vehicles.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_base_weights_car_number"), "base_weights", ["car_number"], unique=False
    )
    op.create_table(
        "organization_employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("bin", sa.String(length=256), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("sid", sa.String(length=256), nullable=True),
        sa.Column("request_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["request_id"],
            ["employee_requests.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_organization_employees_bin"),
        "organization_employees",
        ["bin"],
        unique=False,
    )
    op.create_index(
        op.f("ix_organization_employees_sid"),
        "organization_employees",
        ["sid"],
        unique=False,
    )
    op.create_table(
        "payment_returns",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("zakaz", sa.String(length=256), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.Column("owner_name", sa.String(length=256), nullable=False),
        sa.Column("owner_iin", sa.String(length=256), nullable=False),
        sa.Column("owner_sid", sa.String(length=256), nullable=True),
        sa.Column("status", sa.Integer(), nullable=True),
        sa.Column("comment", sa.String(length=256), nullable=True),
        sa.Column("decided_by_name", sa.String(length=256), nullable=True),
        sa.Column("decided_by_sid", sa.String(length=256), nullable=True),
        sa.Column("decided_id", sa.Integer(), nullable=True),
        sa.Column("cancel_reason", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["decided_id"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["order_id"], ["orders.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_payment_returns_owner_iin"),
        "payment_returns",
        ["owner_iin"],
        unique=False,
    )
    op.create_index(
        op.f("ix_payment_returns_owner_name"),
        "payment_returns",
        ["owner_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_payment_returns_owner_sid"),
        "payment_returns",
        ["owner_sid"],
        unique=False,
    )
    op.create_index(
        op.f("ix_payment_returns_zakaz"), "payment_returns", ["zakaz"], unique=False
    )
    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("zakaz", sa.String(length=256), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.Column("owner_name", sa.String(length=256), nullable=False),
        sa.Column("owner_iin", sa.String(length=256), nullable=False),
        sa.Column("owner_sid", sa.String(length=256), nullable=True),
        sa.Column("driver_id", sa.Integer(), nullable=True),
        sa.Column("driver_name", sa.String(length=256), nullable=False),
        sa.Column("driver_iin", sa.String(length=256), nullable=False),
        sa.Column("driver_sid", sa.String(length=256), nullable=True),
        sa.Column("organization_id", sa.Integer(), nullable=True),
        sa.Column("organization_full_name", sa.String(length=256), nullable=True),
        sa.Column("organization_bin", sa.String(length=256), nullable=True),
        sa.Column("vehicle_id", sa.Integer(), nullable=True),
        sa.Column("vehicle_info", sa.Text(), nullable=False),
        sa.Column("trailer_id", sa.Integer(), nullable=True),
        sa.Column("trailer_info", sa.Text(), nullable=True),
        sa.Column("car_number", sa.String(length=256), nullable=True),
        sa.Column("workshop_schedule_id", sa.Integer(), nullable=True),
        sa.Column("current_operation_id", sa.Integer(), nullable=True),
        sa.Column("current_operation_name", sa.String(length=256), nullable=True),
        sa.Column("current_operation_value", sa.String(length=256), nullable=True),
        sa.Column("start_at", sa.DateTime(), nullable=False),
        sa.Column("end_at", sa.DateTime(), nullable=False),
        sa.Column("rescheduled_start_at", sa.DateTime(), nullable=True),
        sa.Column("rescheduled_end_at", sa.DateTime(), nullable=True),
        sa.Column("loading_volume", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "loading_volume_kg",
            sa.Integer(),
            sa.Computed(
                "(loading_volume * 1000)::INTEGER",
            ),
            nullable=False,
        ),
        sa.Column("vehicle_tara", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("vehicle_netto", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("vehicle_brutto", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "vehicle_tara_kg",
            sa.Integer(),
            sa.Computed(
                "(vehicle_tara * 1000)::INTEGER",
            ),
            nullable=False,
        ),
        sa.Column(
            "vehicle_netto_kg",
            sa.Integer(),
            sa.Computed(
                "(vehicle_netto * 1000)::INTEGER",
            ),
            nullable=False,
        ),
        sa.Column(
            "vehicle_brutto_kg",
            sa.Integer(),
            sa.Computed(
                "(vehicle_brutto * 1000)::INTEGER",
            ),
            nullable=False,
        ),
        sa.Column("responsible_id", sa.Integer(), nullable=True),
        sa.Column("responsible_name", sa.String(length=256), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False),
        sa.Column("is_canceled", sa.Boolean(), nullable=False),
        sa.Column("is_executed", sa.Boolean(), nullable=False),
        sa.Column("executed_at", sa.DateTime(), nullable=True),
        sa.Column("canceled_by", sa.Integer(), nullable=True),
        sa.Column("canceled_by_name", sa.String(length=256), nullable=True),
        sa.Column("canceled_by_sid", sa.String(length=256), nullable=True),
        sa.Column("cancel_reason", sa.Text(), nullable=True),
        sa.Column("canceled_at", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["canceled_by"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["current_operation_id"],
            ["operations.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["driver_id"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["order_id"], ["orders.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["responsible_id"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["trailer_id"], ["vehicles.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["vehicle_id"], ["vehicles.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["workshop_schedule_id"],
            ["workshop_schedules.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_schedules_car_number"), "schedules", ["car_number"], unique=False
    )
    op.create_index(
        op.f("ix_schedules_current_operation_name"),
        "schedules",
        ["current_operation_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_schedules_current_operation_value"),
        "schedules",
        ["current_operation_value"],
        unique=False,
    )
    op.create_index(
        op.f("ix_schedules_driver_sid"), "schedules", ["driver_sid"], unique=False
    )
    op.create_index(
        op.f("ix_schedules_owner_iin"), "schedules", ["owner_iin"], unique=False
    )
    op.create_index(
        op.f("ix_schedules_owner_name"), "schedules", ["owner_name"], unique=False
    )
    op.create_index(
        op.f("ix_schedules_owner_sid"), "schedules", ["owner_sid"], unique=False
    )
    op.create_index(op.f("ix_schedules_zakaz"), "schedules", ["zakaz"], unique=False)
    op.create_table(
        "verified_vehicles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=True),
        sa.Column("car_number", sa.String(length=256), nullable=True),
        sa.Column("verified_at", sa.DateTime(), nullable=True),
        sa.Column("will_act_at", sa.DateTime(), nullable=True),
        sa.Column("is_waiting_for_response", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("is_rejected", sa.Boolean(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("response", sa.Text(), nullable=True),
        sa.Column("verified_by", sa.String(length=256), nullable=True),
        sa.Column("verified_by_sid", sa.String(length=256), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["vehicle_id"], ["vehicles.id"], onupdate="cascade", ondelete="set null"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_verified_vehicles_car_number"),
        "verified_vehicles",
        ["car_number"],
        unique=False,
    )
    op.create_index(
        op.f("ix_verified_vehicles_verified_by"),
        "verified_vehicles",
        ["verified_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_verified_vehicles_verified_by_sid"),
        "verified_vehicles",
        ["verified_by_sid"],
        unique=False,
    )
    op.create_table(
        "schedule_histories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("schedule_id", sa.Integer(), nullable=True),
        sa.Column("operation_id", sa.Integer(), nullable=True),
        sa.Column("responsible_id", sa.Integer(), nullable=True),
        sa.Column("responsible_name", sa.String(length=256), nullable=True),
        sa.Column("responsible_iin", sa.String(length=256), nullable=True),
        sa.Column("is_passed", sa.Boolean(), nullable=True),
        sa.Column("start_at", sa.DateTime(), nullable=True),
        sa.Column("end_at", sa.DateTime(), nullable=True),
        sa.Column("canceled_at", sa.DateTime(), nullable=True),
        sa.Column("cancel_reason", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["operation_id"], ["operations.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["responsible_id"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["schedule_id"], ["schedules.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "act_weights",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("history_id", sa.Integer(), nullable=True),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("zakaz", sa.String(length=256), nullable=True),
        sa.Column("vehicle_id", sa.Integer(), nullable=True),
        sa.Column("vehicle_info", sa.Text(), nullable=False),
        sa.Column("trailer_id", sa.Integer(), nullable=True),
        sa.Column("trailer_info", sa.Text(), nullable=True),
        sa.Column("responsible_id", sa.Integer(), nullable=True),
        sa.Column("responsible_name", sa.String(length=256), nullable=True),
        sa.Column("responsible_iin", sa.String(length=256), nullable=True),
        sa.Column("asvu_id", sa.Integer(), nullable=True),
        sa.Column("vehicle_tara", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("vehicle_netto", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("vehicle_brutto", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "vehicle_tara_kg",
            sa.Integer(),
            sa.Computed(
                "(vehicle_tara * 1000)::INTEGER",
            ),
            nullable=False,
        ),
        sa.Column(
            "vehicle_netto_kg",
            sa.Integer(),
            sa.Computed(
                "(vehicle_netto * 1000)::INTEGER",
            ),
            nullable=False,
        ),
        sa.Column(
            "vehicle_brutto_kg",
            sa.Integer(),
            sa.Computed(
                "(vehicle_brutto * 1000)::INTEGER",
            ),
            nullable=False,
        ),
        sa.Column("measured_at", sa.DateTime(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["asvu_id"], ["asv_weights.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["history_id"],
            ["schedule_histories.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["order_id"], ["orders.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["responsible_id"], ["users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["trailer_id"], ["vehicles.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["vehicle_id"], ["vehicles.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_act_weights_zakaz"), "act_weights", ["zakaz"], unique=False
    )
    op.add_column("vehicles", sa.Column("vehicle_info", sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("vehicles", "vehicle_info")
    op.drop_index(op.f("ix_act_weights_zakaz"), table_name="act_weights")
    op.drop_table("act_weights")
    op.drop_table("schedule_histories")
    op.drop_index(
        op.f("ix_verified_vehicles_verified_by_sid"), table_name="verified_vehicles"
    )
    op.drop_index(
        op.f("ix_verified_vehicles_verified_by"), table_name="verified_vehicles"
    )
    op.drop_index(
        op.f("ix_verified_vehicles_car_number"), table_name="verified_vehicles"
    )
    op.drop_table("verified_vehicles")
    op.drop_index(op.f("ix_schedules_zakaz"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_owner_sid"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_owner_name"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_owner_iin"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_driver_sid"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_current_operation_value"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_current_operation_name"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_car_number"), table_name="schedules")
    op.drop_table("schedules")
    op.drop_index(op.f("ix_payment_returns_zakaz"), table_name="payment_returns")
    op.drop_index(op.f("ix_payment_returns_owner_sid"), table_name="payment_returns")
    op.drop_index(op.f("ix_payment_returns_owner_name"), table_name="payment_returns")
    op.drop_index(op.f("ix_payment_returns_owner_iin"), table_name="payment_returns")
    op.drop_table("payment_returns")
    op.drop_index(
        op.f("ix_organization_employees_sid"), table_name="organization_employees"
    )
    op.drop_index(
        op.f("ix_organization_employees_bin"), table_name="organization_employees"
    )
    op.drop_table("organization_employees")
    op.drop_index(op.f("ix_base_weights_car_number"), table_name="base_weights")
    op.drop_table("base_weights")
    op.drop_index(
        op.f("ix_workshop_schedules_workshop_sap_id"), table_name="workshop_schedules"
    )
    op.drop_table("workshop_schedules")
    op.drop_index(
        op.f("ix_employee_requests_owner_sid"), table_name="employee_requests"
    )
    op.drop_index(
        op.f("ix_employee_requests_employee_sid"), table_name="employee_requests"
    )
    op.drop_table("employee_requests")
    op.drop_index(
        op.f("ix_verified_users_verified_by_sid"), table_name="verified_users"
    )
    op.drop_index(op.f("ix_verified_users_verified_by"), table_name="verified_users")
    op.drop_index(op.f("ix_verified_users_sid"), table_name="verified_users")
    op.drop_index(op.f("ix_verified_users_iin"), table_name="verified_users")
    op.drop_table("verified_users")
    op.drop_index(op.f("ix_operations_value"), table_name="operations")
    op.drop_index(op.f("ix_operations_role_value"), table_name="operations")
    op.drop_index(op.f("ix_operations_role_keycloak_value"), table_name="operations")
    op.drop_table("operations")
    op.drop_table("sap_transfers")
    op.drop_table("asv_weights")
    # ### end Alembic commands ###

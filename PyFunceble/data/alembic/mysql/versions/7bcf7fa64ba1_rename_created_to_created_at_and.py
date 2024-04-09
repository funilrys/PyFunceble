"""Rename created to created_at and modified_to_modified_at

Revision ID: 7bcf7fa64ba1
Revises: 83ada95132bf
Create Date: 2020-12-08 17:34:59.349943

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# pylint: skip-file

# revision identifiers, used by Alembic.
revision = "7bcf7fa64ba1"
down_revision = "83ada95132bf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "pyfunceble_status", sa.Column("created_at", sa.DateTime(), nullable=False)
    )
    op.add_column(
        "pyfunceble_status", sa.Column("modified_at", sa.DateTime(), nullable=True)
    )
    op.drop_column("pyfunceble_status", "created")
    op.drop_column("pyfunceble_status", "modified")
    op.add_column(
        "pyfunceble_whois_record",
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.add_column(
        "pyfunceble_whois_record",
        sa.Column("modified_at", sa.DateTime(), nullable=True),
    )
    op.drop_column("pyfunceble_whois_record", "created")
    op.drop_column("pyfunceble_whois_record", "modified")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "pyfunceble_whois_record",
        sa.Column("modified", mysql.DATETIME(), nullable=True),
    )
    op.add_column(
        "pyfunceble_whois_record",
        sa.Column("created", mysql.DATETIME(), nullable=False),
    )
    op.drop_column("pyfunceble_whois_record", "modified_at")
    op.drop_column("pyfunceble_whois_record", "created_at")
    op.add_column(
        "pyfunceble_status", sa.Column("modified", mysql.DATETIME(), nullable=True)
    )
    op.add_column(
        "pyfunceble_status", sa.Column("created", mysql.DATETIME(), nullable=False)
    )
    op.drop_column("pyfunceble_status", "modified_at")
    op.drop_column("pyfunceble_status", "created_at")
    op.create_table(
        "pyfunceble_file",
        sa.Column(
            "id", mysql.INTEGER(display_width=11), autoincrement=True, nullable=False
        ),
        sa.Column("created", mysql.DATETIME(), nullable=False),
        sa.Column("modified", mysql.DATETIME(), nullable=True),
        sa.Column("path", mysql.TEXT(collation="utf8mb4_unicode_ci"), nullable=False),
        sa.Column(
            "test_completed",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
        sa.CheckConstraint("`test_completed` in (0,1)", name="CONSTRAINT_1"),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    # ### end Alembic commands ###

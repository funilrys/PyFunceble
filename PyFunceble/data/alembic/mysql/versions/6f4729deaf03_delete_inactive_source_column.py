"""Delete inactive.source column

Revision ID: 6f4729deaf03
Revises: 95dc17ddd729
Create Date: 2021-02-13 12:21:00.493002

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# pylint: skip-file

# revision identifiers, used by Alembic.
revision = "6f4729deaf03"
down_revision = "95dc17ddd729"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("pyfunceble_inactive", "source")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "pyfunceble_inactive",
        sa.Column("source", mysql.TEXT(collation="utf8mb4_unicode_ci"), nullable=False),
    )
    # ### end Alembic commands ###

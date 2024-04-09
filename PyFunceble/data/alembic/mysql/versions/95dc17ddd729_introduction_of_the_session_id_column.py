"""Introduction of the session_id column

Revision ID: 95dc17ddd729
Revises: bef7bcaac3f2
Create Date: 2020-12-23 02:26:21.647125

"""

import sqlalchemy as sa
from alembic import op

# pylint: skip-file

# revision identifiers, used by Alembic.
revision = "95dc17ddd729"
down_revision = "bef7bcaac3f2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "pyfunceble_continue", sa.Column("session_id", sa.Text(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("pyfunceble_continue", "session_id")
    # ### end Alembic commands ###

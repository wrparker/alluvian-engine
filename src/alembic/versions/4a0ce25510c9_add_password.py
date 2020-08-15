"""add password

Revision ID: 4a0ce25510c9
Revises: 5e0e574e99b2
Create Date: 2020-08-14 14:55:28.122804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a0ce25510c9'
down_revision = '5e0e574e99b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('password', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('players', 'password')
    # ### end Alembic commands ###

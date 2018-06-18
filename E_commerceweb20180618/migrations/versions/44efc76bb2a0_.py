"""empty message

Revision ID: 44efc76bb2a0
Revises: baf832320c96
Create Date: 2018-06-17 23:34:16.578874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44efc76bb2a0'
down_revision = 'baf832320c96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('close', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'close', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'close', type_='foreignkey')
    op.drop_column('close', 'author_id')
    # ### end Alembic commands ###

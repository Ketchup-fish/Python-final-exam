"""empty message

Revision ID: baf832320c96
Revises: 5f57cde120f7
Create Date: 2018-06-17 21:52:42.910482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'baf832320c96'
down_revision = '5f57cde120f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('close',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('close_name', sa.Text(), nullable=False),
    sa.Column('img', sa.String(length=16), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('close_price', sa.Integer(), nullable=False),
    sa.Column('num', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('img')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('close')
    # ### end Alembic commands ###

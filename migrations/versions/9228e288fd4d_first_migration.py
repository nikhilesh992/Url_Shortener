"""First Migration

Revision ID: 9228e288fd4d
Revises: 
Create Date: 2021-10-30 14:50:55.725977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9228e288fd4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DATAS',
    sa.Column('id_', sa.Integer(), nullable=False),
    sa.Column('long', sa.String(), nullable=True),
    sa.Column('short', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id_'),
    sa.UniqueConstraint('long'),
    sa.UniqueConstraint('short')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('DATAS')
    # ### end Alembic commands ###
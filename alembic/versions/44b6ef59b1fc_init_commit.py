"""init commit

Revision ID: 44b6ef59b1fc
Revises: faaa478e5b6f
Create Date: 2022-04-03 20:35:15.015040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44b6ef59b1fc'
down_revision = 'faaa478e5b6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_name', sa.String(length=100), nullable=True, comment='账号'))
    op.create_index(op.f('ix_user_user_name'), 'user', ['user_name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_user_name'), table_name='user')
    op.drop_column('user', 'user_name')
    # ### end Alembic commands ###

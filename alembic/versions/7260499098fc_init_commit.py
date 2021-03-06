"""init commit

Revision ID: 7260499098fc
Revises: eae5fa0e6bc7
Create Date: 2022-04-04 14:33:19.680249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7260499098fc'
down_revision = 'eae5fa0e6bc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('org', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('org', sa.Column('status', sa.INTEGER(), server_default=sa.text("'1'"), nullable=True))
    # ### end Alembic commands ###

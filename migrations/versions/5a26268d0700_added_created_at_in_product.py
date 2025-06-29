"""added created_at in Product

Revision ID: 5a26268d0700
Revises: 84875f63f780
Create Date: 2025-06-07 16:18:25.716276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a26268d0700'
down_revision = '84875f63f780'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_product_created_at'), ['created_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_product_created_at'))
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###

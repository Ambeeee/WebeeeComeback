"""Aggiunta descrizione, non so perché non c'era

Revision ID: 8a4fd089fdbd
Revises: d7d29c4be347
Create Date: 2022-10-18 22:17:03.433457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a4fd089fdbd'
down_revision = 'd7d29c4be347'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=120), nullable=True))
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.drop_column('description')

    # ### end Alembic commands ###

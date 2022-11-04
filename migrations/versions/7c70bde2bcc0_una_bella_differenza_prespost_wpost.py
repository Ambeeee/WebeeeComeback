"""Una bella differenza - PresPost, Wpost

Revision ID: 7c70bde2bcc0
Revises: ae35948c8765
Create Date: 2022-11-03 21:52:45.537235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c70bde2bcc0'
down_revision = 'ae35948c8765'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pres_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('slug', sa.String(length=250), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('body1', sa.Text(), nullable=False),
    sa.Column('body2', sa.Text(), nullable=True),
    sa.Column('body3', sa.Text(), nullable=True),
    sa.Column('body4', sa.Text(), nullable=True),
    sa.Column('testimonial', sa.Text(), nullable=True),
    sa.Column('testimonial2', sa.Text(), nullable=True),
    sa.Column('cover', sa.String(length=120), nullable=True),
    sa.Column('image1', sa.String(length=120), nullable=True),
    sa.Column('image2', sa.String(length=120), nullable=True),
    sa.Column('image3', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wpost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('slug', sa.String(length=250), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('body1', sa.Text(), nullable=False),
    sa.Column('testimonial', sa.Text(), nullable=True),
    sa.Column('body2', sa.Text(), nullable=True),
    sa.Column('cover', sa.String(length=120), nullable=True),
    sa.Column('image1', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('post')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cover', sa.VARCHAR(length=120), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('title', sa.VARCHAR(length=120), nullable=False),
    sa.Column('description', sa.VARCHAR(length=120), nullable=True),
    sa.Column('body', sa.TEXT(), nullable=False),
    sa.Column('slug', sa.VARCHAR(length=250), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('wpost')
    op.drop_table('pres_post')
    # ### end Alembic commands ###
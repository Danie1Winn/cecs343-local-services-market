"""Initial migrate

Revision ID: 5d31b5af4a28
Revises: 
Create Date: 2024-11-19 18:33:46.540278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d31b5af4a28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=10), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('workers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_picture', sa.String(length=200), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=10), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('skill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('skill_name', sa.String(length=100), nullable=False),
    sa.Column('experience_level', sa.Integer(), nullable=False),
    sa.Column('worker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['worker_id'], ['workers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('skill')
    op.drop_table('workers')
    op.drop_table('employers')
    # ### end Alembic commands ###
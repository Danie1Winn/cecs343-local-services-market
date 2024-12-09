"""Added zip_code and travel_distance to Worker model

Revision ID: 598db9a1cc69
Revises: 8f74dd688e41
Create Date: 2024-12-02 16:46:06.414319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '598db9a1cc69'
down_revision = '8f74dd688e41'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the 'skill' table exists before attempting to drop it
    conn = op.get_bind()  # Get the current connection
    inspector = sa.inspect(conn)  # Use SQLAlchemy's inspector to list tables
    if 'skill' in inspector.get_table_names():
        op.drop_table('skill')

    # Add the 'zip_code' and 'travel_distance' columns with default values
    with op.batch_alter_table('workers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('zip_code', sa.String(length=10), nullable=False, server_default="00000"))
        batch_op.add_column(sa.Column('travel_distance', sa.Integer(), nullable=False, server_default="10"))

    # Remove the server_default once the columns are populated
    with op.batch_alter_table('workers', schema=None) as batch_op:
        batch_op.alter_column('zip_code', server_default=None)
        batch_op.alter_column('travel_distance', server_default=None)


def downgrade():
    # Drop the 'zip_code' and 'travel_distance' columns
    with op.batch_alter_table('workers', schema=None) as batch_op:
        batch_op.drop_column('travel_distance')
        batch_op.drop_column('zip_code')

    # Recreate the 'skill' table if needed
    op.create_table(
        'skill',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('skill_name', sa.String(length=100), nullable=False),
        sa.Column('experience_level', sa.Integer(), nullable=False),
        sa.Column('worker_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['worker_id'], ['workers.id']),
        sa.PrimaryKeyConstraint('id')
    )

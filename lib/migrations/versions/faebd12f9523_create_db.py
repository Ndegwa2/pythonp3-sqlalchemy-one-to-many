"""create db

Revision ID: faebd12f9523
Revises: 
Create Date: 2023-03-15 13:20:05.247015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faebd12f9523'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the games table
    op.create_table(
        'games',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('genre', sa.String, nullable=False),
        sa.Column('platform', sa.String, nullable=False),
        sa.Column('price', sa.Float, nullable=False),
    )

def downgrade():
    # Drop the games table
    op.drop_table('games')

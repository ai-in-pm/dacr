"""initial

Revision ID: 001
Revises: 
Create Date: 2024-12-22 08:50:46.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create transactions table
    op.create_table(
        'transactions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=36, scale=18), nullable=False),
        sa.Column('sender', sa.String(), nullable=True),
        sa.Column('recipient', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create balances table
    op.create_table(
        'balances',
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=36, scale=18), nullable=False),
        sa.Column('last_updated', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('address')
    )

    # Create reserves table
    op.create_table(
        'reserves',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=36, scale=18), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('reserves')
    op.drop_table('balances')
    op.drop_table('transactions')

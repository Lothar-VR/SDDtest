"""
Initial migration: Create employees table
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create employees table"""
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name=op.f('uq_employees_email'))
    )
    op.create_index(op.f('ix_employees_email'), 'employees', ['email'], unique=True)
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)
    op.create_index(op.f('ix_employees_is_deleted'), 'employees', ['is_deleted'], unique=False)
    op.create_index(op.f('ix_employees_created_at'), 'employees', ['created_at'], unique=False)


def downgrade() -> None:
    """Drop employees table"""
    op.drop_index(op.f('ix_employees_created_at'), table_name='employees')
    op.drop_index(op.f('ix_employees_is_deleted'), table_name='employees')
    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_index(op.f('ix_employees_email'), table_name='employees')
    op.drop_table('employees')

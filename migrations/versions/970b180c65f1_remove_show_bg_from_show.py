"""remove show_bg from Show

Revision ID: 970b180c65f1
Revises: 95c2a2a43813
Create Date: 2025-06-06 23:45:33.887848
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '970b180c65f1'
down_revision = '95c2a2a43813'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_column('Show', 'show_bg')

def downgrade():
    op.add_column('Show', sa.Column('show_bg', sa.String(length=255), nullable=True))

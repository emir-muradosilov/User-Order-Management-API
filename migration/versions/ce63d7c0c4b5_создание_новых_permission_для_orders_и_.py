"""создание новых permission для orders и products

Revision ID: ce63d7c0c4b5
Revises: 86e43abdba06
Create Date: 2026-02-03 17:30:25.955429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce63d7c0c4b5'
down_revision: Union[str, Sequence[str], None] = '86e43abdba06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute( """ INSERT INTO permissions (name) VALUES ('orders:read'), ('orders:write'), ('products:read'), ('products:update') ON CONFLICT (name) DO NOTHING; """ )

    op.execute(""" INSERT INTO role_permissions (role_id, permission_id) SELECT r.id, p.id FROM roles r CROSS JOIN permissions p WHERE r.name = 'admin' ON CONFLICT (role_id, permission_id) DO NOTHING; """)
    op.execute(""" INSERT INTO role_permissions (role_id, permission_id) SELECT r.id, p.id FROM roles r CROSS JOIN permissions p WHERE r.name = 'user' AND p.name IN ('orders:read', 'products:read') ON CONFLICT (role_id, permission_id) DO NOTHING; """)

def downgrade() -> None:
    """Downgrade schema."""
    pass

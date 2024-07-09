"""make timestamps default

Revision ID: d63ff5877d9c
Revises: 5cf53d945859
Create Date: 2024-07-08 19:20:13.062026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel # added

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd63ff5877d9c'
down_revision: Union[str, None] = '5cf53d945859'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('rbac_docs', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_docs', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_keys', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_keys', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_orgs', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_orgs', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_projects', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_projects', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_roles', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_roles', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    op.alter_column('rbac_users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.func.now(), default=sa.func.now())
    


def downgrade() -> None:
    op.alter_column('rbac_docs', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_docs', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_keys', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_keys', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_orgs', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_orgs', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_projects', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_projects', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_roles', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_roles', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    op.alter_column('rbac_users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=None, default=None)
    

"""ids should autogenerate

Revision ID: 07b20d80aa77
Revises: d63ff5877d9c
Create Date: 2024-07-08 19:29:29.251590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel # added
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '07b20d80aa77'
down_revision: Union[str, None] = 'd63ff5877d9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('rbac_resources', 'resource_id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=sa.func.uuid_generate_v4())
    
    op.alter_column('rbac_roles', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=sa.func.uuid_generate_v4())
    
    op.alter_column('rbac_users', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=sa.func.uuid_generate_v4())
    
    op.alter_column('rbac_keys', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=sa.func.uuid_generate_v4())
    
    op.alter_column('rbac_orgs', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=sa.func.uuid_generate_v4())
    
    op.alter_column('rbac_role_resource_associations', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=sa.func.uuid_generate_v4())
    
    op.alter_column('rbac_projects', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=sa.func.uuid_generate_v4())
    
    op.alter_column('rbac_docs', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=sa.func.uuid_generate_v4())
    
def downgrade() -> None:
    op.alter_column('rbac_docs', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=None)
    
    op.alter_column('rbac_projects', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=None)
    
    op.alter_column('rbac_role_resource_associations', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=None)
    
    op.alter_column('rbac_orgs', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=None)
    
    op.alter_column('rbac_keys', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=None)
    
    op.alter_column('rbac_users', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=None)
    
    op.alter_column('rbac_roles', 'id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=None)
    
    op.alter_column('rbac_resources', 'resource_id',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=None)
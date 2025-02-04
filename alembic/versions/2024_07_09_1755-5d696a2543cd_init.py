"""init

Revision ID: 5d696a2543cd
Revises:
Create Date: 2024-07-09 17:55:13.035285

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # added
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "5d696a2543cd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # fmt: off
    # Fundamental entities that can be assigned to roles
    op.execute("create schema rbac")
    op.execute("set search_path to rbac, public, extensions")
    op.create_table('rbac_resources',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False, server_default=sa.func.uuid_generate_v4()),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='rbac'
    )
    op.create_index(op.f('ix_rbac_rbac_resources_name'), 'rbac_resources', ['name'], unique=True, schema='rbac')

    # Bundles up resources and permissions for access by a key
    op.create_table('rbac_roles',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False, server_default=sa.func.uuid_generate_v4()),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('has_read', sa.Boolean(), nullable=False),
    sa.Column('has_write', sa.Boolean(), nullable=False),
    sa.Column('has_delete', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='rbac'
    )
    op.create_index(op.f('ix_rbac_rbac_roles_name'), 'rbac_roles', ['name'], unique=True, schema='rbac')

    # Role-Resource Association: roles can access resources, resources can be accessed by multiple roles
    op.create_table('rbac_role_resource_associations',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False, server_default=sa.func.uuid_generate_v4()),
    sa.Column('role_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('resource_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['rbac.rbac_resources.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['role_id'], ['rbac.rbac_roles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='rbac'
    )
    op.create_index(op.f('ix_rbac_rbac_role_resource_associations_resource_id'), 'rbac_role_resource_associations', ['resource_id'], unique=False, schema='rbac')
    op.create_index(op.f('ix_rbac_rbac_role_resource_associations_role_id'), 'rbac_role_resource_associations', ['role_id'], unique=False, schema='rbac')

    # Entities that can assume roles via keys
    op.create_table('rbac_users',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False, server_default=sa.func.uuid_generate_v4()),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='rbac'
    )

    # Keys allow users to assume roles, multiple users to assume the same role, 
    # or one user to assume different roles
    op.create_table('rbac_keys',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False, server_default=sa.func.uuid_generate_v4()),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('key', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('role_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['rbac.rbac_roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['rbac.rbac_users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='rbac'
    )
    op.create_index(op.f('ix_rbac_rbac_keys_key'), 'rbac_keys', ['key'], unique=True, schema='rbac')
    op.create_index(op.f('ix_rbac_rbac_keys_role_id'), 'rbac_keys', ['role_id'], unique=False, schema='rbac')
    op.create_index(op.f('ix_rbac_rbac_keys_user_id'), 'rbac_keys', ['user_id'], unique=False, schema='rbac')

    # Organizations: Top-level grouping entity with its own resource
    op.create_table('rbac_orgs',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False, server_default=sa.func.uuid_generate_v4()),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('resource_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['rbac.rbac_resources.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('resource_id'),
    schema='rbac'
    )
    op.create_index(op.f('ix_rbac_rbac_orgs_name'), 'rbac_orgs', ['name'], unique=True, schema='rbac')

    # Projects: Organizational sub-units with their own resources
    op.create_table('rbac_projects',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False, server_default=sa.func.uuid_generate_v4()),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('resource_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('organization_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['rbac.rbac_orgs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['resource_id'], ['rbac.rbac_resources.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='rbac'
    )
    op.create_index(op.f('ix_rbac_rbac_projects_name'), 'rbac_projects', ['name'], unique=True, schema='rbac')

    # Documents: Lowest-level entity with JSON data and its own resource
    op.create_table('rbac_docs',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False, server_default=sa.func.uuid_generate_v4()),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('resource_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('project_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['rbac.rbac_projects.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['resource_id'], ['rbac.rbac_resources.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='rbac'
    )
    op.create_index(op.f('ix_rbac_rbac_docs_name'), 'rbac_docs', ['name'], unique=True, schema='rbac')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_rbac_docs_name"), table_name="rbac_docs")
    op.drop_table("rbac_docs")
    op.drop_index(op.f("ix_rbac_projects_name"), table_name="rbac_projects")
    op.drop_table("rbac_projects")
    op.drop_index(
        op.f("ix_rbac_role_resource_associations_role_id"),
        table_name="rbac_role_resource_associations",
    )
    op.drop_index(
        op.f("ix_rbac_role_resource_associations_resource_id"),
        table_name="rbac_role_resource_associations",
    )
    op.drop_table("rbac_role_resource_associations")
    op.drop_index(op.f("ix_rbac_orgs_name"), table_name="rbac_orgs")
    op.drop_table("rbac_orgs")
    op.drop_index(op.f("ix_rbac_keys_user_id"), table_name="rbac_keys")
    op.drop_index(op.f("ix_rbac_keys_role_id"), table_name="rbac_keys")
    op.drop_index(op.f("ix_rbac_keys_key"), table_name="rbac_keys")
    op.drop_table("rbac_keys")
    op.drop_table("rbac_users")
    op.drop_index(op.f("ix_rbac_roles_name"), table_name="rbac_roles")
    op.drop_table("rbac_roles")
    op.drop_index(op.f("ix_rbac_resources_name"), table_name="rbac_resources")
    op.drop_table("rbac_resources")
    op.execute("drop schema rbac")
    # fmt: on
    # ### end Alembic commands ###

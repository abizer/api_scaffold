"""key should autogenerate

Revision ID: 06721081382c
Revises: 07b20d80aa77
Create Date: 2024-07-08 20:00:22.172509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel # added


# revision identifiers, used by Alembic.
revision: str = '06721081382c'
down_revision: Union[str, None] = '07b20d80aa77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.alter_column('rbac_keys', 'key',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=sa.func.uuid_generate_v4())

def downgrade() -> None:
     op.alter_column('rbac_keys', 'key',
               existing_type=sqlmodel.sql.sqltypes.GUID(),
               server_default=None)


import uuid

from pydantic import BaseModel
from .model import Role, RoleTable, ResourceTable, RoleResourceTable
from app.mod.meta.crud import CRUDBase

class RoleCreate(Role):
    pass 

class RoleUpdate(Role):
    pass 

class CRUDRole(CRUDBase[RoleTable, RoleCreate, RoleUpdate]):
    pass

role = CRUDRole(RoleTable)

class ResourceCreate(BaseModel):
    name: str

class ResourceUpdate(BaseModel):
    name: str

class CRUDResource(CRUDBase[ResourceTable, ResourceCreate, ResourceUpdate]):
    pass

resource = CRUDResource(ResourceTable)

class RoleResourceCreate(BaseModel):
    role_id: uuid.UUID
    resource_id: uuid.UUID

class RoleResourceUpdate(BaseModel):
    # not allowed
    pass

class CRUDRoleResource(CRUDBase[RoleResourceTable, RoleResourceCreate, RoleResourceUpdate]):
    pass

role_resource = CRUDRoleResource(RoleResourceTable)
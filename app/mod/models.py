from .rbac.user.model import UserTable, KeyTable
from .rbac.role.model import RoleTable, RoleResourceTable, ResourceTable
from .rbac.ent.model import OrganizationTable, ProjectTable, DocumentTable

_rbac_models = ["UserTable", "KeyTable", "OrganizationTable", "ProjectTable", "DocumentTable", "RoleTable", "RoleResourceTable",]

__all__ = [*_rbac_models]

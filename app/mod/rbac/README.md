# how rbac works

we have:

.user.model (contains UserTable, KeyTable)
.role.model (contains Role, RoleTable, ResourceTable, RoleResourceTable)
.ent.model (contains Organization, Project, Document + Tables)

the broad idea is:

1. a _Key_ lets a _User_ assume a _Role_
2. a _Role_ grants read/write/delete access to a _Resource_ identified by a `resource_id`
3. a _Resource_ is an _Organization_, _Project_, or _Document_ (or more generally, an entity, of which org/prj/doc are NamedEntities, but the general form is difficult to express in SQLAlchemy).
4. In order to create a _Resource_, you must first create a new resource_id, then use that resource_id to create the resource, which all take _resource_id_ as a foreign key.
5. _Documents_ belong to _Projects_ which belong to _Organizations_ 
6. Right now, to keep the overall structure simpler, child resources inherit the _resource_id_ from their parent. Only organizations are created with unique resource_ids. 
create table "public"."alembic_version" (
    "version_num" character varying(32) not null
);


create table "public"."rbac_docs" (
    "id" uuid not null default uuid_generate_v4(),
    "created_at" timestamp with time zone default now(),
    "updated_at" timestamp with time zone default now(),
    "name" character varying not null,
    "description" character varying,
    "resource_id" uuid not null,
    "project_id" uuid not null,
    "data" jsonb
);


create table "public"."rbac_keys" (
    "id" uuid not null default uuid_generate_v4(),
    "created_at" timestamp with time zone default now(),
    "updated_at" timestamp with time zone default now(),
    "key" uuid not null default uuid_generate_v4(),
    "is_active" boolean not null,
    "user_id" uuid not null,
    "role_id" uuid not null
);


create table "public"."rbac_orgs" (
    "id" uuid not null default uuid_generate_v4(),
    "created_at" timestamp with time zone default now(),
    "updated_at" timestamp with time zone default now(),
    "name" character varying not null,
    "description" character varying,
    "resource_id" uuid not null
);


create table "public"."rbac_projects" (
    "id" uuid not null default uuid_generate_v4(),
    "created_at" timestamp with time zone default now(),
    "updated_at" timestamp with time zone default now(),
    "name" character varying not null,
    "description" character varying,
    "resource_id" uuid not null,
    "organization_id" uuid not null
);


create table "public"."rbac_resources" (
    "name" character varying not null,
    "resource_id" uuid not null default uuid_generate_v4()
);


create table "public"."rbac_role_resource_associations" (
    "id" uuid not null default uuid_generate_v4(),
    "role_id" uuid not null,
    "resource_id" uuid not null
);


create table "public"."rbac_roles" (
    "id" uuid not null default uuid_generate_v4(),
    "created_at" timestamp with time zone default now(),
    "updated_at" timestamp with time zone default now(),
    "name" character varying not null,
    "description" character varying,
    "has_read" boolean not null,
    "has_write" boolean not null,
    "has_delete" boolean not null
);


create table "public"."rbac_users" (
    "id" uuid not null default uuid_generate_v4(),
    "created_at" timestamp with time zone default now(),
    "updated_at" timestamp with time zone default now(),
    "email" character varying not null
);


CREATE UNIQUE INDEX alembic_version_pkc ON public.alembic_version USING btree (version_num);

CREATE INDEX ix_rbac_docs_id ON public.rbac_docs USING btree (id);

CREATE UNIQUE INDEX ix_rbac_docs_name ON public.rbac_docs USING btree (name);

CREATE INDEX ix_rbac_keys_id ON public.rbac_keys USING btree (id);

CREATE UNIQUE INDEX ix_rbac_keys_key ON public.rbac_keys USING btree (key);

CREATE INDEX ix_rbac_orgs_id ON public.rbac_orgs USING btree (id);

CREATE UNIQUE INDEX ix_rbac_orgs_name ON public.rbac_orgs USING btree (name);

CREATE INDEX ix_rbac_projects_id ON public.rbac_projects USING btree (id);

CREATE UNIQUE INDEX ix_rbac_projects_name ON public.rbac_projects USING btree (name);

CREATE UNIQUE INDEX ix_rbac_resources_name ON public.rbac_resources USING btree (name);

CREATE INDEX ix_rbac_role_resource_associations_id ON public.rbac_role_resource_associations USING btree (id);

CREATE INDEX ix_rbac_role_resource_associations_resource_id ON public.rbac_role_resource_associations USING btree (resource_id);

CREATE INDEX ix_rbac_role_resource_associations_role_id ON public.rbac_role_resource_associations USING btree (role_id);

CREATE INDEX ix_rbac_roles_id ON public.rbac_roles USING btree (id);

CREATE UNIQUE INDEX ix_rbac_roles_name ON public.rbac_roles USING btree (name);

CREATE INDEX ix_rbac_users_id ON public.rbac_users USING btree (id);

CREATE UNIQUE INDEX rbac_docs_pkey ON public.rbac_docs USING btree (id);

CREATE UNIQUE INDEX rbac_docs_resource_id_key ON public.rbac_docs USING btree (resource_id);

CREATE UNIQUE INDEX rbac_keys_pkey ON public.rbac_keys USING btree (id);

CREATE UNIQUE INDEX rbac_orgs_pkey ON public.rbac_orgs USING btree (id);

CREATE UNIQUE INDEX rbac_orgs_resource_id_key ON public.rbac_orgs USING btree (resource_id);

CREATE UNIQUE INDEX rbac_projects_pkey ON public.rbac_projects USING btree (id);

CREATE UNIQUE INDEX rbac_projects_resource_id_key ON public.rbac_projects USING btree (resource_id);

CREATE UNIQUE INDEX rbac_resources_pkey ON public.rbac_resources USING btree (resource_id);

CREATE UNIQUE INDEX rbac_role_resource_associations_pkey ON public.rbac_role_resource_associations USING btree (id);

CREATE UNIQUE INDEX rbac_roles_pkey ON public.rbac_roles USING btree (id);

CREATE UNIQUE INDEX rbac_users_email_key ON public.rbac_users USING btree (email);

CREATE UNIQUE INDEX rbac_users_pkey ON public.rbac_users USING btree (id);

alter table "public"."alembic_version" add constraint "alembic_version_pkc" PRIMARY KEY using index "alembic_version_pkc";

alter table "public"."rbac_docs" add constraint "rbac_docs_pkey" PRIMARY KEY using index "rbac_docs_pkey";

alter table "public"."rbac_keys" add constraint "rbac_keys_pkey" PRIMARY KEY using index "rbac_keys_pkey";

alter table "public"."rbac_orgs" add constraint "rbac_orgs_pkey" PRIMARY KEY using index "rbac_orgs_pkey";

alter table "public"."rbac_projects" add constraint "rbac_projects_pkey" PRIMARY KEY using index "rbac_projects_pkey";

alter table "public"."rbac_resources" add constraint "rbac_resources_pkey" PRIMARY KEY using index "rbac_resources_pkey";

alter table "public"."rbac_role_resource_associations" add constraint "rbac_role_resource_associations_pkey" PRIMARY KEY using index "rbac_role_resource_associations_pkey";

alter table "public"."rbac_roles" add constraint "rbac_roles_pkey" PRIMARY KEY using index "rbac_roles_pkey";

alter table "public"."rbac_users" add constraint "rbac_users_pkey" PRIMARY KEY using index "rbac_users_pkey";

alter table "public"."rbac_docs" add constraint "rbac_docs_project_id_fkey" FOREIGN KEY (project_id) REFERENCES rbac_projects(id) ON DELETE CASCADE not valid;

alter table "public"."rbac_docs" validate constraint "rbac_docs_project_id_fkey";

alter table "public"."rbac_docs" add constraint "rbac_docs_resource_id_fkey" FOREIGN KEY (resource_id) REFERENCES rbac_resources(resource_id) ON DELETE CASCADE not valid;

alter table "public"."rbac_docs" validate constraint "rbac_docs_resource_id_fkey";

alter table "public"."rbac_docs" add constraint "rbac_docs_resource_id_key" UNIQUE using index "rbac_docs_resource_id_key";

alter table "public"."rbac_keys" add constraint "rbac_keys_role_id_fkey" FOREIGN KEY (role_id) REFERENCES rbac_roles(id) ON DELETE CASCADE not valid;

alter table "public"."rbac_keys" validate constraint "rbac_keys_role_id_fkey";

alter table "public"."rbac_keys" add constraint "rbac_keys_user_id_fkey" FOREIGN KEY (user_id) REFERENCES rbac_users(id) ON DELETE CASCADE not valid;

alter table "public"."rbac_keys" validate constraint "rbac_keys_user_id_fkey";

alter table "public"."rbac_orgs" add constraint "rbac_orgs_resource_id_fkey" FOREIGN KEY (resource_id) REFERENCES rbac_resources(resource_id) ON DELETE CASCADE not valid;

alter table "public"."rbac_orgs" validate constraint "rbac_orgs_resource_id_fkey";

alter table "public"."rbac_orgs" add constraint "rbac_orgs_resource_id_key" UNIQUE using index "rbac_orgs_resource_id_key";

alter table "public"."rbac_projects" add constraint "rbac_projects_organization_id_fkey" FOREIGN KEY (organization_id) REFERENCES rbac_orgs(id) ON DELETE CASCADE not valid;

alter table "public"."rbac_projects" validate constraint "rbac_projects_organization_id_fkey";

alter table "public"."rbac_projects" add constraint "rbac_projects_resource_id_fkey" FOREIGN KEY (resource_id) REFERENCES rbac_resources(resource_id) ON DELETE CASCADE not valid;

alter table "public"."rbac_projects" validate constraint "rbac_projects_resource_id_fkey";

alter table "public"."rbac_projects" add constraint "rbac_projects_resource_id_key" UNIQUE using index "rbac_projects_resource_id_key";

alter table "public"."rbac_role_resource_associations" add constraint "rbac_role_resource_associations_resource_id_fkey" FOREIGN KEY (resource_id) REFERENCES rbac_resources(resource_id) ON DELETE CASCADE not valid;

alter table "public"."rbac_role_resource_associations" validate constraint "rbac_role_resource_associations_resource_id_fkey";

alter table "public"."rbac_role_resource_associations" add constraint "rbac_role_resource_associations_role_id_fkey" FOREIGN KEY (role_id) REFERENCES rbac_roles(id) ON DELETE CASCADE not valid;

alter table "public"."rbac_role_resource_associations" validate constraint "rbac_role_resource_associations_role_id_fkey";

alter table "public"."rbac_users" add constraint "rbac_users_email_key" UNIQUE using index "rbac_users_email_key";

grant delete on table "public"."alembic_version" to "anon";

grant insert on table "public"."alembic_version" to "anon";

grant references on table "public"."alembic_version" to "anon";

grant select on table "public"."alembic_version" to "anon";

grant trigger on table "public"."alembic_version" to "anon";

grant truncate on table "public"."alembic_version" to "anon";

grant update on table "public"."alembic_version" to "anon";

grant delete on table "public"."alembic_version" to "authenticated";

grant insert on table "public"."alembic_version" to "authenticated";

grant references on table "public"."alembic_version" to "authenticated";

grant select on table "public"."alembic_version" to "authenticated";

grant trigger on table "public"."alembic_version" to "authenticated";

grant truncate on table "public"."alembic_version" to "authenticated";

grant update on table "public"."alembic_version" to "authenticated";

grant delete on table "public"."alembic_version" to "service_role";

grant insert on table "public"."alembic_version" to "service_role";

grant references on table "public"."alembic_version" to "service_role";

grant select on table "public"."alembic_version" to "service_role";

grant trigger on table "public"."alembic_version" to "service_role";

grant truncate on table "public"."alembic_version" to "service_role";

grant update on table "public"."alembic_version" to "service_role";

grant delete on table "public"."rbac_docs" to "anon";

grant insert on table "public"."rbac_docs" to "anon";

grant references on table "public"."rbac_docs" to "anon";

grant select on table "public"."rbac_docs" to "anon";

grant trigger on table "public"."rbac_docs" to "anon";

grant truncate on table "public"."rbac_docs" to "anon";

grant update on table "public"."rbac_docs" to "anon";

grant delete on table "public"."rbac_docs" to "authenticated";

grant insert on table "public"."rbac_docs" to "authenticated";

grant references on table "public"."rbac_docs" to "authenticated";

grant select on table "public"."rbac_docs" to "authenticated";

grant trigger on table "public"."rbac_docs" to "authenticated";

grant truncate on table "public"."rbac_docs" to "authenticated";

grant update on table "public"."rbac_docs" to "authenticated";

grant delete on table "public"."rbac_docs" to "service_role";

grant insert on table "public"."rbac_docs" to "service_role";

grant references on table "public"."rbac_docs" to "service_role";

grant select on table "public"."rbac_docs" to "service_role";

grant trigger on table "public"."rbac_docs" to "service_role";

grant truncate on table "public"."rbac_docs" to "service_role";

grant update on table "public"."rbac_docs" to "service_role";

grant delete on table "public"."rbac_keys" to "anon";

grant insert on table "public"."rbac_keys" to "anon";

grant references on table "public"."rbac_keys" to "anon";

grant select on table "public"."rbac_keys" to "anon";

grant trigger on table "public"."rbac_keys" to "anon";

grant truncate on table "public"."rbac_keys" to "anon";

grant update on table "public"."rbac_keys" to "anon";

grant delete on table "public"."rbac_keys" to "authenticated";

grant insert on table "public"."rbac_keys" to "authenticated";

grant references on table "public"."rbac_keys" to "authenticated";

grant select on table "public"."rbac_keys" to "authenticated";

grant trigger on table "public"."rbac_keys" to "authenticated";

grant truncate on table "public"."rbac_keys" to "authenticated";

grant update on table "public"."rbac_keys" to "authenticated";

grant delete on table "public"."rbac_keys" to "service_role";

grant insert on table "public"."rbac_keys" to "service_role";

grant references on table "public"."rbac_keys" to "service_role";

grant select on table "public"."rbac_keys" to "service_role";

grant trigger on table "public"."rbac_keys" to "service_role";

grant truncate on table "public"."rbac_keys" to "service_role";

grant update on table "public"."rbac_keys" to "service_role";

grant delete on table "public"."rbac_orgs" to "anon";

grant insert on table "public"."rbac_orgs" to "anon";

grant references on table "public"."rbac_orgs" to "anon";

grant select on table "public"."rbac_orgs" to "anon";

grant trigger on table "public"."rbac_orgs" to "anon";

grant truncate on table "public"."rbac_orgs" to "anon";

grant update on table "public"."rbac_orgs" to "anon";

grant delete on table "public"."rbac_orgs" to "authenticated";

grant insert on table "public"."rbac_orgs" to "authenticated";

grant references on table "public"."rbac_orgs" to "authenticated";

grant select on table "public"."rbac_orgs" to "authenticated";

grant trigger on table "public"."rbac_orgs" to "authenticated";

grant truncate on table "public"."rbac_orgs" to "authenticated";

grant update on table "public"."rbac_orgs" to "authenticated";

grant delete on table "public"."rbac_orgs" to "service_role";

grant insert on table "public"."rbac_orgs" to "service_role";

grant references on table "public"."rbac_orgs" to "service_role";

grant select on table "public"."rbac_orgs" to "service_role";

grant trigger on table "public"."rbac_orgs" to "service_role";

grant truncate on table "public"."rbac_orgs" to "service_role";

grant update on table "public"."rbac_orgs" to "service_role";

grant delete on table "public"."rbac_projects" to "anon";

grant insert on table "public"."rbac_projects" to "anon";

grant references on table "public"."rbac_projects" to "anon";

grant select on table "public"."rbac_projects" to "anon";

grant trigger on table "public"."rbac_projects" to "anon";

grant truncate on table "public"."rbac_projects" to "anon";

grant update on table "public"."rbac_projects" to "anon";

grant delete on table "public"."rbac_projects" to "authenticated";

grant insert on table "public"."rbac_projects" to "authenticated";

grant references on table "public"."rbac_projects" to "authenticated";

grant select on table "public"."rbac_projects" to "authenticated";

grant trigger on table "public"."rbac_projects" to "authenticated";

grant truncate on table "public"."rbac_projects" to "authenticated";

grant update on table "public"."rbac_projects" to "authenticated";

grant delete on table "public"."rbac_projects" to "service_role";

grant insert on table "public"."rbac_projects" to "service_role";

grant references on table "public"."rbac_projects" to "service_role";

grant select on table "public"."rbac_projects" to "service_role";

grant trigger on table "public"."rbac_projects" to "service_role";

grant truncate on table "public"."rbac_projects" to "service_role";

grant update on table "public"."rbac_projects" to "service_role";

grant delete on table "public"."rbac_resources" to "anon";

grant insert on table "public"."rbac_resources" to "anon";

grant references on table "public"."rbac_resources" to "anon";

grant select on table "public"."rbac_resources" to "anon";

grant trigger on table "public"."rbac_resources" to "anon";

grant truncate on table "public"."rbac_resources" to "anon";

grant update on table "public"."rbac_resources" to "anon";

grant delete on table "public"."rbac_resources" to "authenticated";

grant insert on table "public"."rbac_resources" to "authenticated";

grant references on table "public"."rbac_resources" to "authenticated";

grant select on table "public"."rbac_resources" to "authenticated";

grant trigger on table "public"."rbac_resources" to "authenticated";

grant truncate on table "public"."rbac_resources" to "authenticated";

grant update on table "public"."rbac_resources" to "authenticated";

grant delete on table "public"."rbac_resources" to "service_role";

grant insert on table "public"."rbac_resources" to "service_role";

grant references on table "public"."rbac_resources" to "service_role";

grant select on table "public"."rbac_resources" to "service_role";

grant trigger on table "public"."rbac_resources" to "service_role";

grant truncate on table "public"."rbac_resources" to "service_role";

grant update on table "public"."rbac_resources" to "service_role";

grant delete on table "public"."rbac_role_resource_associations" to "anon";

grant insert on table "public"."rbac_role_resource_associations" to "anon";

grant references on table "public"."rbac_role_resource_associations" to "anon";

grant select on table "public"."rbac_role_resource_associations" to "anon";

grant trigger on table "public"."rbac_role_resource_associations" to "anon";

grant truncate on table "public"."rbac_role_resource_associations" to "anon";

grant update on table "public"."rbac_role_resource_associations" to "anon";

grant delete on table "public"."rbac_role_resource_associations" to "authenticated";

grant insert on table "public"."rbac_role_resource_associations" to "authenticated";

grant references on table "public"."rbac_role_resource_associations" to "authenticated";

grant select on table "public"."rbac_role_resource_associations" to "authenticated";

grant trigger on table "public"."rbac_role_resource_associations" to "authenticated";

grant truncate on table "public"."rbac_role_resource_associations" to "authenticated";

grant update on table "public"."rbac_role_resource_associations" to "authenticated";

grant delete on table "public"."rbac_role_resource_associations" to "service_role";

grant insert on table "public"."rbac_role_resource_associations" to "service_role";

grant references on table "public"."rbac_role_resource_associations" to "service_role";

grant select on table "public"."rbac_role_resource_associations" to "service_role";

grant trigger on table "public"."rbac_role_resource_associations" to "service_role";

grant truncate on table "public"."rbac_role_resource_associations" to "service_role";

grant update on table "public"."rbac_role_resource_associations" to "service_role";

grant delete on table "public"."rbac_roles" to "anon";

grant insert on table "public"."rbac_roles" to "anon";

grant references on table "public"."rbac_roles" to "anon";

grant select on table "public"."rbac_roles" to "anon";

grant trigger on table "public"."rbac_roles" to "anon";

grant truncate on table "public"."rbac_roles" to "anon";

grant update on table "public"."rbac_roles" to "anon";

grant delete on table "public"."rbac_roles" to "authenticated";

grant insert on table "public"."rbac_roles" to "authenticated";

grant references on table "public"."rbac_roles" to "authenticated";

grant select on table "public"."rbac_roles" to "authenticated";

grant trigger on table "public"."rbac_roles" to "authenticated";

grant truncate on table "public"."rbac_roles" to "authenticated";

grant update on table "public"."rbac_roles" to "authenticated";

grant delete on table "public"."rbac_roles" to "service_role";

grant insert on table "public"."rbac_roles" to "service_role";

grant references on table "public"."rbac_roles" to "service_role";

grant select on table "public"."rbac_roles" to "service_role";

grant trigger on table "public"."rbac_roles" to "service_role";

grant truncate on table "public"."rbac_roles" to "service_role";

grant update on table "public"."rbac_roles" to "service_role";

grant delete on table "public"."rbac_users" to "anon";

grant insert on table "public"."rbac_users" to "anon";

grant references on table "public"."rbac_users" to "anon";

grant select on table "public"."rbac_users" to "anon";

grant trigger on table "public"."rbac_users" to "anon";

grant truncate on table "public"."rbac_users" to "anon";

grant update on table "public"."rbac_users" to "anon";

grant delete on table "public"."rbac_users" to "authenticated";

grant insert on table "public"."rbac_users" to "authenticated";

grant references on table "public"."rbac_users" to "authenticated";

grant select on table "public"."rbac_users" to "authenticated";

grant trigger on table "public"."rbac_users" to "authenticated";

grant truncate on table "public"."rbac_users" to "authenticated";

grant update on table "public"."rbac_users" to "authenticated";

grant delete on table "public"."rbac_users" to "service_role";

grant insert on table "public"."rbac_users" to "service_role";

grant references on table "public"."rbac_users" to "service_role";

grant select on table "public"."rbac_users" to "service_role";

grant trigger on table "public"."rbac_users" to "service_role";

grant truncate on table "public"."rbac_users" to "service_role";

grant update on table "public"."rbac_users" to "service_role";



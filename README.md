# API Scaffold

this is a project scaffold for building basic Python 3.12 APIs that uses FastAPI, Async SQLAlchemy/SQLModel for 
DB, and Alembic for migrations.

dependencies:
- poetry (to install everything in pyproject.toml)
- just (in case you want to run the justfile commands)
- gh cli (in case you want to use gh commands in the justfile)
- fly.io account (to deploy to fly.io using the provided scripts)
- secrets stored in 1password (to use the provided env.tmpl file, otherwise, populate a .env file as you see fit)
- a postgres database (although you can set app.core.config.DATABASE_ENGINE to "sqlite" for localdev, i use supabase)

to start:

```zsh
poetry install
just op-render-env # (or otherwise create an .env file yourself or export the variables in app.core.config)
just run
```

to use postgres, set up a postgres server somewhere, and update the .env file with the appropriate credentials

then, change app.core.config.DATABASE_ENGINE to 'postgres'

to run migrations, do

```zsh
alembic check
alembic revision -m "<message>" --autogenerate
alembic upgrade head
```

the structure of the repository is as such:

```
app/ - main body
  core/ - core internal routines like db, auth, log, etc 
  utils/ - useful utilities
  modules/ - where most of your code will live
    base/ - base classes and interfaces
      model.py - basic db models 
      schema.py - basic db/api schemas
      service.py - business logic
      router.py - api endpoints 
      crud.py - crud operations 
    api.py - serves module endpoints under /v1 
    crud.py - wraps module crud ops so you can do `from app.modules import crud; await crud.api_key.create(...)` etc 
  main.py - main entrypoint
```

to work in the scaffold, you'll primarily be adding new modules to the modules/ directory, then adding their crud
exports to modules/crud.py and their routers to modules/api.py. see modules/api_keys for examples.

to test, run

```zsh 
just test
```

the demo uses github actions to deploy to fly.io when pushing to the master branch. 
staging and prod environement are nominally configured, although to do it yourself you'll need to 
do `fly launch --no-deploy` to provision the app in fly's infrastructure, then rename the resultant 
fly.toml files to match the naming convention employed here.

then you can do 

```zsh
just logs # inspect fly logs, defaults to staging env 
just logs prod # inspect prod logs
just deploy # deploy to staging by triggering a github action
just deploy prod # deploy to prod by triggering a github action 
just wf # inspect github workflows 
just wf prod 
just status # get fly app status
just status prod
```

to sync secrets to github actions, look at `scripts/sync_gh_vars.zsh` and modify it appropriately,
then run

```zsh
just gh-sync-secrets
```

analogously for fly.io, except fly uses the contents of the .env file we're likely using for localdev:

```zsh
just fly-sync-secrets
```

basic bearer token auth is being implemented

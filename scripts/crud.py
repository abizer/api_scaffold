from app.core.db.middleware import db
from app.core.db.session import postgres_sessionmaker

local_session = postgres_sessionmaker()
type(db).session = property(lambda _: local_session)
print("Local session injected to DB")

from app.mod import crud

# import this into a jupyter console using %run scripts/crud.py to init the
# db with an injected local session because the db is normally initialized
# during app startup by the SQLModel middleware but that doesn't happen in the
# console debugging environment
# i run it as
# %load_ext autoreload
# %autoreload 2
# %run scripts/crud.py

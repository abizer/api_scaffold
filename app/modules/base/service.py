from sqlalchemy import text

from app.core.db.middleware import db


async def get_active_connections() -> int:
    active = text(
        """SELECT count(*) as n FROM pg_stat_activity 
           WHERE state = 'active';"""
    )
    n_active = (await db.session.exec(active)).first()
    return n_active[0]


async def get_active_transactions() -> int:
    xact = text(
        """SELECT count(*) as n FROM pg_stat_activity 
               WHERE state = 'active' AND xact_start IS NOT NULL;"""
    )
    n_xact = (await db.session.exec(xact)).first()
    return n_xact[0]

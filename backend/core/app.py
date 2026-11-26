from contextlib import asynccontextmanager
import logging

from fastapi import Depends, FastAPI
from sqlalchemy import text

from core import auth
from core.db import metadata, transaction
from core.config import SEED_DEMO
from core.middleware import install
from core.queueing import broker, view
from domain.routes import routers
from domain.tag_aliases_service import stale_message
from scripts.seed_demo import seed

@asynccontextmanager
async def lifespan(app):
    from core.db import engine
    metadata.create_all(engine)
    if SEED_DEMO:
        try:
            seed()
        except Exception:
            logging.getLogger('uvicorn.error').exception('demo seed failed')
    yield

app = FastAPI(lifespan=lifespan)
install(app)
app.include_router(auth.router)
for router in routers:
    app.include_router(router)

@app.get('/health')
def health():
    with transaction() as conn:
        conn.execute(text('SELECT 1'))
    return {'ok': bool(broker.ping())}

@app.get('/compute/{token}')
def compute(token: str, user=Depends(auth.actor)):
    data = view(user, token)
    if data.get('status') == 'ready':
        with transaction() as conn:
            notice = stale_message(conn, data.get('input') or {})
        if notice:
            data['stale'] = notice
    return data

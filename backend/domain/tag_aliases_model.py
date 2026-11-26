from sqlalchemy import Column, Integer, String, Table

from core.db import metadata


tag_aliases = Table('tag_aliases', metadata,
    Column('code', String(64), primary_key=True),
    Column('alias', String(160), nullable=False, unique=True),
    Column('canonical', String(160), nullable=False),
    Column('serial', Integer, nullable=False, unique=True),
)

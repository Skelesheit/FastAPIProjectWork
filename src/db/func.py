from contextlib import asynccontextmanager

from src.db import db


@asynccontextmanager
async def get_session():
    async with db.AsyncSessionLocal() as session:
        async with session.begin():
            yield session

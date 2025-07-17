from contextlib import asynccontextmanager

from src.db import db


@asynccontextmanager
async def get_session():
    async with db.AsyncSessionLocal.begin() as session:
        yield session

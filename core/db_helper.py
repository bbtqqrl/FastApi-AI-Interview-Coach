from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession  
from core.config import settings
from typing import AsyncGenerator
from asyncio import current_task

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
    
    def get_scoped_session(self):
        sesion = async_scoped_session(
            self.session_factory,
            scopefunc=current_task,
        )
        return sesion   

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.get_scoped_session()
        yield session
        await session.close()

db_helper = DatabaseHelper(
    settings.db.DATABASE_URL_asyncpg, 
    settings.db.echo
    )
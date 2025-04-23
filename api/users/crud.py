from sqlalchemy import select
from .schemas import UserCreate, BaseUser
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from sqlalchemy.engine import Result
from auth.utils_jwt import hash_password, validate_password


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password_hash)
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    return result.scalars().first() 

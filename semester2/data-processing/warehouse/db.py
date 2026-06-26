from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing import Annotated

engine = create_async_engine("sqlite+aiosqlite:///items.db")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    
async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

async def get_db_session():
    async with async_session_maker() as session:
      yield session
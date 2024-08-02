from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    current_manga: Mapped[str] = mapped_column(default='')
    current_format: Mapped[str] = mapped_column(default='')


async def async_create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)





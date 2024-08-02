from databases.models import async_session, User

from sqlalchemy import select, update

async def check_regestration(tg_id) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return bool(user)

async def add_user_to_DB(*, tg_id):
    async with async_session() as session:
        new_user = User(
                tg_id=tg_id
            )
        session.add(new_user)
        await session.commit()


async def update_current_manga_DB(*, tg_id, current_manga):
    async with async_session() as session:
        await session.execute(update(User)
                              .where(User.tg_id == tg_id)
                              .values(
                                  current_manga=current_manga
                              ))
        await session.commit()

async def update_current_format_DB(*, tg_id, current_format):
    async with async_session() as session:
        await session.execute(update(User)
                              .where(User.tg_id == tg_id)
                              .values(
                                  current_format=current_format
                              ))
        await session.commit()


async def get_current_manga_format_from_DB(*, tg_id):
    async with async_session() as session:
        return(await session.scalar(select(User).where(User.tg_id == tg_id))).__dict__
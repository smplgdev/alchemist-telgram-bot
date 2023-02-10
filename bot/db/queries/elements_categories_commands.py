from sqlalchemy.orm import sessionmaker

from db.models.elements_categories import ElementCategory


async def add(
        session_maker: sessionmaker,
        id: int,
        title_ru: str,
):
    async with session_maker() as session:
        category = await session.merge(
            ElementCategory(
                category_id=id,
                title_ru=title_ru
            )
        )
        await session.commit()
    return category

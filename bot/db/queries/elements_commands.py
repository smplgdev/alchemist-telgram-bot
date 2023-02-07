import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from db.models.elements import Element


async def create(
        session_maker: sessionmaker,
        id: int,
        title_ru: str,
        creates_from_elements_ids=list[int, int] | None
) -> Element:
    async with session_maker() as session:
        async with session.begin():
            element = Element(
                id=id,
                title_ru=title_ru,
                creates_from_elements_ids=creates_from_elements_ids
            )
            await session.merge(element)
            return element


async def get_one(
        session_maker: sessionmaker,
        element_id: int,
) -> Element:
    async with session_maker() as session:
        async with session.begin():
            element = await session.get(Element, element_id)
            return element


async def get_elements(
        session_maker: sessionmaker,
        elements_ids: list[int]
) -> list[Element]:
    elements_list = []
    async with session_maker() as session:
        async with session.begin():
            for element_id in elements_ids:
                element = await get_one(session_maker, element_id)
                elements_list.append(element)
            return elements_list


async def find_by_title(
        session_maker: sessionmaker,
        title_ru: str
) -> Element | None:
    async with session_maker() as session:
        async with session.begin():
            stmt = (
                sa.select(Element).
                where(Element.title_ru == title_ru)
            )
            element = await session.execute(stmt).one_or_none()
            return element


async def check_if_recipe_exists(
        session_maker: sessionmaker,
        elements_ids: list[int]
) -> Element | None:
    reversed_elements_ids = elements_ids[::-1]
    async with session_maker() as session:
        async with session.begin():
            stmt = (
                sa.select(Element).
                where(sa.or_(
                    Element.creates_from_elements_ids == elements_ids,
                    Element.creates_from_elements_ids == reversed_elements_ids
                ))
            )
            element = await session.execute(stmt).one_or_none()
            return element

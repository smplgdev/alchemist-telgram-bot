import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.operators import and_

from db.models.elements import Element
from db.models.games import Game


async def create(
        session_maker: sessionmaker,
        id: int,
        title_ru: str,
        element_category_id: int,
        creates_from_elements_ids=list[int, int] | None
) -> Element:
    async with session_maker() as session:
        element = await get(session_maker, element_id=id)
        if element:
            return element

        element = Element(
            id=id,
            title_ru=title_ru,
            element_category_id=element_category_id,
            creates_from_elements_ids=creates_from_elements_ids
        )
        element = await session.merge(element)
        await session.commit()
        return element


async def get(
        session_maker: sessionmaker,
        element_id: int,
) -> Element:
    async with session_maker() as session:
        element = await session.get(Element, element_id)
        return element


async def get_elements(
        session_maker: sessionmaker,
        elements_ids: list[int]
) -> list[Element]:
    elements_list = []
    for element_id in elements_ids:
        element = await get(session_maker, element_id)
        elements_list.append(element)
    return elements_list


async def find_by_title(
        session_maker: sessionmaker,
        title_ru: str
) -> Element | None:
    async with session_maker() as session:
        sql = (
            sa.select(Element).
            where(Element.title_ru == title_ru)
        )
        query = await session.execute(sql)
        element = query.scalars().first()
    return element


async def check_if_recipe_exists(
        session_maker: sessionmaker,
        elements_ids: list[int]
) -> Element | None:
    reversed_elements_ids = elements_ids[::-1]
    async with session_maker() as session:
        sql = (
            sa.select(Element).
            where(sa.or_(
                Element.creates_from_elements_ids == elements_ids,
                Element.creates_from_elements_ids == reversed_elements_ids
            ))
        )
        query = await session.execute(sql)
        element = query.scalars().first()
        return element


async def add_new_unlocked_element(
        session_maker: sessionmaker,
        game_id: int,
        element_id: int
):
    async with session_maker() as session:
        game = await session.get(Game, game_id)
        if element_id in game.unlocked_elements_ids:
            return
        await session.execute(
            sa.update(Game).
            where(Game.id == game_id).
            values(unlocked_elements_ids=Game.unlocked_elements_ids + [element_id])
        )
        await session.commit()


async def get_user_unlocked_elements(
        session_maker: sessionmaker,
        game_id: int,
        category_id: int = None
) -> list[Element]:
    elements: list[Element] = []
    async with session_maker() as session:
        query = await session.execute(
            sa.select(Game.unlocked_elements_ids).
            where(Game.id == game_id)
        )
        user_elements_ids: list[int] = query.scalars().all()[0]
        if category_id is None:
            for element_id in user_elements_ids:
                element = await session.get(Element, element_id)
                elements.append(element)
            return elements

        for element_id in user_elements_ids:
            query = await session.execute(
                sa.select(Element).
                where(and_(
                    Element.element_category_id == category_id,
                    Element.id == element_id
                    )
                )
            )
            element = query.scalars().first()
            elements.append(element)

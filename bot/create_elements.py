from sqlalchemy.orm import sessionmaker

from db.queries import elements_commands
from db.queries.elements_categories_commands import add

categories = [
    "Вода",
    "Воздух",
    "Огонь",
    "Земля",
    "Растения",
    "Животные",
    "Птицы",
    "Насекомые",
    "Продукция",
    "Электричество",
    "Инструменты",
    "Изобретения",
    "Еда",
    "Другое",
]

elements = [
    [1, "🤍 Воздух", 2, None],
    [2, "🤎 Земля", 4, None],
    [3, "🧡 Огонь", 3, None],
    [4, "💙 Вода", 1, None],
    [5, "🌬 Ветер", 2, [1, 1]],
    [6, "💭 Пар", 2, [3, 4]],
    [7, "☁️ Облако", 2, [1, 4]],
    [8, "❄️ Мороз", 2, [1, 5]],
    [9, "🔋 Энергия", 10, [1, 3]],
    [10, "🧹 Пыль", 14, [1, 2]],
    [11, "🟧 Лава", 3, [2, 3]],
    [12, "🕳 Болото", 1, [2, 4]],
    [13, "🍷 Спирт", 13, [3, 4]],
    [14, "🗿 Камень", 4, [4, 11]],
    [15, "🟨 Песок", None, [4, 14]],
    [16, "🌫 Металл", None, [3, 14]],
    [17, "🔳 Пепел", None, [3, 10]],
    [18, "🏺 Глина", None, [12, 15]],
    [19, "🧱 Кирпич", None, [3, 18]],
    [20, "🌪 Буря", None, [1, 9]],
    [21, "🖱 Стекло", None, [3, 15]],
    [22, "🔌 Электричество", None, [9, 16]],
    [23, "🌱 Жизнь", None, [9, 12]],
    [24, "🦠 Бактерии", None, [12, 23]],
    [25, "🌱💦🌱 Водоросли", None, [4, 23]],
    [26, "🎏 Планктон", None, [4, 24]],
    [27, "🐟 Рыба", None, [24, 26]],
    [28, "🐚 Ракушки", None, [14, 26]],
    [29, "🐳 Кит", None, [26, 27]],
    [30, "🪱 Червь", None, [2, 26]],
    [31, "🦋 Бабочка", None, [1, 30]],
    [32, "🪲 Жук", None, [2, 30]],
    [33, "🦂 Скорпион", None, [15, 32]],
    [34, "🧊 Лёд", 1, [4, 8]],
    [35, "🌧 Дождь", 1, [4, 7]],
]


async def create_elements(session_maker: sessionmaker):
    # Create Categories
    for i, title in enumerate(categories, start=1):
        await add(
            session_maker=session_maker,
            id=i,
            title_ru=title
        )

    for element in elements:
        await elements_commands.create(
            session_maker,
            id=element[0],
            title_ru=element[1],
            element_category_id=element[2],
            creates_from_elements_ids=element[3]
        )

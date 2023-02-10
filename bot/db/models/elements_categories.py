import sqlalchemy as sa

from db.base import BaseModel


class ElementCategory(BaseModel):
    __tablename__ = "elements_categories"

    category_id = sa.Column(sa.Integer, primary_key=True)
    title_ru = sa.Column(sa.String(15))

import sqlalchemy as sa

from db.base import BaseModel


class Element(BaseModel):
    __tablename__ = "elements"

    id = sa.Column(sa.Integer, primary_key=True)
    title_ru = sa.Column(sa.VARCHAR(25))
    title_en = sa.Column(sa.VARCHAR(25))
    creates_from_elements_ids = sa.Column(sa.ARRAY(sa.Integer))

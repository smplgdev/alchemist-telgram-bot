import datetime
from datetime import tzinfo

import pytz
import sqlalchemy as sa

from db.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    telegram_id = sa.Column(sa.BigInteger, unique=True, nullable=False)
    deep_link = sa.Column(sa.VARCHAR(64))
    username = sa.Column(sa.VARCHAR(32))
    reg_date = sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.UTC))
    upd_date = sa.Column(sa.DateTime(timezone=True), onupdate=datetime.datetime.now(tz=pytz.UTC))

    def __str__(self) -> str:
        return f"<User:{self.telegram_id}>"

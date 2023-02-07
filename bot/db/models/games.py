import datetime

import pytz
import sqlalchemy as sa

from db.base import BaseModel


class Game(BaseModel):
    __tablename__ = "games"

    id = sa.Column(sa.BigInteger, primary_key=True)
    user_telegram_id = sa.Column(sa.ForeignKey("users.telegram_id"))
    unlocked_elements_ids = sa.Column(sa.ARRAY(sa.Integer))
    is_finished = sa.Column(sa.Boolean, default=False)
    start_date = sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.UTC))
    upd_date = sa.Column(sa.DateTime(timezone=True), onupdate=datetime.datetime.now(tz=pytz.UTC))

    def __str__(self) -> str:
        return f"<Game:{self.id}>"

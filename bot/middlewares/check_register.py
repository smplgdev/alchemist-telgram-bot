from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, types
from sqlalchemy.orm import sessionmaker

import db.queries.user_commands as user_cmd


class RegisterCheck(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.Message, dict[str, Any]], Awaitable[Any]],
            message: types.Message,
            data: dict[str, Any],
            *args,
            **kwargs
    ) -> Any:
        session_maker: sessionmaker = data['session_maker']
        user = await user_cmd.get(session_maker, message.from_user.id)
        if not user:
            deep_link = message.text.split("/start")[-1]
            user_data = {
                "telegram_id": message.from_user.id,
                "deep_link": deep_link if deep_link != "" else None,
                "username": message.from_user.username,
            }
            await user_cmd.create(
                session_maker,
                **user_data
            )
        else:
            await user_cmd.update(
                session_maker,
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
        return await handler(message, data)

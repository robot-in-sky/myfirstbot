from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
import asyncio
import logging

from app.db.db import create_async_engine, Database

from app.db.schemas.user import UserSchema, UserSchemaAdd
from app.db.schemas.order import OrderSchema, OrderSchemaAdd

print(settings.db.url)
print(settings.db.url_test)

engine = create_async_engine(url=settings.db.url)


async def dbtest():
    async with AsyncSession(bind=engine) as session:
        db = Database(session)

        result = await db.user.add(UserSchemaAdd(
            telegram_id=987654321,
            user_name="Cuckold123",
            first_name="Жмых",
            last_name="Пожилой",
            chat_id=654321
        ))
        print(result)

        # result = await db.user.get(1)
        # print(result)

        # result = await db.user.get_orders(1)
        # for order in result.orders:
        #     print(order)

        # result = await db.user.get_one(user_id=123458)
        # print(result)

        # result = await db.user.get_one(user_id=000000)
        # print(result)

        # result = await db.user.get_many(chat_id=654321)
        # print(result)

        # result = await db.user.get_many(chat_id=000000)
        # print(result)

        # result = await db.order.add(OrderSchemaAdd(
        #     first_name='Пётр',
        #     last_name='Задов',
        #     age=32,
        #     user_id=1
        # ))
        # print(result)

# logging.basicConfig(level=settings.log_level)
asyncio.run(dbtest())


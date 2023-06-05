import asyncio, aiosqlite
import context

async def init():
    async with aiosqlite.connect(context.db_name) as db:
        async with db.executescript("DROP TABLE IF EXISTS post; CREATE TABLE post (id INTEGER PRIMARY KEY AUTOINCREMENT, 'text' TEXT NOT NULL);") as cursor:
            await db.commit()


asyncio.get_event_loop().run_until_complete(init())


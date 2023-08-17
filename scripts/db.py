import aiosqlite

class Database():
    db = "../database.db"

    async def open(self):
        return await aiosqlite.connect("../database.db")

    async def close(self, connection):
        await connection.close()
    
    async def runQuery(self, query: str):
        try:
            db, cursor = await self.open()
            await cursor.execute(query)
            await self.close(db, cursor)
        except Exception as e:
            return e
        finally:
            await self.close(db, cursor)
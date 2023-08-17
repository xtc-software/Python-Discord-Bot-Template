import aiosqlite

class Database():
    db = "../database.db"

    def __init__(self) -> None:
        self.db = "../database.db"
        return
    
    async def open(self):
        return await aiosqlite.connect("../database.db")

    async def close(self, connection):
        await connection.close()
    
    async def runQuery(self, query: str):
        db, cursor = await self.open()
        await cursor.execute(query)
        await self.close(db, cursor)
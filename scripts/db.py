import aiosqlite

async def getConnection():
    return await aiosqlite.connect("../database.db")

async def closeConnection(connection):
    await connection.close()
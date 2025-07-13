from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

class AsyncDBConnector:
    def __init__(self):
        self.client = AsyncIOMotorClient('mongodb://localhost:27017', tls=False)
        self.db = self.client["blog"]["post"]
        print("mongodb connected")

    async def connection_check(self):
        info = await self.client.server_info()
        return info
db = AsyncDBConnector()
import uuid

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from uuid import uuid4
from datetime import datetime, timezone
class AsyncDBConnector:
    def __init__(self):
        self.client = AsyncIOMotorClient('mongodb://localhost:27017', tls=False)
        self.db = self.client["blog"]["posts"]
        print("mongodb connected")

    async def connection_check(self):
        info = await self.client.server_info()
        return info

    async def add_post(self, post):
        post_result = post.model_dump()
        post_result["uuid"] = str(uuid4())
        post_result["created_ts"] = datetime.now(timezone.utc)
        result = await self.db.insert_one(post_result)

        if result.acknowledged:
            print(result.acknowledged)
            return True
        else:
            return False

db = AsyncDBConnector()
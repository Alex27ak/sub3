from datetime import datetime
import time
from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import Config


class UserConfig:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db["users"]

    async def get_user(self, user_id, ) -> dict:
        user_id = int(user_id)
        user = await self.col.find_one({"user_id": user_id})
        if not user:
            return False
        return user
    
    async def add_user(self, user_id):
        res = {
                "user_id": user_id,
                "subscription": None,
                "banned": False,
            }
        await self.col.insert_one(res)
        return True

    async def update_user_info(self, user_id, value: dict, tag="$set"):
        user_id = int(user_id)
        myquery = {"user_id": user_id}
        newvalues = {tag: value}
        await self.col.update_one(myquery, newvalues)

    async def filter_users(self, dict):
        return self.col.find(dict)

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return await self.col.find({}).to_list(None)

    async def delete_user(self, user_id):
        await self.col.delete_one({"user_id": int(user_id)})

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def is_user_exist(self, id):
        user = await self.col.find_one({"user_id": int(id)})
        return bool(user)
    
    async def get_user_email(self, user_id):
        user = await self.get_user(user_id)
        return user["email"]
    
    async def update_email(self, user_id, email):
        await self.update_user_info(user_id, {"email": email})

User = UserConfig(Config.DATABASE_URL, Config.DATABASE_NAME)
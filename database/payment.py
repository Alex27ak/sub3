from bson.objectid import ObjectId
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import Config


class PaymentConfig:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.payments = self.db["payments"]
        self.plans = self.db["plans"]
        self.subscriptions = self.db["subscriptions"]

    async def create_plan(self, plan_id, plan_name, plan_price, plan_peroid, account_size, channel_id):
        plan = await self.get_plan(plan_id)
        if plan:
            return False
        else:
            await self.plans.insert_one(
                {
                    "plan_id": plan_id,
                    "plan_name": plan_name,
                    "plan_price": plan_price,
                    "plan_peroid": plan_peroid,
                    "account_size": account_size,
                    "channel_id": channel_id,
                }
            )
            return True

    async def get_plan(self, plan_id):
        return await self.plans.find_one({"plan_id": plan_id})

    async def get_plan_by_name(self, plan_name):
        return await self.plans.find_one({"plan_name": plan_name})

    async def is_plan_exist(self, price, name, period, account_size, channel_id):
        if plan := await self.plans.find_one({"plan_price": price, "plan_name": name, "plan_peroid": period, "account_size": account_size, "channel_id": channel_id, }):
            return plan
        else:
            return False
        
    async def get_plan_by_price(self, price):
        return await self.plans.find_one({"plan_price": price})

    async def get_all_plans(self):
        # sort plans by price
        return await self.plans.find().sort("plan_price", 1).to_list(None)

    async def delete_plan(self, plan_id):
        await self.plans.delete_one({"plan_id": plan_id})

    async def create_subscription(self, user_id, plan_id, payment_method, status, payment_id):
        subscription = {
            'user_id': user_id,
            'plan_id': plan_id,
            'payment_method': payment_method,
            'payment_id': ObjectId(payment_id),
            'status': status,
            'start_date': datetime.now(),
            'end_date': datetime.now() + await self.get_plan_duration(plan_id)
        }
        await self.subscriptions.insert_one(subscription)

    async def get_subscription(self, user_id):
        return await self.subscriptions.find_one({"user_id": user_id})

    async def get_all_subscriptions(self):
        return await self.subscriptions.find().to_list(None)

    async def get_subscription_by_plan(self, plan_id):
        return await self.subscriptions.find({"plan_id": ObjectId(plan_id)}).to_list(None)

    async def get_plan_duration(self, plan_id):
        plan = await self.plans.find_one({'plan_id': plan_id})
        return timedelta(days=plan['plan_peroid'] * 30)

    async def update_subscription(self, user_id, plan_id, status, payment_id, payment_method):
        subscription = {
            'user_id': user_id,
            'plan_id': plan_id,
            'payment_id': ObjectId(payment_id),
            'payment_method': payment_method,
            'status': status,
            'start_date': datetime.now(),
            'end_date': datetime.now() + await self.get_plan_duration(plan_id),
        }
        await self.subscriptions.update_one({'user_id': user_id}, {'$set': subscription})

    async def delete_subscription(self, user_id):
        await self.subscriptions.delete_one({"user_id": user_id})

    async def delete_user_subscriptions(self, user_id):
        await self.subscriptions.delete_many({"user_id": user_id})

    async def create_payment(self, user_id, amount, payment_method, payment_id, payment_type, metadata=None):
        """Create a payment record in the database.
        payment_type can be either 'invoice' or 'subscription'
        payment method can be either 'stripe' or 'crypto'
        """
        payment = {
            'user_id': user_id,
            'amount': amount,
            'payment_method': payment_method,
            'payment_id': payment_id,
            'payment_type': payment_type,
            'status': 'success',
            'date': datetime.now(),
            'metadata': metadata
        }
        _id = await self.payments.insert_one(payment)
        return _id.inserted_id

    async def get_payment(self, payment_id):
        return await self.payments.find_one({"_id": ObjectId(payment_id)})

    async def delete_payment(self, payment_id):
        await self.payments.delete_one({"_id": ObjectId(payment_id)})

    async def get_plan_by_object_id(self, plan_id):
        return await self.plans.find_one({"_id": ObjectId(plan_id)})

    async def total_subscription_count(self):
        return await self.subscriptions.count_documents({})

payment_config = PaymentConfig(Config.DATABASE_URL, Config.DATABASE_NAME)

from datetime import datetime
from database import payment_config
from pyrogram import types, Client


async def delete_expired_subscriptions(app: Client):
    subscriptions = await payment_config.get_all_subscriptions()
    for subscription in subscriptions:
        if subscription['end_date'] < datetime.now():
            await payment_config.delete_subscription(subscription['user_id'])
            user_id = subscription['user_id']
            subscribe_now_button = types.InlineKeyboardButton(
                '🔔 Subscribe Now', callback_data='view_plans')
            row = [subscribe_now_button]
            keyboard = types.InlineKeyboardMarkup([row])
            await app.send_message(user_id, '⚠️ Your subscription has expired. Please renew it to continue using our service. ⚠️', reply_markup=keyboard)
            
            plan = await payment_config.get_plan(subscription['plan_id'])
            await app.ban_chat_member(plan['channel_id'], user_id)
            await app.unban_chat_member(plan['channel_id'], user_id)

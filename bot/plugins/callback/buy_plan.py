from datetime import datetime
from pyrogram import Client, filters
from bot.config import Config
from bot.plugins.filters.is_subscribed import is_subscribed
from database import payment_config, User
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_callback_query(filters.regex('^buy_plan_(.*)$'))
@is_subscribed
async def buy_plan(bot, update):
    # check if user has subscription
    subscription  = await payment_config.get_subscription(update.from_user.id)
    user = await User.get_user(update.from_user.id)
    if subscription and subscription['status'] == 'active' and subscription['end_date'] > datetime.now():
        return await update.answer("You already have a subscription, cancel the existing one to subscribe the new one", show_alert=True)

    if user['banned']:
        return await update.answer("You are banned from using this bot 🚫", show_alert=True)

    plan_id = update.data.split('_', 2)[2]
    plan = await payment_config.get_plan(plan_id)

    buttons = [
        [
            InlineKeyboardButton(f"Contact Admin", url=f"https://telegram.me/{Config.OWNER_USERNAME}"),
           
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data=f"view_plans"),
        ],
    ]

    await update.message.edit_text(
        text=f"📛 Plan Name: {plan['plan_name']}\n"
        f"💰 Plan Price: {plan['plan_price']} {Config.CURRENCY.upper()}\n"
        f"⌛ Plan Period: {plan['plan_peroid']} months\n\n",
        reply_markup=InlineKeyboardMarkup(buttons))

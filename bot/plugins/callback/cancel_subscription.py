from datetime import datetime
from pyrogram import Client, filters
from database import payment_config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex('^cancel_subscription$'))
async def cancel_subscription(bot, update):
    user_id = update.from_user.id
    subscription = await payment_config.get_subscription(user_id)
    if subscription and subscription['status'] == 'active' and subscription['end_date'] > datetime.now():
        await payment_config.delete_subscription(user_id)
        await update.message.edit_text(
            "**Your subscription has been cancelled**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Subscribe now 📝" , callback_data="view_plans"
                        )
                    ]
                ]
            )
        )
    else:
        await update.message.edit_text(
            "**You don't have an active subscription**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Subscribe now 📝", callback_data="view_plans"
                        )
                    ]
                ]
            )
        )
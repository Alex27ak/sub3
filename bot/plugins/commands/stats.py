from pyrogram import Client, filters
from bot.config import Config
from database import User, payment_config


@Client.on_message(filters.private & filters.command("stats") & filters.user(Config.OWNER_ID))
async def stats(client, message):
    total_users = await User.total_users_count()
    total_subs = await payment_config.total_subscription_count()
    await message.reply_text(
        f"Total Users: {total_users}\n"\
        f"Total Subscriptions: {total_subs}"
    )
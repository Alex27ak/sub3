from pyrogram import Client, filters
from bot.config import Config
from bot.utils import delete_expired_subscriptions


@Client.on_message(filters.command("remind_users", prefixes="/") & filters.user(Config.OWNER_ID) & filters.incoming)
async def remind_users(client, message):
    await delete_expired_subscriptions(client)
    await message.reply_text("Done!")

from pyrogram import Client, filters

from bot.config import Config


@Client.on_message(filters.command("adminhelp", prefixes="/") & filters.private & filters.incoming & filters.user(Config.OWNER_ID))
async def admin_help(client, message):
    text = """
<b>Admin Commands</b>

/start - Start the bot
/broadcast - Broadcast a message to all users
/stats - Get bot stats
/users - Get all users
/premium_users - Get all premium users
"""
    await message.reply_text(text)
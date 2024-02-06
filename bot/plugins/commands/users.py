from pyrogram import Client, filters
from database import User
from bot.config import Config


@Client.on_message(filters.command("users", prefixes="/") & filters.user(Config.OWNER_ID) & filters.incoming)
async def users(client, message):
    users_list = await User.get_all_users()
    user_ids = [user["user_id"] for user in users_list]
    if users_list:
        premium_users = ""
        tg_users = await client.get_users(user_ids, raise_error=False)
        for premium_user in tg_users:
            premium_users += f"`{premium_user.id}` - {premium_user.mention}\n"
        await message.reply_text(
            f"**Total Users:**\n\n{premium_users}\n**Total Users:** {len(users_list)}"
        )

    else:
        await message.reply_text(
            f"**Total Users:**\n\nNo Users"
        )
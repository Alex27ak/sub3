from pyrogram import Client, filters
from database import payment_config
from bot.config import Config


@Client.on_message(filters.command("premium_users", prefixes="/") & filters.user(Config.OWNER_ID) & filters.incoming)
async def premium_users(client, message):
    premium_users_list = await payment_config.get_all_subscriptions()
    user_ids = [user["user_id"] for user in premium_users_list]
    if premium_users_list:
        premium_users = ""
        tg_users = await client.get_users(user_ids, raise_error=False)
        for premium_user in tg_users:
            premium_users += f"`{premium_user.id}` - {premium_user.mention}\n"
        await message.reply_text(
            f"**Premium Users:**\n\n{premium_users}\n**Total Premium Users:** `{len(user_ids)}`"
        )

    else:
        await message.reply_text(
            f"**Premium Users:**\n\nNo Premium Users"
        )
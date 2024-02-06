from pyrogram import Client, filters, types
from bot.config import Script, InlineButtons
from bot.utils import add_new_user


@Client.on_message(filters.command("start") & filters.private & filters.incoming)
@Client.on_callback_query(filters.regex("^start$"))
async def start(client, message):
    user_id = message.from_user.id
    await add_new_user(user_id)
    if isinstance(message, types.CallbackQuery):
        await message.answer()
        func = message.edit_message_text
    else:
        func = message.reply_text

    kwargs = {
        "text": Script.START_MESSAGE,
        "reply_markup": InlineButtons.START_BUTTONS,
        "disable_web_page_preview": True
    }

    await func(**kwargs)

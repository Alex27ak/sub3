from pyrogram import Client, filters, types
from bot.config import Config


@Client.on_callback_query(filters.regex("^help"))
@Client.on_message(filters.command(["help", "support"]) & filters.private & filters.incoming)
async def help(bot, update):
    if isinstance(update, types.CallbackQuery):
        await update.answer()
        func = update.edit_message_text
    else:
        func = update.reply_text
    text = "For support, send message to bot for an auto response or message @{}".format(Config.OWNER_USERNAME)
    back_buttons = [[
        types.InlineKeyboardButton("Back", callback_data="start"),
    ]]
    kwargs = {
        "text": text,
        "reply_markup": types.InlineKeyboardMarkup(back_buttons),
    }

    await func(**kwargs)
from pyrogram import Client, filters


@Client.on_callback_query(filters.regex('^close_data$'))
async def close_data(bot, update):
    await update.message.delete()
    await update.message.reply_to_message.delete() if update.message.reply_to_message else None

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex('^cancel_subscription_confirm$'))
async def cancel_subscription_confirmation(bot, update):
    text = """🛑 Do you want to cancel your subscription? 🛑\n\nNote: 💰 Funds are non-refundable."""
    await update.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Yes", callback_data="cancel_subscription"
                    ),
                    InlineKeyboardButton(
                        "No", callback_data="start"
                    )
                ]
            ]
        )
    )

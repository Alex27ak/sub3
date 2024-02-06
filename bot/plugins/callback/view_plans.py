from pyrogram import Client, filters, types
from bot.config import Config, Script
from database import payment_config


@Client.on_message(filters.private & filters.command("plans"))
@Client.on_callback_query(filters.regex('^view_plans$'))
async def view_plans(bot, update):
    plans = await payment_config.get_all_plans()
    buttons = []
    for i, plan in enumerate(plans, 1):
        buttons.append(
            [
                types.InlineKeyboardButton(
                    f"Plan {i} - {plan['plan_price']} {Config.CURRENCY.upper()} 💵",
                    callback_data=f"buy_plan_{plan['plan_id']}",
                )
            ]
        )
    buttons.append(
        [
            types.InlineKeyboardButton(
                "🔙 Back", callback_data=f"start"
            )
        ]
    )
    PLAN_TEXT = Script.PLAN_TEXT
    if isinstance(update, types.CallbackQuery):
        await update.message.edit_text(
            text=PLAN_TEXT,
            reply_markup=types.InlineKeyboardMarkup(buttons),
        )
    elif isinstance(update, types.Message):
        await update.reply_text(
            text=PLAN_TEXT,
            reply_markup=types.InlineKeyboardMarkup(buttons),
        )

from datetime import datetime
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import Config
from database import payment_config


@Client.on_message(filters.private & filters.command(["subscribe", "register"]))
@Client.on_callback_query(filters.regex(r"^manage_subscription$"))
async def manage_subscription(bot, update):
    user_id = update.from_user.id
    subscription = await payment_config.get_subscription(user_id)
    if subscription and subscription['status'] == 'active' and subscription['end_date'] > datetime.now():
        plan = await payment_config.get_plan(subscription['plan_id'])
        text = f"📝 **Your subscription details** 📝\n\n"\
            f"💰 **Plan:** {plan['plan_name']}\n"\
            f"💰 **Price:** {plan['plan_price']} {Config.CURRENCY.upper()}\n"\
            f"☢️ Account size: More than {plan['account_size']} {Config.CURRENCY.upper()}\n"\
            f"🟢 **Status:** {subscription['status']}\n"\
            f"📅 **Start date:** {subscription['start_date'].strftime('%d %B %Y')}\n"\
            f"📅 **End date:** {subscription['end_date'].strftime('%d %B %Y')}\n"\
            f"💳 **Payment method:** {subscription['payment_method']}\n\n"\
            f"❌ **Do you want to cancel your subscription?** ❌"
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Yes", callback_data="cancel_subscription_confirm"
                    ),
                    InlineKeyboardButton(
                        "No", callback_data="start"
                    )
                ]
            ]
        )

        if isinstance(update, types.CallbackQuery):
            await update.message.edit_text(
                text=text,
                reply_markup=markup
            )
        elif isinstance(update, types.Message):
            await update.reply_text(
                text=text,
                reply_markup=markup
            )
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Subscribe now 💰", callback_data="view_plans"
                    )
                ]
            ]
        )
        text = "**You don't have an active subscription**"
        
        if isinstance(update, types.CallbackQuery):
            await update.message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
        elif isinstance(update, types.Message):
            await update.reply_text(
                text=text,
                reply_markup=reply_markup
            )

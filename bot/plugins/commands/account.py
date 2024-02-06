from datetime import datetime
from pyrogram import Client, filters, types
from bot.config import Script
from database import payment_config


@Client.on_message(filters.command(["account", "settings"]) & filters.private & filters.incoming)
@Client.on_callback_query(filters.regex("^account$"))
async def account(client, message):
    user_id = message.from_user.id
    if isinstance(message, types.CallbackQuery):
        await message.answer()
        await message.message.delete()
        message = message.message

    user_subscription = await payment_config.get_subscription(user_id)
    if user_subscription:
        plan = await payment_config.get_plan(user_subscription['plan_id'])
        plan_name = plan['plan_name']
        expiry_date = user_subscription['end_date']
        if expiry_date > datetime.now():
            status = "Active"
        else:
            status = "Expired"
    else:
        plan_name = "No Plan"
        status = "Not Subscribed"

    # subscribe button
    subscribe_button = [[types.InlineKeyboardButton(
        text="Subscribe Now",
        callback_data="view_plans"
    )]] if status == "Not Subscribed" else [[types.InlineKeyboardButton(
        text="Manage Subscription",
        callback_data="manage_subscription"
    )]]

    # append update email button
    await message.reply_text(
        Script.ACCOUNT_INFO.format(
            user_id=user_id,
            plan_name=plan_name,
            status=status,
        ),
        reply_markup=types.InlineKeyboardMarkup(subscribe_button) if subscribe_button else None,)
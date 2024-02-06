from datetime import datetime
from pyrogram import Client, filters
from bot.utils.helpers import create_unique_link
from database import User, payment_config
from bot.config import Config, Script
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.private & filters.command("user") & filters.user(Config.OWNER_ID) & filters.incoming)
async def user(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        try:
            user = await User.get_user(user_id)
            if user:
                user_subscription = await payment_config.get_subscription(user_id)
                if user_subscription:
                    plan = await payment_config.get_plan(user_subscription["plan_id"])
                    plan_name = plan["plan_name"]
                    status = user_subscription["status"]
                else:
                    plan_name = None
                    status = None

                user_subscription_text = Script.ACCOUNT_INFO.format(
                    user_id=user["user_id"],
                    plan_name=plan_name,
                    status=status)

                if user_subscription:
                    user_subscription_text += "\n**Subscription Details:**\n\n"
                    user_subscription_text += f"📅 **Start date:** {user_subscription['start_date'].strftime('%d %B %Y')}\n" \
                        f"📅 **End date:** {user_subscription['end_date'].strftime('%d %B %Y')}\n" \
                        f"💳 **Payment method:** {user_subscription['payment_method']}\n\n"

                buttons = await get_buttons(user_id, user_subscription)
                await message.reply_text(
                    user_subscription_text,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            else:
                await message.reply_text("User not found!")
        except:
            await message.reply_text("Error!")
    else:
        await message.reply_text("Invalid Command!, Use /user [user_id], Example: /user 1234567890")


@Client.on_callback_query(filters.regex("^cancel_subscription_") & filters.user(Config.OWNER_ID))
async def cancel_subscription_admin(bot, message):
    " Cancel subscription from admin panel "
    user_id = int(message.data.split("_", 2)[2])
    subscription = await payment_config.get_subscription(user_id)

    if subscription and subscription['status'] == 'active' and subscription['end_date'] > datetime.now():
        await payment_config.delete_subscription(user_id)
        await message.message.edit_text(
            "**User subscription has been cancelled**")
    else:
        await message.message.edit_text(
            "**User don't have an active subscription**",
        )


@Client.on_callback_query(filters.regex("^view_plans") & filters.user(Config.OWNER_ID))
async def view_plans_admin(bot, message):
    " View plans from admin panel "
    user_id = int(message.data.split(" ")[1])
    if await payment_config.get_subscription(user_id):
        await message.message.reply_text(
            "**User already have an active subscription**",
        )
        return
    plans = await payment_config.get_all_plans()
    buttons = []
    for plan in plans:
        buttons.append(
            [
                InlineKeyboardButton(
                    plan["plan_name"], callback_data=f"subscribe_user_{user_id}_{plan['plan_id']}")
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                "Back", callback_data=f"user {user_id}")
        ]
    )
    await message.message.edit_text(
        "**Select a plan for user**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex("^subscribe_user_") & filters.user(Config.OWNER_ID))
async def subscribe_user_admin(bot, message):
    " Subscribe user from admin panel "
    user_id = int(message.data.split("_")[2])
    if await payment_config.get_subscription(user_id):
        await message.message.reply_text(
            "**User already have an active subscription**",
        )
        return
    
    plan_id = message.data.split("_", 3)[3]
    plan = await payment_config.get_plan(plan_id)
    payment = await payment_config.create_payment(user_id, amount=plan["plan_price"], payment_method="admin", payment_type="admin", payment_id="admin",)
    await payment_config.create_subscription(user_id, plan_id, "admin", "active", payment_id=payment)
    subscription = await payment_config.get_subscription(user_id)
    link = await create_unique_link(bot, user_id, plan["channel_id"], subscription["end_date"])
    try:
        await bot.send_message(
            user_id,
            text="Your subscription is active now. You can join the channel using the below link.\n\n<b>Channel Link:</b> {}".format(link))
    except:
        await message.message.reply_text(
            "**User has blocked the bot**",
        )
    await message.message.edit_text(
        "**User has given subscribed**",
    )


async def get_buttons(user_id, is_subscribed):
    buttons = []
    if is_subscribed:
        buttons.append(
            [
                InlineKeyboardButton(
                    "Cancel Subscription", callback_data=f"cancel_subscription_{user_id}")
            ]
        )
    else:
        buttons.append(
            [
                InlineKeyboardButton(
                    "Subscribe", callback_data=f"view_plans {user_id}")
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "Back", callback_data="start")
        ]
    )
    return buttons

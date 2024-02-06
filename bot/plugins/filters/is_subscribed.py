# create a pyrogram wrapper if the user is subscribed to any plan or not

from datetime import datetime
import functools
from pyrogram import Client
from pyrogram.types import Message
from database import payment_config


def is_subscribed(func):
    @functools.wraps(func)
    async def wrapper(client: "Client", message: "Message"):
        subscription = await payment_config.get_subscription(message.from_user.id)
        if subscription and subscription['status'] == 'active' and subscription['end_date'] > datetime.now():
            if isinstance(message, Message):
                return await message.reply("You already have a subscription, cancel the existing one to subscribe the new one", quote=True)
            else:
                return await message.answer("You already have a subscription, cancel the existing one to subscribe the new one", show_alert=True)

        return await func(client, message)

    return wrapper

import os
from dotenv import load_dotenv
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
load_dotenv('.env')


def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


class Config(object):
    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    OWNER_ID = int(os.environ.get("OWNER_ID"))
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "SubscrptionBot")
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    plans = os.environ.get("PLANS", None)  # month:usd\nmonth:usd\nmonth:usd
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)
    PLANS = []
    WEB_SERVER = is_enabled(os.environ.get("WEB_SERVER", "True"), True)
    CURRENCY = os.environ.get("CURRENCY", "USD").lower()
    # coin:wallet_id\ncoin:wallet_id\ncoin:wallet_id
    PLAN_TEXT = ""

    for i, line in enumerate(plans.split(), 1) if plans else []:
        if line.count(":") != 4:
            raise Exception(
                "Invalid plan format. Should be month:usd:channel_id:account_size:plan_name")
        month, usd, channel_id, account_size, plan_name = line.split(":")
        if not month.isdigit() or not usd.isdigit() or not channel_id.replace("-", "").isdigit() or not account_size.isdigit():
            raise Exception(
                "Invalid plan format. Should be month:usd:channel_id:account_size")

        PLANS.append(
            {
                "month": int(month),
                "usd": int(usd),
                "channel_id": int(channel_id),
                "account_size": int(account_size),
                "name": plan_name
            }
        )
        PLAN_TEXT += f"**Plan {i}**\n\n📛 Plan Name: Account Size more than {account_size} {CURRENCY.upper()}\n💰 Price: {usd} {CURRENCY.upper()}\n📊 Account Size: More than {account_size} {CURRENCY.upper()}\n\n"


class Script(object):
    start_message = """🎉 Welcome"""

    START_MESSAGE = os.environ.get("START_MESSAGE", start_message)
    ACCOUNT_INFO = """**Account Info**

👤 user ID: `{user_id}`
📛 Plan Name: `{plan_name}`
✅ Status: `{status}`
    """

    PLAN_TEXT = f'''
**For support, send message to bot for an auto response or message @{Config.OWNER_USERNAME}**'''
    PLAN_TEXT = os.environ.get("PLAN_TEXT", PLAN_TEXT)


class InlineButtons(object):
    START_BUTTONS = IKM(
        [
            [IKB("📢 Plans", callback_data="view_plans")],
            [IKB("📝 Manage Subscription", callback_data="manage_subscription")],
            [IKB("📊 Account", callback_data="account")],
        ]
    )

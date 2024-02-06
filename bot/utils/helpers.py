import asyncio
from pyrogram import errors
from bot.config import Config, Script
from database import User, payment_config
from pyrogram.types import ChatInviteLink, BotCommand
from pyrogram import Client, types
from aiohttp import web


class temp(object):
    USERS_INFO = {}
    USER_PROMPT = []


async def reply_text(message, text: str, **kwargs):
    try:
        return await message.reply_text(text, disable_web_page_preview=True, quote=True, **kwargs)
    except errors.FloodWait as e:
        x = await message.reply_text(f"Sleeping for {e.value} seconds")
        print(f"Sleeping for {e.value} seconds")
        await asyncio.sleep(e.value)
        await x.delete()
        return await message.reply_text(text, disable_web_page_preview=True, quote=True, **kwargs)
    except errors.MessageNotModified:
        pass
    except errors.BadRequest:
        pass


async def add_new_user(user_id):
    if not await User.is_user_exist(user_id):
        user = await User.add_user(user_id)
        return user
    else:
        return False


# create unique invite link
async def create_unique_link(app: Client, user_id, channel_id, expiry_date):
    link: ChatInviteLink = await app.create_chat_invite_link(channel_id, name=str(user_id), expire_date=expiry_date, creates_join_request=1)
    return link.invite_link


async def create_or_update_subscription(user_id, payment_id, invoice_id=None, method="card", plan_id=None):
    subscription = await payment_config.get_subscription(user_id)
    if not subscription:
        await payment_config.create_subscription(
            user_id,
            plan_id,
            method,
            "active",
            payment_id
        )
    else:
        await payment_config.update_subscription(
            user_id,
            plan_id,
            "active",
            payment_id,
            method
        )
    return True



async def make_plans():
    for plan in Config.PLANS:
        name = plan['name']
        desc = f"{plan['month']} Month Plan for {plan['usd']} {Config.CURRENCY}"
        account_size = plan['account_size']
        channel_id = plan['channel_id']
        plan_id = f"{name}_{channel_id}_{plan['usd']}"
        plan["id"] = plan_id
        st_plan = await payment_config.is_plan_exist(price=plan["usd"], name=name, period=plan["month"], account_size=account_size, channel_id=channel_id)
        if not st_plan:
            await payment_config.create_plan(plan_id, name, plan["usd"], plan["month"], plan["account_size"], plan["channel_id"])


    database_plans = await payment_config.get_all_plans()
    plan_ids = [plan["id"] for plan in Config.PLANS]
    for plan in database_plans:
        if plan["plan_id"] not in plan_ids:
            await payment_config.delete_plan(plan["plan_id"])


async def create_server():
    if Config.WEB_SERVER:
        routes = web.RouteTableDef()
        @routes.get("/", allow_head=True)
        async def root_route_handler(request):
            res = {
                "status": "running",
            }
            return web.json_response(res)

        async def web_server():
            web_app = web.Application(client_max_size=30000000)
            web_app.add_routes(routes)
            return web_app

        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", 8000).start()



async def set_commands(app):
    COMMANDS = [
        BotCommand("start", "Used to start the bot."),
        BotCommand("account", "Used to get account information."),
        BotCommand("plans", "Get plan information."),
        BotCommand("subscribe", "Used to subscribe to a plan."),
        BotCommand("adminhelp", "Used to get admin commands."),
    ]
    await app.set_bot_commands(COMMANDS)
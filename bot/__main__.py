
from bot.utils.remind import delete_expired_subscriptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import Bot


if __name__ == '__main__':
    bot = Bot()
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(delete_expired_subscriptions,
                      "interval", hours=1, args=[bot])
    bot.run()

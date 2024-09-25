import logging
import asyncio

from main.data.loader import dp, bot
from main.handlers import user_menu

logging.basicConfig(filename="log.txt", level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info("Bot started")
    dp.include_router(user_menu.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logger.info("Run Main")
    asyncio.run(main())
from aiogram import executor, types

import handlers
import states
from configs.config import db, dp


def bot_is_start():
    print('[+] Bot is start')


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=bot_is_start(),
    )

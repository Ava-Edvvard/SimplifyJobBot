#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .config_db import SimplifyDB
from aiogram.utils.callback_data import CallbackData

# STATIC
# Система на которой запускается бот (Linux/Windows)
platform = sys.platform.lower()
# Путь на корневой каталог проекта
BASE_URL = os.getcwd()
# Путь на каталог с медиафайлами бота
if 'win' in platform:  # Windows
    MEDIA_URL = f'{BASE_URL}\\media'
else:
    MEDIA_URL = f'{BASE_URL}/media'

# TELEGRAM
# Токен бота
BOT_TOKEN = '6752065164:AAFgCx9H2yAmwyQfo7BxNyoO0fy5zkE4qf8'
# Админы бота (идентификаторы str)
superusers = []

# Database
# Токен для доступа к базе данных директус
simplify_token = 'UokPEWhb7Gjf2hrqjRv_FlHOzWPSViPG'
# Объявление объекта для обработки базы данных
db = SimplifyDB(access_token=simplify_token)

# Bot
# Объект для работы с FSMContext (машиной состояний) - не пригодилось в текущей версии
storage = MemoryStorage()
# Объект для работы с телеграм API
bot = Bot(BOT_TOKEN, parse_mode='HTML')
# Объект для обработки входящих сообщений и действий на бота
dp = Dispatcher(bot, storage=storage)


def get_load_message():
    """Функция для генерации прогрузочного сообщения (прогрузка между основным выводом инфомрации в боте)"""
    if 'win' in platform:  # Если бот запущен с windows то использовать \\ для перехода между каталогами|файлами системы
        return types.InputMedia(
            type='photo',
            media=open(MEDIA_URL + '\\loading.jpg', 'rb'),
            caption='Загрузка...'
        )
    # Если бот запщуен с Linux то использовать / для перехода между каталогами|файлами системы
    return types.InputMedia(
        type='photo',
        media=open(MEDIA_URL + '/loading.jpg', 'rb'),
        caption='Загрузка...'
    )


# CallbackData объекты предназначеные для обрабокти действий связанных InlineButtons
# Действия над айтемами (параметр айтема при выборке type: section/special)
item_callback = CallbackData('item', 'item_id')
# Действия над продуктами (параметр айтема type: product)
product_callback = CallbackData('product', 'item_id')
# Действия над кнопками основного меню (back/shop, обрабатываются в файле keyboards в функции get_menu_keyboard_buttons)
menu_callback = CallbackData('menu', 'handler', 'item_id')

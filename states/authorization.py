import os
import sys

from aiogram import types
from configs.config import dp, db
from keyboards.keyboards import keyboard_main

sys.path.insert(0, os.getcwd())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    item = db.get_item_by_id(5)
    photo_link = db.get_file_link(item['photo'])

    await message.answer_photo(
        caption=item['block_text'],
        photo=photo_link,
        reply_markup=keyboard_main
    )

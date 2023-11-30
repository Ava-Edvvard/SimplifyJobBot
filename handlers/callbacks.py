from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from configs.config import db, dp, item_callback, bot, get_load_message, product_callback, menu_callback
from keyboards.keyboards import generate_item_keyboard


async def load_message(query: types.CallbackQuery):
    """
    Функция обрабатывающая текущее сообщение по шаблону `прогрузка` между выводом основных данных бота

    :param query: данные о текущем сообщении в боте
    """
    try:
        await bot.edit_message_media(
            get_load_message(),
            query.from_user.id,
            query.message.message_id,
        )
    except MessageNotModified:
        pass
    return


@dp.callback_query_handler(menu_callback.filter(handler='back'))
async def back(query: types.CallbackQuery, callback_data: dict):
    """
    Функция вызываемая при вызове инлайн кнопки `назад`, возвращает предыдущий рздел бота

    :param query: данные о текущем сообщении в боте
    :param callback_data: данные передаваемые в кнопке CallbackData('menu', 'handler', 'item_id')
    """
    # Объявление прогрузки
    await load_message(query)

    # Обработка данных из CallbackData (были выданы при генерации кнопок get_menu_buttons)
    # Получение id текущего раздела
    item_id = callback_data.get('item_id')
    # Получение данных об айтеме текущего раздела (необходимо для получения id раздела которому он принадлежит)
    item = db.get_item_by_id(item_id)
    # Получение id раздела (предыдущий раздел) которому принадлежит текущий айтем
    before_item_id = item['last_block']
    # Изменине данных в CallbackData для их последующей обработки (для вывода предыдущего раздела)
    callback_data['item_id'] = before_item_id
    # Получение данных о предыдущем разделе
    before_item = db.get_item_by_id(before_item_id)
    # Получение типа предыдущего раздела
    before_item_type = before_item['type']

    # Словарь с типами айтемов (разделов) и ссылками на функции вызываемыми при генерации разделов
    # Данная конструкция предназначена для уменьшения количества кода и исключения if/elif блоков
    menu_handlers = {
        'product': product,
        'section': section,
        'special': section
    }
    # Вызов обработчика на основе типа данных предыдущего айтема и генерации его кнопок (разделов)
    await menu_handlers[before_item_type](query, callback_data)


@dp.callback_query_handler(menu_callback.filter(handler='shop'))
async def shop(query: types.CallbackQuery, callback_data: dict):
    """
    Функция для перехода на основную страницу бота (магазин)

    :param query: данные о текущем сообщении в боте
    :param callback_data: данные передаваемые в кнопке CallbackData('menu', 'handler', 'item_id')
    """
    await section(query, callback_data)


@dp.callback_query_handler(item_callback.filter())
async def section(query: types.CallbackQuery, callback_data: dict):
    """
    Функция для генерации и вывода раздела на которырй перешел пользователь (по шаблону section/special)
    Вызывается в случае если айтем на который переходит пользователь имел type=section/special

    :param query: данные о текущем сообщении в боте
    :param callback_data: данные передаваемые в кнопке CallbackData('item', 'item_id')
    """
    await load_message(query)

    # ID раздела на который переходит пользователь
    item_id = callback_data.get('item_id')
    # Данные раздела
    current_item_data = db.get_item_by_id(item_id)
    # ID фото раздела
    item_photo = current_item_data['photo']
    # Текст раздела (caption)
    item_text = current_item_data['block_text']
    # Если текста нет в параметре block_text то взять текст и note, если его нет и там то оставить пустое значение
    if item_text is None:
        item_text = current_item_data['note'] if current_item_data['note'] is not None else ''
    # Получение вложенных в раздел айтемов отсортированных по строка->колона
    include_items = db.get_items('row', 'column', last_block=item_id)

    # Генерация сообщения с фотографией и текстом раздела
    message = types.InputMedia(
        type='photo',
        media=db.get_file_link(item_photo),
        caption=item_text
    )

    # Генерация кнопок раздела на основе вложенных в него айтемов
    # Отправление измененного сообщения пользователю
    await bot.edit_message_media(
        message,
        query.from_user.id,
        query.message.message_id,
        reply_markup=generate_item_keyboard(item_id, include_items)
    )


@dp.callback_query_handler(product_callback.filter())
async def product(query: types.CallbackQuery, callback_data: dict):
    """
    Функция для генерации и вывода раздела на которырй перешел пользователь (по шаблону product)
    Вызывается в случае если айтем на который переходит пользователь имел type=product

    :param query: данные о текущем сообщении в боте
    :param callback_data: данные передаваемые в кнопке CallbackData('item', 'item_id')
    """
    # ID раздела на который переходит пользователь
    item_id = callback_data.get('item_id')
    # Данные раздела
    current_item_data = db.get_item_by_id(item_id)
    # ID фото раздела
    item_photo = current_item_data['photo']
    # Текст раздела (caption)
    item_text = current_item_data['block_text']
    # Если текста нет в параметре block_text то взять текст и note, если его нет и там то оставить пустое значение
    if item_text is None:
        item_text = current_item_data['note'] if current_item_data['note'] is not None else ''
    # Получение вложенных в раздел айтемов отсортированных по строка->колона
    include_items = db.get_items('row', 'column', last_block=item_id)

    # Генерация сообщения с фотографией и текстом раздела
    message = types.InputMedia(
        type='photo',
        media=db.get_file_link(item_photo),
        caption=item_text
    )

    # Генерация кнопок раздела на основе вложенных в него айтемов
    # Отправление измененного сообщения пользователю
    await bot.edit_message_media(
        message,
        query.from_user.id,
        query.message.message_id,
        reply_markup=generate_item_keyboard(item_id, include_items)
    )

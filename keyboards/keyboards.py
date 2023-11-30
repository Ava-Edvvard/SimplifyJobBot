from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from configs.config import item_callback, bot, product_callback, menu_callback


# Основная клавитаруа вызывающаяся при команде /start (вызывается в файле authorization в каталоге states)
keyboard_main = InlineKeyboardMarkup()
keyboard_main.add(
    InlineKeyboardButton('Магазин', callback_data=item_callback.new(item_id='5')),
)


def get_menu_keyboard_buttons(item_id):
    """
    Функция для генерирации кнопок Назад и Магазин

    :param item_id: Идентификатор текущего айтема из базы директус на котором в данный момент находится пользователь
    :return: list[InlineKeyboardButton]
    """
    buttons = []
    if int(item_id) != 5:
        buttons.append(
            InlineKeyboardButton(
                'Назад',
                callback_data=menu_callback.new(
                    'back',
                    item_id=item_id
                )
            )
        )
        buttons.append(
            InlineKeyboardButton(
                'Магазин',
                callback_data=menu_callback.new(
                    'shop',
                    item_id=str(5)
                )
            )
        )
    return buttons


def generate_item_keyboard(item_id, include_items):
    """
    Функция генерирует клавитуру раздела на основе вложенных в него айтемов (фильтр по last_block)

    :param item_id: Идентификатор текущего айтема (текущий раздел) из базы директус
    :param include_items: Список айтемов вложенных в иекущий раздел
    :return: InlineKeyboardMarkup
    """
    # Если у текущего раздела не твложенных айтемов то сгенеруется меню и отправится пользователю
    # Остальные дейсвтия функции выполняться не будут
    if not include_items:
        menu = get_menu_keyboard_buttons(item_id)
        if menu:
            keyboard = InlineKeyboardMarkup()
            return keyboard.row(*menu)

    # Словарь с типами айтемов (разделов) и ссылками на функции которые их обрабатывают
    # Данная конструкция предназначена для уменьшения количества кода и исключения if/elif блоков
    handlers = {
        'product': handle_product,
        'section': handle_section,
        'special': handle_section
    }

    # Объект принимает тип вложенных в раздел айтемов (section/product/special)
    items_type = include_items[0]['type']
    # На основе типа айтемов вызывается нужный обработчик который генерирует клавиатуру
    keyboard = handlers[items_type](include_items)
    # К клавиатуре добавляется меню
    menu = get_menu_keyboard_buttons(item_id)
    if menu:
        # Функция get_menu_keyboard_buttons возваращет структуру list[InlineKeyboardButton], поэтому она распаковывается
        keyboard.row(*menu)
    return keyboard


def handle_product(items):
    """
    Обработчик генерирующий клавиатуру на основе вложенных айтемов с типом product

    :param items: Список вложенных в раздел айтемов
    :return: InlineKeyboardMarkup
    """
    # Объявление клавиатуры
    keyboard = InlineKeyboardMarkup()
    # Объявление текущей строки (по умолчанию 1)
    current_row = 1
    # Объявление текущей строки в клавиатуре
    keyboard_row = keyboard.row()
    # Проход по каждому вложенному айтему для генерации кнопок раздела
    for item in items:
        # ID вложенного айтема
        _id = item['id']
        # Строка на которой он должен находиться (так как айтемы отсортированы по строка->колонна, то
        # обрабатывать расположение по колонне не нужно, достаточно добавлять кнопки в строку пока текущая строка
        # равна строке на которой должна находиться кнопка (current_row == row)
        row = item['row']
        # Текст который должна иметь кнопка
        text = item['button_text'] if 'null' not in item['button_text'] else item['note']
        # Проверка - если текущая строка не совпадает со строкой на которой должна находиться кнопка,
        # то в клавиатуре объявляется новая строка, а параметр текущей строки принимает значение строки айтема
        if current_row != row or row is None:
            keyboard_row = keyboard.row()
            current_row = row
        # Кнопка добавляется в текущую строку клавитуры
        keyboard_row.insert(
            InlineKeyboardButton(text, callback_data=product_callback.new(item_id=_id))
        )
    return keyboard


def handle_section(items):
    """
    Обработчик генерирующий клавиатуру на основе вложенных айтемов с типом section/special

    :param items: Список вложенных в раздел айтемов
    :return: InlineKeyboardMarkup
    """
    # Объявление клавиатуры
    keyboard = InlineKeyboardMarkup()
    # Объявление текущей строки (по умолчанию 1)
    current_row = 1
    # Объявление текущей строки в клавиатуре
    keyboard_row = keyboard.row()
    # Проход по каждому вложенному айтему для генерации кнопок раздела
    for item in items:
        _id = item['id']
        # Строка на которой он должен находиться (так как айтемы отсортированы по строка->колонна, то
        # обрабатывать расположение по колонне не нужно, достаточно добавлять кнопки в строку пока текущая строка
        # равна строке на которой должна находиться кнопка (current_row == row)
        row = item['row']
        # Текст который должна иметь кнопка
        text = item['button_text'] if 'null' not in item['button_text'] else item['note']
        # Проверка - если текущая строка не совпадает со строкой на которой должна находиться кнопка,
        # то в клавиатуре объявляется новая строка, а параметр текущей строки принимает значение строки айтема
        if current_row != row or row is None:
            keyboard_row = keyboard.row()
            current_row = row
        # Кнопка добавляется в текущую строку клавитуры
        keyboard_row.insert(
            InlineKeyboardButton(text, callback_data=item_callback.new(item_id=_id))
        )
    return keyboard




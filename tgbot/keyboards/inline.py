from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData # <--- Важно для aiogram 3.x

# 1. Определяем фабрику CallbackData (для структурированных данных)
class MyCallbackFactory(CallbackData, prefix="my_action"):
    action: str # Например, "view", "edit", "delete"
    item_id: int # Например, ID элемента, с которым будет произведено действие

# 2. Функция для создания Inline-клавиатуры
def get_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки, используя нашу фабрику для callback_data
    builder.row(
        InlineKeyboardButton(
            text="Показать товар 101",
            callback_data=MyCallbackFactory(action="view", item_id=101).pack()
        ),
        InlineKeyboardButton(
            text="Редактировать товар 101",
            callback_data=MyCallbackFactory(action="edit", item_id=101).pack()
        )
    )
    # Кнопка с URL-ссылкой
    builder.row(
        InlineKeyboardButton(text="Посетить сайт", url="https://example.com")
    )
    # Кнопка для переключения в inline-режим (для поиска или отправки сообщений в текущий чат)
    builder.row(
        InlineKeyboardButton(text="Начать inline-поиск", switch_inline_query=""),
        InlineKeyboardButton(text="Отправить сообщение через inline", switch_inline_query_current_chat="")
    )

    # Автоматическое распределение кнопок (например, 2 кнопки в каждом ряду)
    builder.adjust(2)

    return builder.as_markup()


#  БОЛЕЕ ПРОСТОЙ ПРИМЕР ДЛЯ БИЛДА КНОПОК (Более старый метод создания, имеет меньший функционал)
def start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="ЗАКАЗАТЬ",
                                 callback_data="buy_start")
        ],
        [
            InlineKeyboardButton(text="Подробнее о сайтах",
                                 callback_data="site_information")
        ],
        [
            InlineKeyboardButton(text="Подробнее о телеграмм ботах",
                                 callback_data="bots_information")
        ],
        [
            InlineKeyboardButton(text="Подробнее о других услугах",
                                 callback_data="other_information")
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
    return keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def visa_country_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Индия", callback_data="visa_data:country:ind")]])


def visa_type_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Туристическая 30 дней",
                              callback_data="visa_data:type:tour_30d")],
        [InlineKeyboardButton(text="Туристическая 1 год",
                              callback_data="visa_data:type:tour_1y")],
        [InlineKeyboardButton(text="Туристическая 5 лет",
                              callback_data="visa_data:type:tour_5y")]])


def check_passport_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Отправить снова",
                              callback_data="passport_checked:no"),
        InlineKeyboardButton(text="OK",
                              callback_data="passport_checked:yes")]])

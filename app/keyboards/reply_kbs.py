from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_placeholder_kb(manga_name:str):
    placeholder_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=' ')]],
                                         resize_keyboard=True,
                                         is_persistent=True,
                                         input_field_placeholder=f'{manga_name}')
    return placeholder_kb 

del_kb = ReplyKeyboardRemove()
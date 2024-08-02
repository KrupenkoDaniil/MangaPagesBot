from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.CONSTANTS import PAGE_DESCRIPTION_FORMATS
from utils.ya_disk_api import get_mangas_names

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поменять мангу', callback_data='change_manga')],
    [InlineKeyboardButton(text='Поменять формат описания', callback_data='change_format')],
])

def create_formats_kb():
    formats_kb = InlineKeyboardBuilder()

    for format in PAGE_DESCRIPTION_FORMATS:
        data = format.replace(' [description]', '')
        formats_kb.add(InlineKeyboardButton(text=format, callback_data=f'format_{data}'))

    return formats_kb.adjust(1).as_markup()

def create_mangas_kb():
    manga_names_list = get_mangas_names()
    manga_names_kb = InlineKeyboardBuilder()
    
    for manga_name in manga_names_list:
        data = manga_name.replace(' ', '_')
        manga_names_kb.add(InlineKeyboardButton(text=manga_name, callback_data=f'manga_{data}'))
    manga_names_kb.add(InlineKeyboardButton(text='Новая манга', callback_data='create_new_manga'))
    
    return manga_names_kb.adjust(2).as_markup()

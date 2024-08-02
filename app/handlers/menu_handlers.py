import os

from yadisk.exceptions import PathExistsError, DirectoryExistsError

from aiogram import Bot, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender

from databases.requests import update_current_format_DB, update_current_manga_DB, \
                                get_current_manga_format_from_DB

from keyboards.inline_kbs import menu_kb, create_mangas_kb, create_formats_kb
from keyboards.reply_kbs import create_placeholder_kb
from utils.CONSTANTS import BOT_MESSAGES, PC_MANGA_FOLDER_PATH
from utils.states import Menu
from utils.keyboards_utils import handle_inline_keyboard
from utils.ya_disk_api import create_manga_folder, upload_page
from utils.page_utils import get_chapter_page_description
from utils.errors import GettingChapterPageDescriptionError


menu_router = Router()

@menu_router.message(Command('menu'))
async def open_menu(message: Message, state: FSMContext):
    await state.set_state(Menu.menu) 
    
    await message.answer(BOT_MESSAGES['menu']['main'],
                         reply_markup=menu_kb)


@menu_router.callback_query(Menu.menu, F.data == 'change_manga')
async def start_changing_manga(callback: CallbackQuery):
    await handle_inline_keyboard(callback)

    await callback.message.answer(BOT_MESSAGES['menu']['change_manga'],
                                  reply_markup=create_mangas_kb())
    
@menu_router.callback_query(Menu.menu, F.data.startswith('manga_'))
async def change_manga(callback: CallbackQuery, state: FSMContext):
    try:
        await handle_inline_keyboard(callback)
        manga_name = ' '.join(callback.data.split('_')[1:])
        await update_current_manga_DB(tg_id=callback.from_user.id, current_manga=manga_name)
        
        await state.set_state(Menu.menu)
        
        await callback.message.answer(BOT_MESSAGES['menu']['manga_changed'] + manga_name,
                                    reply_markup=create_placeholder_kb(manga_name))
    except Exception as e:
        await callback.message.answer(f'Exception: ' + str(e))


@menu_router.callback_query(Menu.menu, F.data == 'create_new_manga')
async def start_creating_new_manga(callback: CallbackQuery, state: FSMContext):
    await handle_inline_keyboard(callback)

    await state.set_state(Menu.new_manga)

    await callback.message.answer(BOT_MESSAGES['menu']['create_new_manga']) 
    
@menu_router.message(Menu.new_manga, F.text)
async def create_new_manga(message: Message, state: FSMContext):
    try:
        
        await update_current_manga_DB(tg_id=message.from_user.id, current_manga=message.text)
        create_manga_folder(message.text)
        
        await state.set_state(Menu.menu)
        
        await message.answer(BOT_MESSAGES['menu']['new_manga_created'], 
                             reply_markup=create_placeholder_kb(message.text))
    
    except DirectoryExistsError:
        await message.answer(BOT_MESSAGES['errors']['new_manga_already_exists_error'])

    except Exception as e:
        await message.answer(f'Exception: ' + str(e))


@menu_router.callback_query(Menu.menu, F.data == 'change_format')
async def start_changing_format(callback: CallbackQuery):
    await handle_inline_keyboard(callback)

    await callback.message.answer(BOT_MESSAGES['menu']['change_format'],
                           reply_markup=create_formats_kb())

@menu_router.callback_query(Menu.menu, F.data.startswith('format_'))
async def change_format(callback: CallbackQuery, state: FSMContext):
    await handle_inline_keyboard(callback)

    new_format = callback.data.split('_')[-1]
    await update_current_format_DB(tg_id=callback.from_user.id, current_format=new_format)

    await state.set_state(Menu.menu) 
    
    await callback.message.answer(BOT_MESSAGES['menu']['format_changed'] + new_format)


@menu_router.message(F.photo)
async def load_photo(message: Message, state: FSMContext, bot: Bot):
    try:
        await state.set_state(Menu.loading_page)

        user_data = await get_current_manga_format_from_DB(tg_id=message.from_user.id)
        current_format, current_manga = user_data['current_format'], user_data['current_manga']
    
        # get info about sent pic from tg
        page = await bot.get_file(message.photo[-1].file_id)
        page_extension = page.file_path.split('.')[-1]
        page_caption = message.caption
        await bot.download_file(page.file_path, f'{PC_MANGA_FOLDER_PATH}/temp.{page_extension}')
        
        # get metadata about pic
        chapter_number, page_number, description = get_chapter_page_description(page_caption, current_format)

        # gather file name
        file_name = f'{current_manga}(c{chapter_number}p{page_number}){description}.{page_extension}'

        # load file to yandex disk
        upload_page(file_name, page_extension, current_manga)
        os.remove(f'{PC_MANGA_FOLDER_PATH}/temp.{page_extension}')

        await message.answer(file_name)

        # if page is loaded succesfully, no need for Menu.loading_page state
        await state.set_state(Menu.menu)

    except GettingChapterPageDescriptionError:
        await message.answer(BOT_MESSAGES['errors']['format_error'])
    
    except PathExistsError:
        await message.answer(BOT_MESSAGES['errors']['page_already_exists_error'])

    except Exception:
        await message.answer(BOT_MESSAGES['errors']['loading_error'])
        

@menu_router.message(Menu.loading_page, F.text)
async def add_caption(message: Message, state: FSMContext):
    try:

        user_data = await get_current_manga_format_from_DB(tg_id=message.from_user.id)
        current_format, current_manga = user_data['current_format'], user_data['current_manga']
        page_caption = message.text
        page_extension = os.listdir(PC_MANGA_FOLDER_PATH)[0].split('.')[1]

        # get metadata about pic
        chapter_number, page_number, description = get_chapter_page_description(page_caption, current_format)

        # gather file name
        file_name = f'{current_manga}(c{chapter_number}p{page_number}){description}.{page_extension}'

        # load file to yandex disk
        upload_page(file_name, page_extension, current_manga)
        os.remove(f'{PC_MANGA_FOLDER_PATH}/temp.{page_extension}')

        await message.answer(file_name)

        # if page is loaded succesfully, no need for Menu.loading_page state
        await state.set_state(Menu.menu)
    
    except GettingChapterPageDescriptionError:
        await message.answer(BOT_MESSAGES['errors']['format_error'])
        
    except PathExistsError:
        await message.answer(BOT_MESSAGES['menu']['page_already_exists'])

    except Exception:
            await message.answer(BOT_MESSAGES['errors']['loading_error'])
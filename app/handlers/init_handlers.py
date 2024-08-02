from site import addusersitepackages
from aiogram import Bot, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, or_f

from yadisk.exceptions import DirectoryExistsError

from databases.requests import check_regestration, add_user_to_DB,\
                                update_current_format_DB, update_current_manga_DB, \
                                get_current_manga_format_from_DB

from keyboards.inline_kbs import create_formats_kb, create_mangas_kb
from keyboards.reply_kbs import create_placeholder_kb
from utils.CONSTANTS import BOT_MESSAGES
from utils.states import Init, Menu
from utils.keyboards_utils import handle_inline_keyboard
from utils.ya_disk_api import create_manga_folder

init_router = Router()

@init_router.message(or_f(CommandStart(), Command('init')))
async def start(message: Message, state: FSMContext):
    await state.set_state(Init.init)

    if (not await check_regestration(message.from_user.id)):
        await add_user_to_DB(tg_id=message.from_user.id)

    user_data = await get_current_manga_format_from_DB(tg_id=message.from_user.id)
    current_manga = user_data['current_manga']
    
    await message.answer(BOT_MESSAGES['init']['greeting'],
                                    reply_markup=create_placeholder_kb(current_manga)) 
    await message.answer(BOT_MESSAGES['init']['choose_format'],
                                    reply_markup=create_formats_kb())


@init_router.callback_query(Init.init, F.data.startswith('format_'))
async def set_format(callback: CallbackQuery, state: FSMContext):
    await handle_inline_keyboard(callback)

    await update_current_format_DB(tg_id=callback.from_user.id, current_format=callback.data.split('_')[-1])

    await callback.message.answer(BOT_MESSAGES['init']['choose_manga'],
                                  reply_markup=create_mangas_kb())


@init_router.callback_query(Init.init, F.data.startswith('manga_'))
async def set_manga(callback: CallbackQuery, state: FSMContext):
    await handle_inline_keyboard(callback)

    manga_name = ' '.join(callback.data.split('_')[1:])
    await update_current_manga_DB(tg_id=callback.from_user.id, current_manga=manga_name)
    await state.set_state(Menu.menu)

    await callback.message.answer(BOT_MESSAGES['init']['init_end'],
                                  reply_markup=create_placeholder_kb(manga_name))


@init_router.callback_query(Init.init, F.data == 'create_new_manga')
async def start_creating_new_manga(callback: CallbackQuery, state: FSMContext):
    await handle_inline_keyboard(callback)

    await state.set_state(Init.new_manga)

    await callback.message.answer(BOT_MESSAGES['menu']['create_new_manga']) 
    
@init_router.message(Init.new_manga, F.text)
async def create_new_manga(message: Message, state: FSMContext):
    try:
        await update_current_manga_DB(tg_id=message.from_user.id, current_manga=message.text)
        await state.set_state(Menu.menu)

        create_manga_folder(message.text)
        
        await message.answer(BOT_MESSAGES['init']['init_end'],
                                reply_markup=create_placeholder_kb(message.text))
        
    except DirectoryExistsError:
        await message.answer(BOT_MESSAGES['errors']['new_manga_already_exists_error'])

    except Exception:
        await message.answer(BOT_MESSAGES['errors']['new_manga_error'])
from aiogram.exceptions import TelegramBadRequest

# Удаляет reply_markup и добавляет текст в текущее сообщение сообщение
async def handle_inline_keyboard(callback, *, text='',new_line_count=2, new_markup=None):
    try:
        await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id, 
            text=callback.message.text + '\n'*new_line_count + (text or get_inline_button_text(callback)))
        
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id, 
            reply_markup=new_markup)
    
    except TelegramBadRequest:
        pass

# Достает текст inline-кнопки
def get_inline_button_text(callback):
    inline_kb = callback.message.reply_markup.inline_keyboard
    callback_data = callback.data
    for row in inline_kb:
        for button in row:
            if button.callback_data == callback_data:
                return button.text
    return callback_data
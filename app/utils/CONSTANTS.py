
LINUX_MANGA_FOLDER_PATH = '/home/daniil-mint/Documents/MangaPagesBot-main/app/assets/manga pages'
WINDOWS_MANGA_FOLDER_PATH = 'C:/Users/Ford/Local Projects/MangaBot/app/assets/manga pages'
PC_MANGA_FOLDER_PATH = LINUX_MANGA_FOLDER_PATH # change for your system

DISK_MANGA_FOLDERS_PATH = '/Manga'

PAGE_DESCRIPTION_FORMATS = [
    'c1p1 [description]',
    '1.1 [description]'
]

BOT_MESSAGES = {
    'errors': {
            'general_error': 'Извините, что-то пошло не так(',
            'format_error': 'Неверный формат подписи страницы. Напишите описанание страницы ещё раз.',
            'loading_error': 'Не удалось загрузить страницу. Попробуйте еще раз.',
            'new_manga_already_exists_error': 'Извините, данная манга уже существует. Напишите новое название:',
            'page_already_exists_error': 'Страница с подобными данными уже существует. Пожалуйста, напишите другое описание.',
            'no_user_account': 'Похоже, вас нет в базе данных и мы не может узать необходимую информацию (формат )',
            'wrong_local_dir': 'Похоже, неправильно указа папка, в которой должен сохраняться временный файл. \
                Убедитесь, что путь в файле CONSTANTS указан правильно',

    },
    'init': {
        'greeting': 'Добро пожаловать в Manga Pages Bot',
        'choose_format': 'Выберите формат для подписи страниц манги:\n',
        'choose_manga': 'Выберите папку с мангой, которую вы сейчас читаете, или создайте новую:\n',
        'init_end': 'Хорошо, теперь вы можете сохранять страницы из своей манги! 🎉'
    },
    'menu': {
        'main': 'Вот что вы можете сейчас сделать:\n',
        'change_manga': 'Вот ваша манга: \n',    
        'manga_changed': 'Вы выбрали мангу: ',
        'change_format': 'Вот возможные форматы описания: \n',
        'format_changed': 'Вы выбрали формат: ',
        'create_new_manga': 'Напишите название новой манги:',
        'new_manga_created': 'Новая манга создана!',
    },
    'loading': {
        'page_loaded': 'Вы успешно загрузили страницу:\n' 
    }
}

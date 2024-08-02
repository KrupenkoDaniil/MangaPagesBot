import os, yadisk

from utils.CONSTANTS import DISK_MANGA_FOLDERS_PATH, PC_MANGA_FOLDER_PATH

YA_TOKEN = os.getenv('YA_TOKEN')
y = yadisk.YaDisk(token=YA_TOKEN)
       
def check_token() -> bool:
    if (not y):
        raise Exception('Your haven\'t logged in yandex disk.')
    if (not y.check_token()):
        raise Exception('Your token is not valid.')
    return True

def get_mangas_names() -> list[str]:
    mangas_list = list(y.listdir(DISK_MANGA_FOLDERS_PATH))
    mangas_names_list = list(map(get_manga_name, mangas_list))
    return mangas_names_list

def get_manga_name(manga_obj:dict) -> str:
    return manga_obj['path'].split('/')[-1]

def create_manga_folder(manga_name:str) -> None:
    y.mkdir(f'{DISK_MANGA_FOLDERS_PATH}/{manga_name}')
    
def upload_page(file_name:str, file_extension:str, current_manga: str) -> None:
    y.upload(f'{PC_MANGA_FOLDER_PATH}/temp.{file_extension}', f'{DISK_MANGA_FOLDERS_PATH}/{current_manga}/{file_name}')
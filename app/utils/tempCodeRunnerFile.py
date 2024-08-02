
from utils.errors import GettingChapterPageDescriptionError

def get_chapter_page_description(page_caption:str, current_format) -> list[str]:
    if(not page_caption):
        raise GettingChapterPageDescriptionError()

    result = []
    chapter_page = page_caption.split(' ')[0]
    if (len(page_caption.split(' ')) > 1):
        description = ' '.join(page_caption.split(' ')[1:])
        description = f'({description})'
    else:
        description = '' 

    match current_format:
        case '1.1':
            result = chapter_page.split('.')
        case 'c1p1':
            if (not chapter_page[0] == 'c'):
                raise GettingChapterPageDescriptionError()
            if (not len(chapter_page.split('p') == 2)):
                raise GettingChapterPageDescriptionError()
            chapter_page = chapter_page.replace('c', '')
            result = chapter_page.split('p')
    
    result.append(description)
    return result


print(get_chapter_page_description('11', '1.1'))
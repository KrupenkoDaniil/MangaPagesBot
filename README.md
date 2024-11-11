Телеграмм-бот для загрузки отправленных ему страниц из манги на YandexDisk.
## Работа с ботом
### Общие принципы работы:
+ функция создания новых папок под мангу
+ выбор текущей папки с мангой
+ загрузка новых страниц для текущей манги
+ выбор формата для загрузки страницы манги

### Инициализация ( /start , /init )
+ пользователь входит через yandex OAuth (❌)
  + ❌ при неверном токене  отправляется сообщение об ошибке
  + ✅ при верном токене отправляется сообщее от успехе входа
+ пользователь либо находится в базе данных, либо добавляется туда
+ пользователь выбирает папку с мангой из текущих или создает новую
  + после выбора манги метяется placeholder
  + при выборе "создания манги" нужно вписать ее название, после чего она автоматически выберется
  + ❌ если при создании манги введенное название уже существует, бот просит отправить другое название 
  + при выборе/добавлении манги, она обновляется в бд

### Меню ( /menu )
+ раздел для выбора/создания папки с мангой (работает так же, как при инициализации)
  + после выбора манги метяется placeholder
  + при выборе "создания манги" нужно вписать ее название, после чего она автоматически выберется
  + ❌ если при создании манги введенное название уже существует, бот просит отправить другое название
  + при выборе/добавлении манги, она обновляется в бд
+ изменение формата для загрузки страницы (то, как бот будет определять номер главы, номер страницы и описание *(опционально)*)

### Загрузка страницы ( F.photo )
+ бот получает фото нужной страницы
  + каждая новая фотография прерывает предыдущую заргрузку
+ считывает ее описание в соответствии с выбраным форматом
  + ❌ если описание не соответствует формату, бот просит отправить описание повторно (страницу дублировать не обязательно)
+ загружает страницу на YandexDisk
  + ❌ возможные ошибки:
  	+ если страница **уже существует**, бот просит отправить другое описание
  	+ если не удалось **загрузить страницу**, отправляется сообщение об ошибке
  + ✅ при успехе отправляет сообщение об успехе с указанием текущей манги и данными о новой странице

## Установка проекта:
+ Скачать и экспортировать файл с проектом.
+ Создать среду разработки и установить необходимые модули (*pip install -r requirements.txt*)
+ Создать файл .env и добавить туда переменные:
  + TG_TOKEN: токен вашего тг-бота; можно найти у [**@BotFather**](https://t.me/BotFather)
  + YA_TOKEN: токен вашего яндекс приложения; для этого создайте [**яндекс id**](https://oauth.yandex.ru/client/new/id) и узнайте свой токет по такому шаблону:
```
https://oauth.yandex.ru/authorize?response_type=token&client_id=ВАШ CLIEN_ID
```
+ Уточните путь для верменного изображеия в **файле CONSTANTS** в зависимости от вашей ОС; 
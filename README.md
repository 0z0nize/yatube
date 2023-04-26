![233348780-313ad8af-8fa5-47cve0-x8cvfd1c-7f0aea8c24a122](https://user-images.githubusercontent.com/112638163/234638661-8310f7ed-24ae-44af-aef4-69b517aec740.png)

# Соцсеть Yatube

Социальная сеть блогеров. Повзоляет написание постов и публикации их в отдельных группах, подписки на посты, добавление и удаление записей и их комментирование.
Подписки на любимых блогеров.

## Инструкции по установке
***- Клонируйте репозиторий:***
```
git clone git@github.com:0z0nize/yatube.git
```

***- Установите и активируйте виртуальное окружение:***
- для MacOS
```
python3 -m venv venv
source venv/bin/activate
```
- для Windows
```
python -m venv venv
source venv/Scripts/activate
```

***- Установите зависимости из файла requirements.txt:***
```
pip install -r requirements.txt
```

***- Примените миграции:***
```
python manage.py migrate
```

***- В папке с файлом manage.py выполните команду:***
```
python manage.py runserver
```

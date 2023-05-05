![233348780-313ad8af-8fa5-47cve0-x8cvfd1c-7f0aea8c24a122](https://user-images.githubusercontent.com/112638163/234638661-8310f7ed-24ae-44af-aef4-69b517aec740.png)

### Описание

Социальная сеть блогеров. Повзоляет написание постов и публикации их в отдельных группах, подписки на посты, добавление и удаление записей и их комментирование.
Подписки на любимых блогеров.

### Технологии
![python version](https://img.shields.io/badge/Python-3.9.10-yellowgreen?logo=python)
![django version](https://img.shields.io/badge/Django-3.2.16-yellowgreen?logo=django)
![Pillow version](https://img.shields.io/badge/Pillow-8.3.1-yellowgreen?logo=pillow)
![sorl-thumbnail version](https://img.shields.io/badge/sorl_thumbnail-12.7.0-yellowgreen?logo=sorl-thumbnail)
![requests version](https://img.shields.io/badge/requests-2.26.0-yellowgreen)
![pytest version](https://img.shields.io/badge/pytest-6.2.4-yellowgreen?logo=pytest)

### Как запустить проект

Клонируйте репозиторий:
```
git clone git@github.com:0z0nize/yatube.git
```

Установите и активируйте виртуальное окружение:
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
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Примените миграции:
```
python manage.py migrate
```
В папке с файлом manage.py выполните команду:
```
python manage.py runserver
```

### Автор проекта:
#### [_Владислав Шкаровский_](https://github.com/0z0nize)


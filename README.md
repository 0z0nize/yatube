![YaTube2](https://user-images.githubusercontent.com/112638163/236888213-965b263c-61ea-4d08-9483-78e3d8456a24.png)

### Описание
Социальная сеть блогеров YaTube - позволяет писать и публиковать посты в отдельных группах, добавлять и удалять записи и подписываться на любимых блогеров.
* Есть возможность добавлять комментарии к постам других пользователей. На странице поста под текстом записи выводится форма для отправки комментария, а ниже — список комментариев. 
* Комментировать могут только авторизованные пользователи. 
* Список постов на главной странице сайта хранится в кэше и обновляется раз в 20 секунд.
* Присутсвует система подписки на авторов и создана лента их постов.
* Настроен эмулятор отправки писем
    - отправленные письма сохраняются в виде текстовых файлов в директорию /sent_emails
    - настроена отправка письма при восстановлении пароля
* Созданы кастомные страницы для ошибок
    - 404 Page not found
    - 403 Forbidden
    - 403 CSRF
    - 500 Internal Server Error
* Написаны тесты проверяющие работу сервисов


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

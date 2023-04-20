![social](https://user-images.githubusercontent.com/112638163/233350906-a5eaa239-f73e-4ae6-84d4-10a873f6b3b0.png)

# Соцсеть Yatube

Социальная сеть блогеров. Повзоляет написание постов и публикации их в отдельных группах, подписки на посты, добавление и удаление записей и их комментирование.
Подписки на любимых блогеров.

## Инструкции по установке
***- Клонируйте репозиторий:***
```
git clone git@github.com:PashkaVRN/hw05_final.git
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

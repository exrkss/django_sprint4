# Описание.

## Проект django_sprint4.

## Технологии:
* Python 3.7
* Django 3.2
* SQlite3

## Описание проекта

Доработка проекта django_sprint3.
Финальная версия небольшой социальной сети для публикации личных дневников. 

## Как запустить проект:

* Клонировать репозиторий и перейти в него в командной строке:

        git clone git@github.com:ANTIWARFIX/yan4
        cd yan4

* Cоздать и активировать виртуальное окружение:

        python -m venv venv
        source venv/Scripts/activate

* Установить зависимости requirements.txt:

        python -m pip install --upgrade pip
        pip install -r requirements.txt

* Выполнить команду:

        python manage.py migrate


* Запустить проект:

        python manage.py runserver

* Запустить локальный сервер:

        http://127.0.0.1:8000/

# Вебсайт тлумачного словника ІТ-термінів

Кваліфікаційний проєкт на тему: **«Розробка вебсайту тлумачного словника інформаційно-комп'ютерних термінів»**.

## Реалізований функціонал

- каталог термінів із пошуком і фільтрацією за категоріями;
- сторінка окремого терміна з повним визначенням;
- перегляд категорій і вмісту категорій;
- форма пропозиції нового терміна;
- інформаційна сторінка про проєкт;
- адміністративна панель Django для повного CRUD.

## Технологічний стек

- Python 3.14
- Django 6
- SQLite
- HTML + CSS

## Швидкий старт

1. Створити віртуальне оточення:
   - `python -m venv .venv`
2. Встановити залежності:
   - `.venv\Scripts\python -m pip install -r requirements.txt`
3. Виконати міграції:
   - `.venv\Scripts\python manage.py migrate`
4. Завантажити тестові дані:
   - `.venv\Scripts\python manage.py loaddata dictionary/fixtures/initial_data.json`
5. Запустити сервер:
   - `.venv\Scripts\python manage.py runserver`
6. Відкрити сайт:
   - `http://127.0.0.1:8000/`

## Налаштування для публічного репозиторію

Проєкт читає базові параметри Django з змінних середовища:

- `DJANGO_SECRET_KEY` - секретний ключ (обов'язково змінити для продакшну);
- `DJANGO_DEBUG` - режим налагодження (`True` або `False`);
- `DJANGO_ALLOWED_HOSTS` - список хостів через кому (наприклад: `127.0.0.1,localhost,example.com`).

Приклад для PowerShell:

- `$env:DJANGO_SECRET_KEY="your-strong-secret-key"`
- `$env:DJANGO_DEBUG="False"`
- `$env:DJANGO_ALLOWED_HOSTS="example.com,www.example.com"`

## Тестування

Запуск автоматизованих тестів:

- `.venv\Scripts\python manage.py test`

## Документація кваліфікаційної роботи

- `docs/Кваліфікаційна_робота.docx`
- `docs/Додатки.docx`

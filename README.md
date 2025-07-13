# РИДМИ БРИДМИ

Здесь мы прям жёёёёёска размещаем 1 рецепт

Скачайте код с GitHub. Установите зависимости:
```
pip install -r requirements.txt
```

Создайте файл `.env` в корне проекта и укажите необходимые переменные окружения:
```
SECRET_KEY=your_secret_key_here
DEBUG=true
BOT_TG_TOKEN=your_bot_tg_token_here
```

Создайте базу данных SQLite:
```
python manage.py migrate
```
Запустите сервер:
```
python manage.py runserver
```

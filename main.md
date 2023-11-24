## Инструкция по локальному развертыванию проекта

Для работы проекта потребуются:

- Python
- DRF
- Django
- Telegram-bot
    
Проект содержит в себе requirements.txt


1. Клонировать проект:
    ```
    git clone https://github.com/EchoFoe/traffic_light.git
    ```

2. Создать виртуальную среду и установить в неё зависимости:
    ```
    pip install -r requirements.txt
    ```


3. Произвести миграции:
    ```
    python manage.py migrate
    ```


4. Запустить daphne:
    ```
    daphne traffic_light.asgi:application
    ```


5. Запустить локальный сервер:
    ```
    python manage.py runserver
    ```

6. Запустить тесты:
    ```
    python manage.py test --settings=traffic_light.settings_test
    ```
    

Проект успешно развернут, если все тесты прошли.
### Проверить АПИ можно по адресу: 
    ```
    http://localhost:8000/api/weather/?city=минск
    ``` 
(запросить можете любой другой город)
### Найти бота в ТГ можно так:
    ```
    https://t.me/l_weather_echo_bot
    ```

Если тесты не проходят или испытываете трудности по запуску сервера разработки, закомментируйте строки:
    ```
    updater.bot.deleteWebhook()
    updater.start_polling()
    updater.idle()
    ``` в weather/views.py
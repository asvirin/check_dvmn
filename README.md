# Telegram-bot DVMN
Бот для Telegram, который присылает уведомления о проверке заданий от проекта devman. Бот постоянно запущен и проверяет наличие новых проверок. В зависимости от результатов проверок, присылаются разные сообщения. Также в боте присутствуют системные уведомления об ошибках, которые также приходят пользователю. 

# Как установить
### Этап 1. Для запуска бота необходимо получить ключи от нескольких сервисов
1) Создать бота в telegram через [Отца ботов](https://telegram.me/BotFather) и взять токен для авторизации.
2) Узнать свой ID через [специального бота](https://telegram.me/userinfobot).
3) Узнать токен для авторизации сервиса devman в документации по [API](https://dvmn.org/api/docs/).

### Этап 2. Установить переменные окружения
1) telegram_token — переменная для токена от телеграм-бота;  
2) chat_id — переменная, в которую нужно записать кому присылать сообщения;  
3) dvmn_api_token — переменная для токена авторизации от API Devman.  

Все переменные записаны в ifmain.

### Этап 3. Запустить бота. Пример запуска
```python
python3 main.py
```
# Требования
Все требуемые модули указаны в файле requirements.txt  
Для установки запустите команду:
```python
python3 pip install -r requirements.txt
```

# Требования к запуску на Heroku
Для запуска на Heroku необходимы файлы Procfile и Pipfile:
1) В файле Procfile прописано какой файл нужно запускать на Heroku.
2) В файлах Pipfile и reqirements.txt указаны необходимые модули для работы бота.

# Автор бота
Алексей Свирин  
Телеграм — [@svirin](https://telegram.me/svirin)

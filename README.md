# Telegram-bot DVMN
Бот для Telegram, который присылает уведомления о проверке заданий от проекта devman.

# Как установить
Бот написан специально под сервис Heroku. Для запуска бота необходимо:  
1) Создать бота в telegram через [Отца ботов](https://telegram.me/BotFather) и взять ключ для авторизации.
2) Узнать свой ID через [специального бота](https://telegram.me/@userinfobot).
3) Узнать ключ для авторизации сервиса devman в документации по [API](https://dvmn.org/api/docs/).
4) На Heroku ключи добавляются на вкладке Settings. Если запускать в другом месте, то ключи необходимо поместить в функции: MyLogsHandler, send_messages и get_status_homework. 

# Требования
1) В файле Procfile прописано какой файл нужно запускать на Heroku.
2) В файлах Pipfile и reqirements.txt указаны необходимые модули для работы бота.

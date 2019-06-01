import os
import requests
import time
import telegram
import logging 

def send_message(message, bot):
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    
def handle_response(answer, bot):
    if answer['status'] == 'timeout':
        return answer['timestamp_to_request']
    
    lesson_title = answer['new_attempts'][0]['lesson_title']
    lesson_url = 'https://dvmn.org{}'.format(answer['new_attempts'][0]['lesson_url'])
    status_answer = answer['new_attempts'][0]['is_negative']
    
    if status_answer:
        message = 'Задача "{}" проверена, но есть ошибки( \n[Ссылка на задачу]({})'.format(lesson_title, lesson_url)
    else:
        message = 'Задача проверена, ошибок нет!'

    send_message(message, bot)
    return answer['last_attempt_timestamp']
    
def request_new_attempts(timestamp, bot):
    url = 'https://dvmn.org/api/long_polling/'
    params = {'timestamp': timestamp}
    headers = {'Authorization': dvmn_api_token}
    
    response = requests.get(url, headers=headers, params=params)
    answer = response.json()
        
    try:
        response.raise_for_status()
        return handle_response(answer, bot)
    except requests.exceptions.HTTPError:
        message = 'Ошибка при запросе статуса задачи: {}'.format(answer)
        send_message(message, bot)
        time.sleep(3600)
    
if __name__ == '__main__':
    timestamp = int(time.time())
    
    dvmn_api_token = os.environ['authorization_token_dvmn']
    
    telegram_token = os.environ['telegram_token']
    chat_id = os.environ['chat_id']
    bot = telegram.Bot(token=telegram_token)
    
    class MyLogsHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            bot.send_message(chat_id=chat_id, text=log_entry)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    
    logger.info("Бот запущен")

    while True:
        try:
            timestamp = request_new_attempts(timestamp, bot)
        except (requests.exceptions.ReadTimeout, requests.ConnectionError):
            continue
        except Exception:
            logger.exception('Возникла ошибка ↓')
            time.sleep(14400)

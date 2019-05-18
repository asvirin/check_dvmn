from dotenv import load_dotenv
import os
import requests
import time
import telegram
    
def send_message(answer):
    bot = telegram.Bot(token=os.getenv("telegram_token"))
    chat_id = os.getenv("chat_id")
    
    lesson_title = answer['new_attempts'][0]['lesson_title']
    lesson_url = 'https://dvmn.org{}'.format(answer['new_attempts'][0]['lesson_url'])
    status_answer = answer['new_attempts'][0]['is_negative']
    
    if status_answer is True:
        message = 'Задача "{}" проверена, но есть ошибки( \n*Ссылка*: {}'.format(lesson_title, lesson_url)
    elif status_answer is False:
        message = 'Задача проверена, ошибок нет!'
    
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
        
    
def get_status_homework(timestamp):
    bot = telegram.Bot(token=os.getenv("telegram_token"))
    chat_id = os.getenv("chat_id")
    
    url = 'https://dvmn.org/api/long_polling/'
    params = {'timestamp': timestamp}
    headers = {'Authorization': os.getenv("authorization_token_dvmn")}
    
    response = requests.get(url, headers=headers, params=params)
    answer = response.json()
    
    if response.ok is False:
        raise requests.exceptions.HTTPError(bot.send_message(chat_id=chat_id, \
                                                             text='Ошибка при запросе: {}'.format(answer)))
    elif answer['status'] == 'timeout':
        return answer['timestamp_to_request']
    else:
        send_message(answer)
        return answer['last_attempt_timestamp']
    
if __name__ == '__main__':
    timestamp = int(time.time())
    while True:
        try:
            timestamp = get_status_homework(timestamp)
        except requests.exceptions.ReadTimeout:
            timestamp = get_status_homework(timestamp)
        except requests.ConnectionError:
            timestamp = get_status_homework(timestamp)
    

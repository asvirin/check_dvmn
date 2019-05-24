#!/usr/bin/env python
import os
import requests
import time
import telegram
import logging

def send_message(message):
    bot = telegram.Bot(token=os.environ['telegram_token'])
    chat_id = os.environ['chat_id']
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
    
def get_text_answer(answer):
    if answer['status'] == 'timeout':
        return answer['timestamp_to_request']
    
    lesson_title = answer['new_attempts'][0]['lesson_title']
    lesson_url = 'https://dvmn.org{}'.format(answer['new_attempts'][0]['lesson_url'])
    status_answer = answer['new_attempts'][0]['is_negative']
    
    if status_answer:
        message = 'Задача "{}" проверена, но есть ошибки( \n*Ссылка*: {}'.format(lesson_title, lesson_url)
    else:
        message = 'Задача проверена, ошибок нет!'
    
    send_message(message)
    return answer['last_attempt_timestamp']
    
def get_status_homework(timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    params = {'timestamp': timestamp}
    headers = {'Authorization': os.environ['authorization_token_dvmn']}
    
    response = requests.get(url, headers=headers, params=params)
    answer = response.json()
    
    try:
        response.raise_for_status()
        return get_text_answer(answer)
    except requests.exceptions.HTTPError:
        message = 'Ошибка при запросе статуса задачи: {}'.format(answer)
        send_message(message)
        time.sleep(1800)
    
if __name__ == '__main__':
    logging.warning('Бот запущен')
    timestamp = int(time.time())
    while True:
        try:
            timestamp = get_status_homework(timestamp)
        except (requests.exceptions.ReadTimeout, requests.ConnectionError):
            continue

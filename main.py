from dotenv import load_dotenv
import os
import requests
import time
import telegram

def get_status_homework():
    url = 'https://dvmn.org/api/long_polling/'
    response = requests.get(url, headers=headers, params=params)
    answer = response.json()
    
    if answer['error'] in answer:
        raise requests.exceptions.HTTPError(bot.send_message(chat_id=chat_id, \
                                                             text='Ошибка при запросе: {}'.format(answer['error'])))
    status_answer = answer['status']
    
    if status_answer == 'timeout':
        timestamp = answer['timestamp_to_request']
    elif status_answer == 'found' and answer['solution_attempts']['is_negative'] is True:
        bot.send_message(chat_id=chat_id, text='Задача проверена, но есть ошибки(')
    elif status_answer == 'found' and answer['solution_attempts']['is_negative'] is False:
        bot.send_message(chat_id=chat_id, text='Задача проверена, ошибок нет!')
    
    
if __name__ == '__main__':
    telegram_token = os.getenv("telegram_token")
    authorization_token_dvmn = os.getenv("authorization_token_dvmn")
    chat_id = os.getenv("chat_id")
    
    headers = {'Authorization': authorization_token_dvmn}
    params = {'timestamp': timestamp}
    timestamp = int(time.time()) 
    bot = telegram.Bot(token=telegram_token)
        
    while True:
        try:
            get_status_homework()
        except requests.exceptions.ReadTimeout:
            get_status_homework()
        except requests.ConnectionError:
            get_status_homework()

import types
import telebot
import conf
import json
import requests

user = conf.user
psw = conf.psw
urlCS = conf.urlCS
urlBalance = conf.urlBalance
bot = telebot.TeleBot(conf.token)
admin_login = 'root'
admin_pass = 'root@123'
start_login = ''
start_pass = ''

#######################################################################################################################

@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Введите ваш логин:')
        bot.register_next_step_handler(message, start_l)

    elif message.text == '/admin':
        bot.send_message(message.from_user.id, '# input user')
        bot.register_next_step_handler(message, admin_l)
    else:
        bot.send_message(message.chat.id, 'Для начала работы нажмите /start')


def start_l(message):
    global start_login
    start_login = message.text
    bot.send_message(message.from_user.id, 'Введите пароль от ЛК:')
    bot.register_next_step_handler(message, start_p)

def start_p(message):
    global start_pass
    start_pass = message.text

    headersCS = {'Content-type': 'application/json',
                 'Accept': 'text/plain',
                 'Content-Encoding': 'utf-8'}
    dataCS = {"method": "contractList",
              "user": {"user": user, "pswd": psw},
              "params": {
                  "title": start_login,
                  "fc": -1,
                  "groupMask": 0,
                  "subContracts": 'false',
                  "closed": 'true',
                  "hidden": 'false',
                  "page": {}
              }}
    answer = requests.post(urlCS, data=json.dumps(dataCS), headers=headersCS)
    responseCS = answer.json()

    try:
        CID = str(responseCS['data']['return'][0]['id'])
        stat = str(responseCS['data']['return'][0]['status'])
        group = str(responseCS['data']['return'][0]['groups'])
        limit = str(responseCS['data']['return'][0]['balanceLimit'])
        passwordLK = str(responseCS['data']['return'][0]['password'])
        loginLK = str(responseCS['data']['return'][0]['title'])

        # Получаем баланс по contractID

        headersBalance = {'Content-type': 'application/json',
                          'Accept': 'text/plain',
                          'Content-Encoding': 'utf-8'}
        dataBalance = {"method": "balanceDetailList",
                       "user": {"user": user, "pswd": psw},
                       "params": {
                           "contractId": CID,
                           "period": {},
                           "available": 'false'
                       }}

        answer = requests.post(urlBalance, data=json.dumps(dataBalance), headers=headersBalance)
        responseB = answer.json()
        balance = str(responseB['data']['return'][-1]['sumAfterChange'])

        if int(stat) == 0:
            stat = "Активен"
        elif int(stat) == 4:
            stat = "Приостановлен"
        elif int(stat) == 2:
            stat = "Отключен"
        else:
            stat = stat

        if start_pass == passwordLK:
            bot.send_message(message.chat.id, "Статус : " + stat + '\n' + "Лимит : "
                             + limit + '\n' + "Баланс : " + balance)
        else:
            bot.send_message(message.from_user.id, 'Неправильно введён пароль')

    except IndexError:
        bot.send_message(message.chat.id, "Неправильно введен логин")

def admin(message):
    bot.send_message(message.from_user.id, '2')

def admin_l(message):
    if message.text == admin_login:
        bot.send_message(message.from_user.id, '# input pass')
        bot.register_next_step_handler(message, admin_p)
    else:
        bot.send_message(message.from_user.id, '# user failure')
        menu(message)

def admin_p(message):
    if message.text == admin_pass:
        bot.send_message(message.from_user.id, '# Введи логин:')
        bot.register_next_step_handler(message, admin_code)
    else:
        bot.send_message(message.from_user.id, '# pass failure')
        menu(message)

def admin_code(message):
    headersCS = {'Content-type': 'application/json',
                 'Accept': 'text/plain',
                 'Content-Encoding': 'utf-8'}
    dataCS = {"method": "contractList",
              "user": {"user": user, "pswd": psw},
              "params": {
                  "title": message.text,
                  "fc": -1,
                  "groupMask": 0,
                  "subContracts": 'false',
                  "closed": 'true',
                  "hidden": 'false',
                  "page": {}
              }}
    answer = requests.post(urlCS, data=json.dumps(dataCS), headers=headersCS)
    responseCS = answer.json()

    try:
        CID = str(responseCS['data']['return'][0]['id'])
        stat = str(responseCS['data']['return'][0]['status'])
        group = str(responseCS['data']['return'][0]['groups'])
        limit = str(responseCS['data']['return'][0]['balanceLimit'])
        passwordLK = str(responseCS['data']['return'][0]['password'])
        loginLK = str(responseCS['data']['return'][0]['title'])

        # Получаем баланс по contractID

        headersBalance = {'Content-type': 'application/json',
                          'Accept': 'text/plain',
                          'Content-Encoding': 'utf-8'}
        dataBalance = {"method": "balanceDetailList",
                       "user": {"user": user, "pswd": psw},
                       "params": {
                           "contractId": CID,
                           "period": {},
                           "available": 'false'
                       }}

        answer = requests.post(urlBalance, data=json.dumps(dataBalance), headers=headersBalance)
        responseB = answer.json()
        balance = str(responseB['data']['return'][-1]['sumAfterChange'])

        #        bot.send_message(message.chat.id, "Ваш баланс: " + balance + "/n" + status + "/n" + group + "/n" + limit)

        # bot.send_message(message.chat.id, "Логин : " + loginLK)
        # bot.send_message(message.chat.id, "Статус : " + stat)
        # bot.send_message(message.chat.id, "Лимит : " + limit)
        # bot.send_message(message.chat.id, "Группа : " + group)
        # bot.send_message(message.chat.id, "Баланс : " + balance)
        # bot.send_message(message.chat.id, "Пароль ЛК : " + passwordLK)

        if int(stat) == 0:
            stat = "Активен"
        elif int(stat) == 4:
            stat = "Приостановлен"
        elif int(stat) == 2:
            stat = "Отключен"
        else:
            stat = stat

        if int(group) == 276:
            group = "Демир"
        elif int(group) == 272:
            group = "Главный"
        elif int(group) == 288:
            group = "Акушинский"
        elif int(group) == 258:
            group = "Гамидова"
        else:
            group = "unknow (" + group + ")"

        bot.send_message(message.chat.id,
                         "Логин : " + loginLK + '\n' + "Статус : " + stat
                         + '\n' + "Лимит : " + limit + '\n' + "Группа : " + group
                         + '\n' + "Баланс : " + balance + '\n' + "Пароль ЛК : " + passwordLK)

    except IndexError:
        bot.send_message(message.chat.id, "Неправильно введен логин")

    if message.text != '/stop':
        bot.register_next_step_handler(message, admin_code)
    else:
        bot.send_message(message.chat.id, "Вы вышли из администраторского режима")
        menu(message)

    # print(stat)
    # print(loginLK)
    # print(limit)
    # print(group)
    # print(balance)
    # print(passwordLK)


#######################################################################################################################

if __name__ == '__main__':
    bot.polling(none_stop=True)

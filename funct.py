import conf
import json
import requests

loginG = ''
passwordG = 0
user = conf.user
psw = conf.psw
urlCS = conf.urlCS
urlBalance = conf.urlBalance

#######################################################################################################################

def loginLK():
    x = input('Веведите логин: ')
    print(x)
    global loginG
    loginG = x
    passwordLK()

def passwordLK():
    y = input('Введите пароль: ')
    print(y)
    global passwordG
    passwordG = y
    code()

def code():

    global loginG
    global passwordG

    headersCS = {'Content-type': 'application/json',  # Определение типа данных
                 'Accept': 'text/plain',
                 'Content-Encoding': 'utf-8'}
    dataCS = {
        "method": "contractList",
        "user": {"user": user, "pswd": psw},
        "params": {
            "title": loginG,
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
        pas = str(responseCS['data']['return'][0]['password'])

        #################################################################################################################

        headersBalance = {'Content-type': 'application/json',  # Определение типа данных
                          'Accept': 'text/plain',
                          'Content-Encoding': 'utf-8'}
        dataBalance = {
            "method": "balanceDetailList",
            "user": {"user": user, "pswd": psw},
            "params": {
                "contractId": CID,
                "period": {},
                "available": 'false'
            }}

        answer = requests.post(urlBalance, data=json.dumps(dataBalance), headers=headersBalance)
        responseB = answer.json()

    except IndexError:
        print("Ошибка")
    try:
        balance = str(responseB['data']['return'][-1]['sumAfterChange'])
    except:
        print('Неправильно введен логин или пароль')


    # float(balance)
    # x = round(balance, 2)


    if pas == passwordG:
        print("-----------------------------------")
        print("Баланс:" + balance)
    else:
        print('Пароль введен неверный!')

loginLK()

#######################################################################################################################
#
# if __name__ == '__main__':
#     bot.polling(none_stop=True)

"""Описание:
Сделать телеграм бота для обмена валюты
Данные должны быть спарсены с сайта НАЦбанка (USD, EURO, RUB, KZT)
https://www.nbkr.kg/index.jsp?lang=RUS
Пользователь:
Пользователь пишет боту и выбирает валюту которую нужно поменять,
например KGS на USD и вы пишете 100 и получаете 8572 сом (примерно по
курсу валюты)
ДОП ЗАДАНИЕ:
Попробуйте сделать бота с использованием inline кнопок
Загрузить код в GitHub с .gitignore"""

import requests
from bs4 import BeautifulSoup


def parsing_aki():
    url = "https://akipress.org/"
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.text)
    news =soup.find_all("a", class_="newslink")

    for b in enumerate(news) :
        with open('st.txt', 'a+',encoding="utf-8") as f:
            f.write(f"{str(b)}\n")

def parsing_currency():
        url = "https://www.nbkr.kg/index.jsp?lang=RUS"
        response = requests.get(url)
        soup = BeautifulSoup(response.text,"lxml")
        currency = soup.find_all("td",class_='exrate')
        # print(currency)
        for usd in currency[0:2]:
            print(usd.txt)
        print("==========")
        for euro in currency[2:4]:
            print(euro.txt)
        print("==========")
        for rub in currency[4:6]:
            print(rub.txt)
        print("==========")
        for kzt in currency[4:6]:
            print(kzt.txt)
        print("==========")
parsing_currency()
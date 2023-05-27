from dotenv import load_dotenv
from aiogram.types import KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup
import os,sqlite3,time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
import requests
from bs4 import BeautifulSoup
from state import DollarSom,SomDollar,EuroSom,SomEuro
from states import *
url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
currency = soup.find_all('td', class_='exrate')
usds = currency[0].text.replace(",", ".")
euros = currency[2].text.replace(",", ".")
rubs = currency[4].text.replace(",", ".")
kzts = currency[6].text.replace(",", ".")
# print (usds,rubs,euros,kzts)
 



load_dotenv('.env')
bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    username VARCHAR(150),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created VARCHAR(200)
);
""")
cursor.connection.commit()


inline_buttons1 = [
    InlineKeyboardButton('Курсы валют',callback_data='curs'),
    InlineKeyboardButton('Расчитать по нынешнему курсу',callback_data='calculator'),
    InlineKeyboardButton('Главная',callback_data='menu')
]
inline1 = InlineKeyboardMarkup().add(*inline_buttons1)


inline_buttons2 = [
    InlineKeyboardButton('Курс доллара',callback_data='dollar'),
    InlineKeyboardButton('Курс евро',callback_data='euro'),
    InlineKeyboardButton('Курс рубля',callback_data='rub'),
    InlineKeyboardButton('Курс тенге',callback_data='kzt'),
    InlineKeyboardButton('Главная',callback_data='menu')
]
inline2 = InlineKeyboardMarkup().add(*inline_buttons2)



inline_buttons4 = [
    InlineKeyboardButton('Главная',callback_data='menu')
]
inline4 = InlineKeyboardMarkup().add(*inline_buttons4)

@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == 'dollar':
        await dollar (call.message)
    elif call.data == 'euro':
        await euro (call.message)
    elif call.data == "rub":
        await rub (call.message)
    elif call.data == "kzt":
        await kzt (call.message)
    elif call.data == "curs":
        await curs (call.message)
    elif call.data == "calculator":
        await calculator (call.message)
    elif call.data == "menu":
        await menu (call.message)




@dp.message_handler(commands="start")
async def start (message:types.Message):
    cursor=db.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO users VALUES (
            {message.from_user.id},
            '{message.from_user.username}',
            '{message.from_user.first_name}',
            '{message.from_user.last_name}',
            '{time.ctime()}'
        )""")
        cursor.connection.commit()
    await message.answer(f"""Привет{message.from_user.full_name}""",reply_markup=inline4)
@dp.message_handler(commands="/menu")
async def menu (message:types.Message):
    await message.answer(f"Удачного пользования!☺!☺!☺",reply_markup=inline1)

@dp.message_handler(commands=['curs'])
async def curs(message: types.Message):
    await message.answer(f'Курсы валют',reply_markup=inline2)
@dp.message_handler(commands=['dollar'])
async def dollar(message: types.Message):
    await message.answer(f'Курс доллара {usds}',reply_markup=inline2)
@dp.message_handler(commands=['euro'])
async def euro(message: types.Message):
    await message.answer(f'Курс евро {euros}',reply_markup=inline2)
@dp.message_handler(commands=['rub'])
async def rub(message: types.Message):
    await message.answer(f'Курс рубля {rubs}',reply_markup=inline2)
@dp.message_handler(commands=['kzt'])
async def kzt(message: types.Message):
    await message.answer(f'Курс тенге {kzts}',reply_markup=inline2)

@dp.message_handler(commands=['calculator'])
async def calculator(message: types.Message):
    await message.answer(f"""Выберите для расчета денег:
    Расчитать доллар в сом   /dollar_som
    Расчитать сом в доллар        /som_dollar
    Расчитать евро в сом     /euro_som
    Расчитать сом в евро          /som_euro
    Расчитать рубль в сом    /rub_som
    Расчитать сом в рубль         /som_rub
    Расчитать тенге в сом    /kzt_som
    Расчитать сом в тенге         /som_kzt
    """)


@dp.message_handler(commands=['dollar_som'],state=None)
async def dollar_som(message: types.Message):
    await message.answer(f'Введите количество долларов(USD):')
    await DollarSom.dollar.set()
@dp.message_handler(state=DollarSom)
async def dollar_som(message:types.Message,state:FSMContext):
    dollars=int(message.text)
    b=float(usds)
    c=dollars*b
    await message.answer(f"{c} сом(KGS)",reply_markup=inline1)


@dp.message_handler(commands=['som_dollar'],state=None)
async def som_dollar(message: types.Message):
    await message.answer(f'Введите количество сом(KGS):')
    await SomDollar.som.set()

@dp.message_handler(state=SomDollar)
async def som_dollar(message:types.Message,state:FSMContext):
    a=int(message.text)
    b=float(usds)
    c=a/b
    await message.answer(f"{c} долларов(USD)",reply_markup=inline1)


@dp.message_handler(commands=['euro_som'])
async def euro_som (message: types.Message):
    await message.answer(f'Введите количество евро(EURO):')
    await EuroSom.euro.set()

@dp.message_handler(state=EuroSom)
async def euro_som(message:types.Message,state:FSMContext):
    a=int(message.text)
    b=float(euros)
    c=a*b
    await message.answer(f"{c} сом (KGS)",reply_markup=inline1)


@dp.message_handler(commands=['som_euro'])
async def som_euro(message: types.Message):
    await message.answer(f'Введите количество сом(KGS):')
    await SomEuro.som.set()

@dp.message_handler(state=SomEuro)
async def som_euro(message:types.Message,state:FSMContext):
    a=int(message.text)
    b=float(euros)
    c=a/b
    await message.answer(f"{c} евро(EURO)",reply_markup=inline1)


@dp.message_handler(commands=['rub_som'])
async def rub_som (message: types.Message):
    await message.answer(f'Введите количество рублей(RUB):')
    await RubsSom.rub.set()

@dp.message_handler(state=RubsSom)
async def RubSom(message:types.Message,state:FSMContext):
    a=int(message.text)
    b=float(rubs)
    c=a*b
    await message.answer(f"{c} сом(KGS)",reply_markup=inline1)


@dp.message_handler(commands=['som_rub'])
async def som_rub(message: types.Message):
    await message.answer(f'Введите количество сом(KGS):')
    await SomsRub.som.set()

@dp.message_handler(state=SomsRub)
async def SomRub(message:types.Message,state:FSMContext):
    a=int(message.text)
    b=float(rubs)
    c=a/b
    await message.answer(f'{c} рублей(RUB)',reply_markup=inline1)



@dp.message_handler(commands=['kzt_som'])
async def kzt_som (message: types.Message):
    await message.answer(f'Введите количество рублей(KZT):')
    await KztsSom.kzt.set()
@dp.message_handler(state=KztsSom)
async def KztSom(message:types.Message,state:FSMContext):
    a=int(message.text)
    b=float(kzts)
    c=a*b
    await message.answer(f"{c} сом(KGS)",reply_markup=inline1)



@dp.message_handler(commands=['som_kzt'])
async def som_kzt(message: types.Message):
    await message.answer(f'Введите количество сом(KGS):')
    await SomsKzt.som.set()

@dp.message_handler(state=SomsKzt)
async def SomKzt(message:types.Message,state:FSMContext):
    a=int(message.text)
    b=float(kzts)
    c=a/b
    await message.answer(f"{c} сом(KGS)",reply_markup=inline1)

executor.start_polling(dp, skip_updates=True)

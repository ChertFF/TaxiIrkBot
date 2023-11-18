import os

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URL = f'postgresql://{PGUSER}:{PGPASSWORD}@{IP}/{DATABASE}'
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID'))

CITY_LIST = [
        [
           "г. Иркутск", "г. Шелехов"
        ],
        [
            "п. Дзержинск", "c. Пивовариха"
        ],
        [
            "п. Молодежный", "рабочий посёлок Маркова"
        ],
        [
            "c. Максимовщина", "с. Смоленщина"
        ],
        [
            "с. Баклаши", "с. Введенщина"
        ],
        [
            "д. Олха", "д. Новолисиха"
        ],
        [
            "п. Плишкино", "с. Мамоны"
        ],
        [
            "п. Мегет", "п. Грановщина"
        ],
        [
            "с. Хомутово", "д. Урик"
        ],
        [
            "п. Карлук", "д. Куда"
        ],
        [
           "д. Столбова", "д. Малая Еланка"
        ],
        [
            "п. Вересовка"
        ]]

TIME_LIST = [
        [
           "22:10"
        ],
        [
            "23:10"
        ],
        [
            "00:10"
        ],
        [
            "01:10"
        ],
        [
            "02:10"
        ]]

MORNING_TIME_LIST = [
        [
           "06:15"
        ]
        ]
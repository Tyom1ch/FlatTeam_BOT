import sqlite3
import datetime
import httpx
import random
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

token = "12120:3c7d7a8841024fa256cb18aa5bda1b4a"
user_pages = {}
user_pages_dom = {}
base_db = 'database.db'
stat_db = 'stats.db'

# Создание таблицы Users
def create_users_table():
    conn = sqlite3.connect(base_db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tg_id INTEGER UNIQUE,
                       join_date TIMESTAMP,
                       first_start INTEGER,
                       lolz_link TEXT,
                       worked_before INTEGER,
                       verified INTEGER
                       )''')
    conn.commit()
    conn.close()

def create_database():
    conn = sqlite3.connect(stat_db)  # Подключение к базе данных
    conn.close()

# Функция для создания таблицы statistics
def create_statistics_table():
    conn = sqlite3.connect(stat_db)  # Подключение к базе данных
    cursor = conn.cursor()

    # Создание таблицы statistics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            tg_id INTEGER PRIMARY KEY,
            balance REAL,
            all_time_logs TEXT,
            ma_files INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# Создание нового пользователя
async def create_user(tg_id, first_start, worked, lolz_link):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(base_db)
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO Users (tg_id, join_date, first_start, lolz_link, worked_before, verified)
                        VALUES (?, ?, ?, ?, ?, ?)''', (tg_id, timestamp, first_start, lolz_link, worked, 0))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as error:
        print("Произошла ошибка при выполнении операции:", error)
        return False
#
async def get_profile_data(tg_id):
    conn = sqlite3.connect(base_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE tg_id = ?", (tg_id,))
    result = cursor.fetchone()

    if result:
        (id, tg_id, join_date, first_start, url_lolz, worked_before, verified) = result
        conn.close()
        return (id, tg_id, join_date, first_start, url_lolz, worked_before, verified)
    else:
        conn.close()
        return True

async def get_statistics_by_tg_id(tg_id):
    conn = sqlite3.connect(stat_db)  # Подключение к базе данных
    cursor = conn.cursor()

    # Извлечение данных из таблицы statistics по tg_id
    cursor.execute('SELECT * FROM statistics WHERE tg_id = ?', (tg_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        # Распаковка данных из кортежа в переменные
        tg_id, balance, all_time_logs, ma_files = result

        # Возврат данных в виде кортежа или другой структуры данных по вашему выбору
        return tg_id, balance, all_time_logs, ma_files
    else:
        return None  # Если данные для заданного tg_id не найдены

#
async def get_profile_data_adm(tg_id):
    conn = sqlite3.connect(base_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE tg_id = ?", (tg_id,))
    result = cursor.fetchone()

    if result:
        (id, tg_id, join_date, first_start, url_lolz, worked_before, verified) = result
        conn.close()
        return (id, tg_id, join_date, first_start, url_lolz, worked_before, verified)
    else:
        conn.close()
        return True

#
async def check_first_start(tg_id):
    conn = sqlite3.connect(base_db)
    cursor = conn.cursor()
    cursor.execute("SELECT first_start FROM Users WHERE tg_id = ?", (tg_id,))
    result = cursor.fetchone()

    if result:
        first_start = result[0]
        if first_start:
            conn.close()
            return True
            #print(f"Пользователь с tg_id {tg_id} первый раз запускает бота")
        else:
            conn.close()
            return False
            #print(f"Пользователь с tg_id {tg_id} уже запускал бота ранее")
    else:
        conn.close()
        return True

# Удаление пользователя по ID
async def delete_user(user_id):
    conn = sqlite3.connect(base_db)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM Users WHERE id = ?''', (user_id,))
    conn.commit()
    conn.close()
# Проверка ссылки на подлинность
async def checklink(url):
    headers = {'User-Agent': 'My User Agent'}
    cookies = {'session_id': '1234567890'}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, cookies=cookies)
            return response.status_code
    except Exception as e:
        print(e)
        return False

async def get_page_number(telegram_id):
    if telegram_id in user_pages:
        return user_pages[telegram_id]
    else:
        return None

async def get_page_number_dom(telegram_id):
    if telegram_id in user_pages_dom:
        return user_pages_dom[telegram_id]
    else:
        return None

async def set_page(telegram_id, page_number):
    user_pages[telegram_id] = page_number

async def set_page_dom(telegram_id, page_number):
    user_pages_dom[telegram_id] = page_number

async def increase_page(telegram_id, MAX_PAGE_NUMBER):
    if telegram_id in user_pages:
        user_pages[telegram_id] += 1
        # ограничение до указанного номера
        # можно добавить проверку здесь, чтобы удостовериться, что номер не превышает заданное значение
        if user_pages[telegram_id] > MAX_PAGE_NUMBER: user_pages[telegram_id] = MAX_PAGE_NUMBER
    else:
        user_pages[telegram_id] = 0

async def decrease_page(telegram_id):
    if telegram_id in user_pages:
        user_pages[telegram_id] -= 1
        # ограничение до указанного номера
        # можно добавить проверку здесь, чтобы удостовериться, что номер не меньше 0
        if user_pages[telegram_id] < 0: user_pages[telegram_id] = 0
    else:
        user_pages[telegram_id] = 0

# Получить ID доменов
async def get_domains_list_id():
    headers = {"Authorization": f"Basic {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.uproject.cc/links/list", headers=headers)
        if response.status_code == 200:
            data = response.json()
            domid = []
            for doms in data["domains"]:
                domid.append(doms["id"])
            return (domid)
        else:
            return False
            print(f"Ошибка при выполнении запроса: {response.status_code}")
# Получсить список ID дизайнов
async def get_design_list_id():
    headers = {"Authorization": f"Basic {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.uproject.cc/designs/list", headers=headers)
        if response.status_code == 200:
            data = response.json()
            ids = []
            for item in data:
                ids.append(item["id"])
                #print(item["name"])
            return(ids)
        else:
            return False
            print(f"Ошибка при выполнении запроса: {response.status_code}")
# Получить названия доменов
async def get_domains_list_names():
    headers = {"Authorization": f"Basic {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.uproject.cc/links/list", headers=headers)
        if response.status_code == 200:
            data = response.json()
            domains = []
            for doms in data["domains"]:
                domains.append(doms["domain"])
            return(domains)
        else:
            return False

def generate_17_digit_number():
    min_value = 10 ** 16  # Минимальное 17-значное число
    max_value = (10 ** 17) - 1  # Максимальное 17-значное число
    
    random_number = random.randint(min_value, max_value)
    random_number_str = str(random_number).zfill(17)
    
    return (f"profiles/{str(random_number_str)}")

# Получить названия дизайнов
async def get_design_list_names():
    headers = {"Authorization": f"Basic {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.uproject.cc/designs/list", headers=headers)
        if response.status_code == 200:
            data = response.json()
            desingns = []
            for item in data:
                desingns.append(item["name"])
                #print(item["name"])
            return(desingns)
        else:
            return False

# Получить активные ссылки
async def get_actual_links():
    headers = {"Authorization": f"Basic {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.uproject.cc/links/list", headers=headers)
        if response.status_code == 200:
            data = response.json()
            links = []
            for item in data["list"]:
                domain_name = item["domain_name"]
                path_name = item["path"]
                link_create_time = datetime.datetime.fromtimestamp(item["date"])
                links.append((domain_name, path_name, link_create_time))
            return links
        else:
            return False

#
async def create_link(design_id, domain_id, profile_adress=generate_17_digit_number()):
    headers = {"Authorization": f"Basic {token}"}
    post_data = {"domain": domain_id, "design": design_id, "path": profile_adress}
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.uproject.cc/links/new", headers=headers, json=post_data)
        if response.status_code == 200:
            data = response.json()
            return True
        else:
            return False
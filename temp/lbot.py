import sqlite3
from datetime import datetime
import httpx

token = "12120:3c7d7a8841024fa256cb18aa5bda1b4a"

base_db = 'database.db'

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
    conn = sqlite3.connect('stats.db')  # Подключение к базе данных
    conn.close()

# Функция для создания таблицы statistics
def create_statistics_table():
    conn = sqlite3.connect('stats.db')  # Подключение к базе данных
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
    conn = sqlite3.connect('stats.db')  # Подключение к базе данных
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
# Получить ID доменов
async def get_domains_list_id():
    headers = {"Authorization": f"Basic {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.uproject.cc/links/list", headers=headers)
        if response.status_code == 200:
            data = response.json()
            for doms in data["domains"]:
                print(doms["id"])
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")
# Получсить список ID дизайнов
async def get_design_list_id():
    headers = {"Authorization": f"Basic {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.uproject.cc/designs/list", headers=headers)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                return item["id"]
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")
# Получить названия доменов
async def get_domains_list_names():
    headers = {"Authorization": f"Basic {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.uproject.cc/links/list", headers=headers)
        if response.status_code == 200:
            data = response.json()
            for doms in data["domains"]:
                return(doms["domain"])
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")
# Получить названия дизайнов
async def get_design_list_names():
    headers = {"Authorization": f"Basic {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.uproject.cc/designs/list", headers=headers)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                return item["name"]
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")
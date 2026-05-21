import logging
import os
import sqlite3

from aiogram import Bot
from aiogram.types import Message, FSInputFile
import requests

from core.keyboards.reply import get_reply_keyboard
from core.keyboards.inline import get_inline_keyboard
from core.settings import settings

logger = logging.getLogger(__name__)

API_URL = os.getenv('API_URL', '')
API_TOKEN = os.getenv('API_TOKEN', '')

tg_token = os.getenv('tg_token')
tg_chat_id = os.getenv('tg_chat_id')


def send2tg(message):
    url = f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_chat_id}&text={message}"
    return requests.get(url).json()


db_path = '/data/skin_d.db' if os.path.exists('/data/skin_d.db') else 'skin_d.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()


def table_exists(table_name):
    c.execute(
        'SELECT count(name) FROM sqlite_master WHERE type = ? AND name = ?',
        ('table', table_name)
    )
    return c.fetchone()[0] == 1


if not table_exists('skin_d'):
    c.execute('''
        CREATE TABLE skin_d(
            chat_num TEXT,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            date TEXT,
            diagnosis TEXT
        )
    ''')


def insert_p(chat_num, first_name, last_name, username, date, diagnosis):
    c.execute(
        'INSERT INTO skin_d (chat_num, first_name, last_name, username, date, diagnosis) VALUES(?, ?, ?, ?, ?, ?)',
        (chat_num, first_name, last_name, username, date, diagnosis)
    )
    conn.commit()


async def get_photo(message: Message, bot: Bot):
    await message.reply('Отлично. Ты отправил изображение, я загружу его в модель ИИ.')

    file = await bot.get_file(message.photo[-1].file_id)
    file_path = f'photos/{message.photo[-1].file_id}.jpg'
    await bot.download_file(file.file_path, file_path)
    logger.info(f'Downloaded photo to {file_path}, size={os.path.getsize(file_path)} bytes')

    try:
        with open(file_path, 'rb') as f:
            logger.info(f'POST {API_URL}')
            response = requests.post(
                API_URL,
                headers={
                    'Authorization': f'Bearer {API_TOKEN}',
                    'accept': 'application/json',
                },
                files={'file': (file_path, f, 'image/jpeg')},
                timeout=300,
            )
        response.raise_for_status()
        result = response.json()
        logger.info(f'API response: {result}')

        prediction = result.get('prediction', 'Неизвестно')
        recommendations = result.get('recommendations', '')
        is_skin = result.get('is_skin', False)
        is_pathology = result.get('is_pathology', False)

    except Exception as e:
        logger.error(f'API request failed: {type(e).__name__}: {e}')
        prediction = 'Ошибка анализа'
        recommendations = 'Не удалось связаться с сервером диагностики. Попробуйте позже.'
        is_skin = False
        is_pathology = False

    os.remove(file_path)

    if not is_skin:
        await message.answer(
            f'{message.from_user.first_name}, на изображении не обнаружена кожа. '
            f'Пожалуйста, отправьте фотографию кожи крупным планом.'
        )
        return

    pathology_note = '\n⚠️ Обнаружена патология. Рекомендуется консультация врача.' if is_pathology else ''

    await message.answer(
        f'{message.from_user.first_name}, результаты следующие:\n\n'
        f'📍 Диагноз: {prediction}\n📍 Рекомендации: {recommendations}'
        + pathology_note
    )
    insert_p(
        message.chat.id, message.from_user.first_name, message.from_user.last_name,
        message.from_user.username, message.date, prediction
    )


async def get_inline(message: Message, bot: Bot):
    await message.answer(f'{message.from_user.first_name}, выбери то, что тебе нужно:',
                         reply_markup=get_inline_keyboard())


async def get_start(message: Message, bot: Bot):
    send2tg(f'New user in SkinAI: {message.from_user.first_name}')
    await message.answer(
        f'<b>Привет, {message.from_user.first_name}. Рад тебя видеть.</b>\n'
        f'Данный бот представляет собой демо-версию модели ИИ для диагностики кожных заболеваний. '
        f'В данной версии анализируются только опухолевые заболевания.\n'
        f'Пришли мне фото кожи 🔬\n\n'
        f'🚩 <b>Необходимо отправить фотографию без посторонних предметов. '
        f'На изображении должна быть только исследуемая область кожи. При необходимости обрежь фотографию.</b>\n\n'
        f'🚩 Данный диагноз не является окончательным и не заменяет посещение врача.\n\n'
        f'🚩 Не является оказанием медицинской услуги.',
        reply_markup=get_reply_keyboard())
    insert_p(message.chat.id, message.from_user.first_name, message.from_user.last_name,
             message.from_user.username, message.date, None)
    photo = FSInputFile('assets/photo_choice.jpg')
    await bot.send_photo(message.chat.id, photo, caption='Какое фото лучше отправить?')


async def get_hello(message: Message, bot: Bot):
    await message.reply('И тебе привет!')


async def get_help(message: Message, bot: Bot):
    await message.reply('Отправь мне фото и я по нему поставлю диагноз.\n\n🚩Постарайся чтобы на фотографии была только кожа и не было посторонних предметов, так как от этого будет зависеть точность диагноза.')


async def get_cancel(message: Message, bot: Bot):
    await message.reply('Мы не храним ваши фотографии, поэтому можете не беспокоиться о них.')


async def get_support(message: Message, bot: Bot):
    await message.reply('Можете поддержать развитие данного проекта: https://yoomoney.ru/fundraise/1HGP6FN1PVQ.260502')


async def get_order(message: Message, bot: Bot):
    await message.reply('Если хотите заказать у нас бот любой сложности, то можете обратиться к нам через телеграмм: https://t.me/dinis_n')


async def get_faq(message: Message, bot: Bot):
    await message.reply('📌 Что такое Skin AI?\nSkin AI – это возможность распознавания заболеваний кожи по фотографии со смартфонов, основанная на медицинском опыте, технологиях искусственного интеллекта и компьютерного зрения.\n\n📌 Для кого предназначен Skin AI?\nОсновные группы пользователей Skin AI:\n1️⃣ Рядовые пользователи – для самостоятельной проверки здоровья кожи.\n2️⃣ Дерматологи, терапевты, врачи общей практики, косметологи могут использовать Skin AI как вспомогательный инструмент для принятия решений.\n\n📌 Заменяет ли Skin AI врачей?\n1️⃣ Skin AI не заменяет визит к врачу.\n2️⃣ Skin AI не ставит диагнозы, не выписывает лекарственные средства.\n\n📌 Как часто стоит проводить скрининг кожных заболеваний?\nСтрогих цифр нет, но рекомендуем повторно загружать фотографию даже при небольших визуальных изменениях.')


async def get_better(message: Message, bot: Bot):
    await message.reply('Ответьте, пожалуйста, на несколько вопросов. Это займет пару минут: https://forms.gle/WXttCBGeQzuZCkPDA')


async def get_newsletter(message: Message, bot: Bot):
    if message.from_user.id == int(settings.bots.admin_id):

        chat_ids_list = []
        c.execute('''SELECT chat_num FROM skin_d''')
        for row in c.fetchall():
            chat_ids_list.append(int(row[0]))

        for i in list(set(chat_ids_list)):
            try:
                await bot.send_message(chat_id=i, text=message.text.replace('#рассылка ', ''),
                                       disable_notification=True
                                      )
            except Exception:
                continue


async def get_smile(message: Message, bot: Bot):
    await message.reply('Спасибо за поддержку!')
    await bot.send_message(chat_id=int(settings.bots.admin_id), text=f'{message.from_user.first_name} 👍',
                                       disable_notification=True
                                      )

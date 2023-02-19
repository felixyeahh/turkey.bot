#    turkey-bot - telegran bot that does not like "bad" words
#    Copyright (C) 2023  Baffu, Inc. <https://baffu.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from loguru import logger

import sys
import json
import string

from aiogram.utils import executor, deep_linking
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from .bot import dp, bot, Bot, Dispatcher
from .database.database import get_engine, connect_database, check_turkey, new_turkey

if sys.version_info < (3, 8, 0):
    logger.critical('your python version is too low')
    sys.exit(1)

async def create_db(bot: Bot):
    sqlite_file_name = 'database.db'
    sqlite_url = f'sqlite:///{sqlite_file_name}'
    engine = get_engine(sqlite_url)
    await connect_database(engine)
    bot['engine'] = engine
async def on_startup(dp: Dispatcher):
    try:
        await create_db(dp.bot)
        logger.info('bot connected')
    except Exception as e:
        return logger.exception(e)

@dp.message_handler(commands=['start'], commands_prefix='/')
async def startcmd(message: Message):
    if message.chat.type == 'private':
        return await message.reply('''👾 <b>TurkeyBot</b> - <i>бот, который не любит нецензурную лексику!</i>

• я отправляю каждому человеку, который написал в своём сообщении мат, свой любимый хэштег - #ктоМатеритсяТотИндюк 
• я считаю индюков пользователя и чата
• можно посмотреть сколько индюков у пользователя/чата с помощью <code>сколько индюков?</code>''', parse_mode='html', reply_markup=InlineKeyboardMarkup()\
    .add(InlineKeyboardButton('🐸 Добавить в свой чат', 't.me/baffuturkeybot?startgroup=hi')))

    return bot.send_message(message.chat.id, '👾 Добрый день, чат! Спасибо за добавление бота :3')
    
@dp.message_handler(Text(startswith='сколько индюков', ignore_case=True))
async def check_turkey_cmd(message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        text = '🐸 У пользователя'
    else:
        user_id = message.from_user.id
        text = '🐸 У вас'
    turkey = check_turkey(message.bot.get('engine'), user_id, message.chat.id)

    await message.reply(f'{text} {turkey[0]} индюков.\n\n🛸 Всего индюков в чате: {turkey[1]}')
    return turkey_handler(message)

@dp.message_handler()
async def turkey_handler(message: Message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id

        text = message.text.lower()
        engine = message.bot.get('engine')

        if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in text.split(" ")}.intersection(set(json.load(open('cenz.json')))) != set():
            new_turkey(engine, user_id, chat_id)
            turkey = check_turkey(engine, user_id, chat_id)
            return await message.reply(f'🦃 #ктоМатеритсяТотИндюк (это ваш {turkey[0]} индюк!)\n\n🛸 Всего индюков в чате: {turkey[1]}')
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True)
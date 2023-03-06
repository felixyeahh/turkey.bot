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

import configparser
import sys
import getpass

from datetime import datetime

from loguru import logger
from aiogram import Bot, Dispatcher

config = configparser.ConfigParser()

def colored_input(prompt: str = "", hide: bool = False) -> str:
    """beatiful colored user input"""
    frame = sys._getframe(1)
    return (input if not hide else getpass)(
        "\x1b[32m{time:%Y-%m-%d %H:%M:%S}\x1b[0m | "
        "\x1b[1m{level: <8}\x1b[0m | "
        "\x1b[36m{name}\x1b[0m:\x1b[36m{function}\x1b[0m:\x1b[36m{line}\x1b[0m - \x1b[1m{prompt}\x1b[0m".format(
            time=datetime.now(), level="INPUT", name=frame.f_globals["__name__"],
            function=frame.f_code.co_name, line=frame.f_lineno, prompt=prompt
        )
    )

if not config.read("./config.ini"):
    config['bot'] = {
        "token": colored_input("Enter your bot token: ")
    }
    with open('./config.ini', 'w') as file:
        config.write(file)
        logger.success('config is succesfully setted up. Now, restart the bot.')
        sys.exit(1)
        
config.read('./config.ini')
TOKEN = config.get('bot', 'token')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
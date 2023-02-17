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

from sqlmodel import SQLModel, Field
from typing import Optional

class userdata(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, description='Telegram User ID')
    turkey: Optional[int] = Field(default=0, description='User Turkey Count')

class chatdata(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: Optional[int] = Field(default=None, description='Telegram Chat ID')
    chat_turkey: Optional[int] = Field(default=None, description='Chat Turkey Count')
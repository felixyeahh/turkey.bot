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

from sqlmodel import create_engine, select, Session, SQLModel
from sqlalchemy import exc
from .SQLModels import userdata, chatdata

from typing import Union, Tuple

async def connect_database(engine: create_engine) -> None:
    SQLModel.metadata.create_all(engine)

def get_engine(path: str) -> create_engine:
    return create_engine(path, echo=False)

def get_user(engine: create_engine, user_id: str) -> Union[userdata, None]:
    with Session(engine) as session:
        try:
            user = session.exec(select(userdata).where(userdata.user_id == user_id)).one()
        except exc.NoResultFound:
            logger.warning(f"user {user_id} was not founded")
            return None
    logger.info(f'user {user_id} was founded')
    return user
def create_user(engine: create_engine, data: dict) -> Union[userdata, None]:
    user = userdata(**data)
    with Session(engine) as session:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            logger.info(f'user {data["user_id"]} was created')
        except exc.CompileError:
            logger.warning(f'user {data["user_id"]} was not created')
            return None
    return user
def update_user(engine: create_engine, user_id: str, field_name: str, value: int) -> bool:
    user = get_user(engine, user_id)
    with Session(engine) as session:
        try:
            setattr(user, field_name, value)
            session.add(user)
            session.commit()
            logger.info(f'user {user_id} updated')
        except exc.CompileError:
            logger.warning(f'user {user_id} was not updated')
            return False
    return True

def get_chat(engine: create_engine, chat_id: str) -> Union[chatdata, None]:
    with Session(engine) as session:
        try:
            chat = session.exec(select(chatdata).where(chatdata.chat_id == chat_id)).one()
        except exc.NoResultFound:
            logger.warning(f"chat {chat_id} was not founded")
            return None
    logger.info(f'chat {chat_id} was founded')
    return chat
def create_chat(engine: create_engine, data: dict) -> Union[chatdata, None]:
    chat = chatdata(**data)
    with Session(engine) as session:
        try:
            session.add(chat)
            session.commit()
            session.refresh(chat)
            logger.info(f'chat {data["chat_id"]} was created')
        except exc.CompileError:
            logger.warning(f'chat {data["chat_id"]} was not created')
            return None
    return chat
def update_chat(engine: create_engine, chat_id: str, field_name: str, value: int) -> bool:
    chat = get_chat(engine, chat_id)
    with Session(engine) as session:
        try:
            setattr(chat, field_name, value)
            session.add(chat)
            session.commit()
            logger.info(f'user {chat_id} updated')
        except exc.CompileError:
            logger.warning(f'user {chat_id} was not updated')
            return False
    return True 

def new_turkey(engine: object, user_id: str, chat_id: str) -> None:
    user = get_user(engine, user_id)
    chat = get_chat(engine, chat_id)

    if not user:
        user = create_user(engine, {'user_id': user_id, 'turkey': 1})
    else:
        update_user(engine, user_id, 'turkey', getattr(user, 'turkey') + 1)
    if not chat:
        chat = create_chat(engine, {'chat_id': chat_id, 'chat_turkey': 1})
    else:
        update_chat(engine, chat_id, 'chat_turkey', getattr(chat, 'chat_turkey'))
    return

def check_turkey(engine: object, user_id: str, chat_id: str) -> Tuple[int, int]:
    user = get_user(engine, user_id)
    chat = get_chat(engine, chat_id)

    return (user.turkey, chat.chat_turkey)
from aiogram.types import InputMediaPhoto, InputMediaDocument, InputMediaVideo
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from asyncio import sleep as asleep
from typing import List

from settings import bot


def _chunk_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


async def send_media(attachments: List, chat_id: int):
    photos = []
    documents = []
    video = []
    for attachment in attachments:
        if attachment['type'] == 'photo':
            photos.append(InputMediaPhoto(media=attachment['context'][0]))
        elif attachment['type'] == 'document':
            documents.append(InputMediaDocument(media=attachment['context'][0]))
        elif attachment['type'] == 'video':
            video.append(InputMediaVideo(media=attachment['context'][0]))
    for chunk in _chunk_list(photos, chunk_size=10):
        await bot.send_media_group(chat_id=chat_id, media=chunk)
    for chunk in _chunk_list(documents, chunk_size=10):
        await bot.send_media_group(chat_id=chat_id, media=chunk)
    for chunk in _chunk_list(video, chunk_size=10):
        await bot.send_media_group(chat_id=chat_id, media=chunk)


async def send_message(text: str, chat_id: int):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except TelegramRetryAfter as FloodControlException:
        await asleep(FloodControlException.retry_after)
        await bot.send_message(chat_id=chat_id, text=text)
    except TelegramBadRequest:
        return False
    return True

import uuid
import os
from typing import Dict
import ftransc.core as ft
import speech_recognition as sr
from aiogram import Bot, Router, F
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from chat_gpt.config import Settings
from chat_gpt.presentation.di import IoC
from chat_gpt.presentation.bot.filters import ChatTypeFilter, UserAccess
from chat_gpt.core.dto import SendQuery
from chat_gpt.core.use_cases import SendQueryUseCase


router = Router()


@router.message(
    ChatTypeFilter(["private"]),
    UserAccess(),
    F.content_type.in_([ContentType.VOICE]),
)
async def voice_query(
    message: Message,
    useful_data: Dict,
    state: FSMContext,
    bot: Bot,
    settings: Settings,
    ioc: IoC,
):
    send_query_use_case: SendQueryUseCase = await ioc.provider(
        SendQueryUseCase
    )
    user = useful_data["user"]
    filename = str(uuid.uuid4())
    file_name_full = filename + ".ogg"
    file_name_full_converted = filename + ".wav"
    file_info = await bot.get_file(message.voice.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    with open(file_name_full, "wb") as new_file:
        new_file.write(downloaded_file.getvalue())
    text = await transcribe_voice(filename)
    if text == "Sorry.. run again...":
        answer = "Извините, мы не смогли перевести текст"
    else:
        if user.number_requests + 1 > settings.request_limit:
            await message.answer("Лимит запросов исчерпан")
            return
        answer = await send_query_use_case.execute(
            SendQuery(
                user_id=user.id,
                query_text=text,  # type: ignore
            )
        )
    os.remove(file_name_full)
    os.remove(file_name_full_converted)
    await message.answer(answer)


async def transcribe_voice(file_info):
    ft.transcode(file_info + ".ogg", "wav")
    recognizer = sr.Recognizer()
    with sr.WavFile(file_info + ".wav") as source:
        audio = recognizer.record(source)

    try:
        txt = recognizer.recognize_google(audio, language="ru_RU")
        return txt
    except sr.UnknownValueError:
        return "Sorry.. run again..."
    except sr.RequestError:
        return "Sorry.. run again..."

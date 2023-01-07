import dataclasses

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.types import InputFile
from pytube import YouTube
from data.config import ADMINS
from handlers.users.youtube import Download,Download_audio
from random import choice
from string import ascii_lowercase

from keyboards.inline.menu import kb
from loader import dp, bot
import os

@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    print(message.from_user.id)
    await message.answer(f"Salom, {message.from_user.full_name}!")

def rand():
    result_str = ''.join(choice(ascii_lowercase) for i in range(5))
    return result_str

@dp.message_handler(text_contains="https://youtube.com/watch?v=")
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    url = message.text
    yt = YouTube(url)
    thumb = YouTube(url).thumbnail_url
    data = message.text.replace("https://youtube.com/watch?v=","https://youtube.com/")
    await bot.send_photo(chat_id=user_id, photo=thumb, caption=f"*📹 {yt.title}* [→]({yt.channel_url})\n"
                                                               f"👤 [#{yt.author} →]({yt.channel_url})\n\n"
                                                               f"*Yuklab olish turini tanlang ↓*",
                         reply_markup=kb.main(video_url=data, audio_url=data), parse_mode="Markdown")

@dp.message_handler()
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    url = message.text
    yt = YouTube(url)
    thumb = YouTube(url).thumbnail_url
    if message.text.startswith == "https://youtu.be/" or "https://youtube.com/" or "https://www.youtube.com/" or "https://youtube.com/shorts/" or "http://youtu.be/" or "http://youtube.com/" or "http://www.youtube.com/":
        await bot.send_photo(chat_id=user_id,photo=thumb,caption=f"*📹 {yt.title}* [→]({yt.channel_url})\n"
                                                    f"👤 [#{yt.author} →]({yt.channel_url})\n\n"
                                                    f"*Yuklab olish turini tanlang ↓*",
                             reply_markup=kb.main(video_url=url, audio_url=url), parse_mode="Markdown")
    else:
        await message.answer("😕 Men Faqat YouTubedan yuklayman...", parse_mode="Markdown")

@dp.callback_query_handler(text_contains="video;")
async def select(call:types.CallbackQuery):
    message_id = (await call.message.answer("Yuklanmoqda...🚀")).message_id
    await call.message.delete()
    data = call.data
    print(data)
    video_url = data.rsplit(";")
    print(video_url[1])
    user_bot =await bot.get_me()
    x = rand()
    print(x)
    data = await Download(video_url[1],"media/",x)
    if data is not None:
        await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
        await bot.send_video(chat_id=call.from_user.id,video=f"{data}",caption=f"Yuklab olish muvaffaqiyatli yakunlandi 🥳\n\n@{user_bot.username}")
        if os.path.exists(f"media/{x}"):
            os.remove(f"media/{x}")
        else:
            await bot.send_message(chat_id=ADMINS,text="XATOLIK YUZAGA KELDI...\n\nADMIN MENI SOZLAMASANGIZ BOTINGIZ SIZDAN XAFA BO'LADI...")
    else:
        await call.message.answer("Yuklab Bo'lmadi qayta Yuborin...")


@dp.callback_query_handler(text_contains="audio:")
async def select(call:types.CallbackQuery):
    message_id = (await call.message.answer("Yuklanmoqda...🚀")).message_id
    await call.message.delete()

    data = call.data
    audio_url = data.replace("audio:","")
    print(audio_url)
    user_bot =await bot.get_me()
    f = rand()
    data = await Download_audio(audio_url,f"audio/",f + ".mp3")
    audio_url = InputFile(path_or_bytesio=f"audio/{f}.mp3")
    if data is not None:
        await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
        await bot.send_audio(chat_id=call.from_user.id,audio=audio_url,title="Audio",performer=f"@{user_bot.username}",caption=f"Yuklab olish muvaffaqiyatli yakunlandi 🥳\n\n@{user_bot.username}")
        if os.path.exists(f"audio/{f}.mp3"):
            os.remove(f"audio/{f}.mp3")
        else:
            await bot.send_message(chat_id=ADMINS,text="XATOLIK YUZAGA KELDI...\n\nADMIN MENI SOZLAMASANGIZ BOTINGIZ SIZDAN XAFA BO'LADI...")
    else:
        await call.message.answer("Yuklab Bo'lmadi qayta Yuborin...")

@dp.callback_query_handler(text_contains="off")
async def select(call:types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Yuklash uchun Havola yuboring")
from pytube import YouTube
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

TOKEN = "5603383887:AAFCJijKuThcsOJKxAQVpxMkwDxdUWCLrHg"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Link(StatesGroup):
  link_user = State()
  


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
  await message.reply("Hello!\nSend link on youtube video")
  await Link.link_user.set()

@dp.message_handler(state=Link.link_user)
async def link_finded(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data["link_user"] = message.text
    dload = YouTube(message.text)
    if os.path.exists(f"{os.getcwd()}/{dload.title}.mp4"):
      os.remove(f"{dload.title}.mp4")
      video = dload.streams.first()
      video = dload.streams.get_highest_resolution()
      video.download()
      await bot.send_video(message.chat.id, open(f'{dload.title}.mp4', 'rb'))
      print(dload.title)
    else:
      video = dload.streams.first()
      video = dload.streams.get_highest_resolution()
      video.download()
      await bot.send_video(message.chat.id, open(f'{dload.title}.mp4', 'rb'))
      print(dload.title)

  await state.finish()
  


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)

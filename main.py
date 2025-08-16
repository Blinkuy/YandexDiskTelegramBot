import os
import yadisk
import datetime
from time import time_ns
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database import *

load_dotenv()
os.makedirs("photos", exist_ok=True)

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
YANDEX_DISK_TOKEN = os.getenv("YANDEX_DISK_TOKEN")

yan_disk = yadisk.YaDisk(token=YANDEX_DISK_TOKEN)
bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()


def get_path_by_date_and_cafe(cafe_title):
    date = datetime.date.today()

    year = date.year
    month = date.month
    day = date.day

    path = f"{cafe_title}/{year}/{month}/{day}"
    return path


async def create_dir_date(path):
    yan_disk.makedirs(path)
    return path


@dp.message(Command(commands="start"))
async def on_start(message: Message):
    
    arg = message.text.split()[1] if len(message.text.split()) > 1 else None
    user_id = message.from_user.id
    
    if arg is None:
        await message.answer("В стратовую команду не был передан ключ. Пример: /start <ключ>")
    else:
        if is_user_in_table(user_id):
            await message.answer(f"Вы уже входили в систему. Предприятие: {get_cafe_by_user_id(user_id)}")
        else:   
            insert_user(user_id, arg)
            await message.answer(f"Вы были записаны в предприятие: {get_cafe_by_user_id(user_id)}")
        

@dp.message(F.content_type == "photo")
async def handle_photo(message: Message):

    user_id = message.from_user.id
    try:
        cafe_title = get_cafe_by_user_id(user_id)
    except TypeError:
        message.answer("Вы не были зарегестрированы в предприятии!")
        return
    
    ph = message.photo[-1]

    file_id = ph.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await bot.download_file(file_path, f"photos/{file_id}.jpg")

    path = get_path_by_date_and_cafe(cafe_title)
    
    if not yan_disk.is_dir(path):
        await create_dir_date(path)

    path += f"/{time_ns()}.jpg"
    try:
        yan_disk.upload(f"photos/{file_id}.jpg", path)
        os.remove(f"photos/{file_id}.jpg")
    except Exception:
        await message.answer("Произошла ошибка. Фото не загружено!")
    else:
        await message.answer(f"Фото успешно загружено в предприятие: \"{cafe_title}\"!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход из бота")


import os
import yadisk
import datetime
from time import time_ns
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

load_dotenv()
os.makedirs("photos", exist_ok=True)

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
YANDEX_DISK_TOKEN = os.getenv("YANDEX_DISK_TOKEN")

yan_disk = yadisk.YaDisk(token=YANDEX_DISK_TOKEN)
bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()


def get_path_by_date():
    date = datetime.date.today()

    year = date.year
    month = date.month
    day = date.day

    path = f"{year}/{month}/{day}"
    return path


async def create_dir_date(path):
    yan_disk.makedirs(path)
    return path


@dp.message(Command("start"))
async def on_start(message: Message):
    await message.answer("Привет, отправь фото накладной и я загружу ее на диск!")


@dp.message(F.content_type == "photo")
async def handle_photo(message: Message):

    ph = message.photo[-1]

    file_id = ph.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await bot.download_file(file_path, f"photos/{file_id}.jpg")

    path = get_path_by_date()
    if not yan_disk.is_dir(path):
        await create_dir_date(path)

    path += f"/{time_ns()}.jpg"
    yan_disk.upload(f"photos/{file_id}.jpg", path)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
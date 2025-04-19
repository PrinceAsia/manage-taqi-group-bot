import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
import asyncio
import re
from datetime import timedelta
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Tokenni shu yerga yozing
BOT_TOKEN = getenv("BOT_TOKEN")

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher obyektlari
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Bloklashga sabab bo‘ladigan so‘zlar
BLOCK_KEYWORDS = ['стабил', 'ищу', 'напиши', 'подходит', 'кандидат', 'доллар', 'доход', 'капитал',
                  'средств', 'источ', 'отправ', 'для', 'доступно', 'возможност', 'недел', 'получа',
                  'лич']

# Guruhdagi xabarlarni tekshirish
@dp.message(F.chat.type == ChatType.SUPERGROUP)
async def check_message(message: types.Message):
    txt = message.text or message.caption or ""
    text = txt.lower()
    s = 0
    for keyword in BLOCK_KEYWORDS:
        if keyword in text:
            s += 1
            if s > 2:
                break
    if s > 2:
        try:
            until_date = message.date + timedelta(days=7)
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until_date
            )

            # Javob yuborish
            await message.reply(f"⚠️ @{message.from_user.username} 7 sutkaga bloklandi, sabab: taqiqlangan so‘zlar qatnashgan xabar.")
            # Xabarni o‘chirish
            await message.delete()

        except Exception as e:
            logging.error(f"Bloklashda xatolik: {e}")
            await message.reply("❌ Foydalanuvchini bloklashda xatolik yuz berdi.")

# Botni ishga tushurish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

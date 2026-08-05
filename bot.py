import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Твой токен от @BotFather
TOKEN = "8896652212:AAE5hg7ODgmoTkhL7KbxdizWYg--PcT0jjU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище последних данных об авариях и ремонтах (в реальном проекте здесь будет парсер или API)
current_incidents = {
    "accidents": [
        "⚠️ **М-3 «Украина», 35-й км (возле Внуково):** Оформление ДТП в среднем ряду, занята полоса.",
    ],
    "works": [
        "🚧 **М-3 «Украина», 65-й км:** Дорожные работы, сужение дороги до двух полос."
    ]
}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "🚗 **Бот-транслятор Киевского шоссе активен!**\n\n"
        "Я слежу за пробками, авариями и ремонтом дорог.\n\n"
        "📌 **Доступные команды:**\n"
        "/status — Общая дорожная ситуация\n"
        "/accidents — Актуальные аварии и дорожные работы\n"
        "/cameras — Ссылки на камеры"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    status_text = (
        "📊 **Оперативная ситуация на М-3:**\n\n"
        "• МКАД — Апрелевка: движение плотное, скорость 40-60 км/ч.\n"
        "• Апрелевка — Наро-Фоминск: свободнее, до 90 км/ч.\n"
        "• Погода: сухо, видимость хорошая."
    )
    await message.answer(status_text, parse_mode="Markdown")

@dp.message(Command("accidents"))
async def cmd_accidents(message: Message):
    accidents_list = "\n".join(current_incidents["accidents"]) if current_incidents["accidents"] else "Аварий не зафиксировано."
    works_list = "\n".join(current_incidents["works"]) if current_incidents["works"] else "Дорожных работ нет."

    response_text = (
        f"🚨 **Оперативная информация об инцидентах:**\n\n"
        f"**Аварии и ДТП:**\n{accidents_list}\n\n"
        f"**Дорожные работы:**\n{works_list}"
    )
    await message.answer(response_text, parse_mode="Markdown")

@dp.message(Command("cameras"))
async def cmd_cameras(message: Message):
    cameras_text = (
        "📷 **Полезные ресурсы:**\n\n"
        "• [Яндекс.Карты (Киевское шоссе)](https://yandex.ru/maps)\n"
        "• [Сервис ЦОДД / Автодор](https://russianhighways.ru)"
    )
    await message.answer(cameras_text, parse_mode="Markdown", disable_web_page_preview=True)

# Функция для фоновой проверки (сюда можно добавить реальный парсинг сайтов или API)
async def check_road_updates():
    while True:
        await asyncio.sleep(300)  н# Проверка каждые 5 минут
        # Здесь в будущем будет логика запроса к API карт. 
        # Если появляется новое ЧП, его можно автоматически отправлять в админ-чат или канал.
        logging.info("Фоновая проверка дорожной обстановки...")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот успешно запущен и готов ловить аварии!")
    
    # Запускаем фоновую задачу параллельно с ботом
    asyncio.create_task(check_road_updates())
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from duckduckgo_search import DDGS  # Библиотека для поиска свежих новостей

TOKEN = "8896652212:AAE5hg7ODgmoTkhL7KbxdizWYg--PcT0jjU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Автоматическое хранилище инцидентов
current_incidents = {
    "accidents": ["⏳ Инициализация... Ожидание первой проверки новостей."],
    "works": ["⏳ Инициализация... Ожидание первой проверки дорожных работ."]
}

# Функция для автоматического поиска новостей о ДТП и работах на М-3
async def fetch_road_news():
    global current_incidents
    while True:
        try:
            logging.info("🔄 Фоновая проверка: ищем свежие новости по Киевскому шоссе (М-3)...")
            
            with DDGS() as ddgs:
                # Ищем новости про ДТП на М-3 Украина / Киевское шоссе за последнее время
                accidents_results = list(ddgs.text("Киевское шоссе М3 ДТП авария сегодня", max_results=3))
                works_results = list(ddgs.text("Киевское шоссе М3 дорожные работы ремонт", max_results=3))
                
                if accidents_results:
                    new_accidents = []
                    for item in accidents_results:
                        title = item.get('title', 'Без названия')
                        snippet = item.get('body', '')
                        new_accidents.f(f"⚠️ {title} — {snippet[:100]}...")
                    if new_accidents:
                        current_incidents["accidents"] = new_accidents[:3]

                if works_results:
                    new_works = []
                    for item in works_results:
                        title = item.get('title', 'Без названия')
                        snippet = item.get('body', '')
                        new_works.append(f"🚧 {title} — {snippet[:100]}...")
                    if new_works:
                        current_incidents["works"] = new_works[:3]
                        
            logging.info("✅ Данные успешно обновлены из интернета!")
        except Exception as e:
            logging.error(f"Ошибка при фоновом обновлении новостей: {e}")

        # Проверка каждые 5 минут (300 секунд)
        await asyncio.sleep(300)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "🚗 **Автоматический бот Киевского шоссе (М-3)**\n\n"
        "Я каждые 5 минут сканирую новости и интернет на наличие ДТП и дорожных работ.\n\n"
        "📌 **Команды:**\n"
        "/status — Общая ситуация\n"
        "/accidents — Свежие аварии и ремонт (авто-обновление)\n"
        "/cameras — Камеры и карты\n\n"
        "🛠 Также доступен ручной ввод:\n"
        "`/add_acc [текст]` | `/add_work [текст]`"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    status_text = (
        "📊 **Оперативная ситуация на М-3 «Украина»:**\n\n"
        "• Мониторинг пробок: Активен (автоматический режим)\n"
        "• Фоновое обновление новостей: Каждые 5 минут\n"
        "• Используйте /accidents для просмотра актуальных сводок по ДТП."
    )
    await message.answer(status_text, parse_mode="Markdown")

@dp.message(Command("accidents"))
async def cmd_accidents(message: Message):
    accidents_list = "\n\n".join(current_incidents["accidents"]) if current_incidents["accidents"] else "✅ Свежих аварий не найдено."
    works_list = "\n\n".join(current_incidents["works"]) if current_incidents["works"] else "✅ Дорожных работ не найдено."

    response_text = (
        f"🚨 **Оперативная сводка из интернета:**\n\n"
        f"**🔴 Последние ДТП и происшествия:**\n{accidents_list}\n\n"
        f"**🚧 Дорожные работы и ремонт:**\n{works_list}"
    )
    await message.answer(response_text, parse_mode="Markdown")

@dp.message(Command("add_acc"))
async def add_accident(message: Message):
    text = message.text.replace("/add_acc", "").strip()
    if text:
        current_incidents["accidents"].insert(0, f"⚠️ (От водителя) {text}")
        await message.answer(f"✅ Добавлено в сводку аварий!")

@dp.message(Command("add_work"))
async def add_work(message: Message):
    text = message.text.replace("/add_work", "").strip()
    if text:
        current_incidents["works"].insert(0, f"🚧 (От водителя) {text}")
        await message.answer(f"✅ Добавлено в сводку работ!")

@dp.message(Command("cameras"))
async def cmd_cameras(message: Message):
    await message.answer("📷 [Яндекс.Карты — Киевское шоссе](https://yandex.ru/maps)", parse_mode="Markdown", disable_web_page_preview=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен с автоматическим поиском новостей!")
    
    # Запускаем фоновый цикл сбора новостей параллельно с ботом
    asyncio.create_task(fetch_road_news())
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

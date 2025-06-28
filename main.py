from aiogram import Bot, Dispatcher, executor, types
from keyboards import main_kb
import os
from dotenv import load_dotenv
from tarot_cards import get_card_meaning

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        "🔮 Привет! Это - Таро говорит!.\n"
        "Здесь ты можешь сделать расклад Таро и получить ответ на любой вопрос.\n\n"

        "❓ Что я могу:\n"
        "🫖 Рассказать о сути карт\n"
        "🃏 Сделать расклад по выбранным карточкам\n"
        "✨ Получить прогноз на день или ситуацию\n\n"

        "📌 Пример вопроса:\n"
        "Буду ли я встречаться с Кириллом?\n\n"

        "💬 Чтобы начать:\n"
        "1️⃣ Напиши свой вопрос \n\n"

        "Например: Жрица, Колесо фортуны, Смерть",
        reply_markup=main_kb
    )

# Команда /help
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply("Чтобы получить значение карт, напиши:\n/read Карта1, Карта2, Карта3")

# Команда /read
@dp.message_handler(commands=['read'])
async def read_cards(message: types.Message):
    try:
        # Получаем текст после команды
        cards_text = message.text.split(' ', 1)[1]
        cards_list = [card.strip() for card in cards_text.split(',')]

        response = "🔮 Вот значения карт из вашего расклада:\n\n"

        for card in cards_list:
            meaning = get_card_meaning(card)
            response += f"🃏 <b>{card}</b>:\n{meaning}\n\n"

        await message.reply(response, parse_mode="HTML")

    except IndexError:
        await message.reply("❗ Укажите хотя бы одну карту после команды /read")

# Обработчик нажатий на кнопки (callback)
@dp.callback_query_handler(lambda c: c.data in ['today', 'tarot', 'miniapp', 'about'])
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == 'today':
        await bot.send_message(callback_query.from_user.id, "🌙 Карта дня — «Луна». Она указывает на интуицию.")
    elif callback_query.data == 'tarot':
        kb = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text="🃏 Сделать расклад", web_app=types.WebAppInfo(url="https://your-tarot-miniapp.vercel.app/miniapp.html"))
        )
        await bot.send_message(callback_query.from_user.id, "👉 Открой Mini App и сделай свой расклад:", reply_markup=kb)
    elif callback_query.data == 'about':
        await bot.send_message(callback_query.from_user.id,
            "☕ Таро говорит! — это пространство, где Таро встречается с уютом.\n"
            "Каждый день мы делаем расклады, учимся читать карты и находим ответы на важные вопросы.\n"
            "Будь как дома, гадай с чашкой чая в руках."
        )
    elif callback_query.data == 'miniapp':
        kb = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text="🃏 Сделать расклад", web_app=types.WebAppInfo(url="https://your-tarot-miniapp.vercel.app/miniapp.html"))
        )
        await bot.send_message(callback_query.from_user.id, "👉 Вот ваш интерактивный расклад:", reply_markup=kb)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
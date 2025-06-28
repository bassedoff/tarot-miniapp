from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главная клавиатура
main_kb = InlineKeyboardMarkup(row_width=2)
btn_today = InlineKeyboardButton(text="🔮 Расклад дня", callback_data="today")
btn_tarot = InlineKeyboardButton(text="🃏 Сделать", callback_data="tarot")
btn_miniapp = InlineKeyboardButton(text="🃏 Сделать расклад", web_app={"url": "https://yourdomain.com/tarot "})
btn_about = InlineKeyboardButton(text="ℹ️ О проекте", callback_data="about")

main_kb.add(btn_today, btn_tarot).add(btn_miniapp).add(btn_about)
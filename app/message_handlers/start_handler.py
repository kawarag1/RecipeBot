from app.bot.bot import bot

from telebot import types
import json


with open("app/data/recipes.json", "r", encoding="utf-8") as f:
    RECIPES = json.load(f)

@bot.message_handler(commands=["start"])
async def welcome_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📖 Все рецепты"),
        types.KeyboardButton("🔍 Выбрать блюдо"),
    )
    bot.send_message(
        message.chat.id,
        "Привет! Я бот, который поможет тебе найти вкусные рецепты. Выбери один из вариантов ниже, чтобы начать.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "📖 Все рецепты")
async def show_all_recipes(message):
    if not RECIPES:
        bot.send_message(message.chat.id, "Пока что нет доступных рецептов.")
        return

    text_parts = ["📖 <b>Все рецепты:</b>\n"]
    for name, data in RECIPES.items():
        text_parts.append(
            f"\n🍲 <b>{name.title()}</b>\n"
            f"<b>Ингредиенты:</b> {', '.join(data['ингредиенты'])}\n"
            f"<b>Приготовление:</b>\n{data['рецепт']}\n"
            f"{'—' * 20}"
        )

    full_text = "\n".join(text_parts)

    if len(full_text) <= 4096:
        bot.send_message(message.chat.id, full_text, parse_mode="HTML")
    else:
        chunk = ""
        for part in text_parts:
            if len(chunk) + len(part) > 4000:
                bot.send_message(message.chat.id, chunk, parse_mode="HTML")
                chunk = ""
            chunk += part
        if chunk:
            bot.send_message(message.chat.id, chunk, parse_mode="HTML")
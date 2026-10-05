import json
from pathlib import Path

from telebot import types

from recipebot.app.bot.bot import bot

RECIPES_PATH = Path(__file__).parent.parent / "utils" / "recipes.json"
with RECIPES_PATH.open(encoding="utf-8") as f:
    RECIPES = json.load(f)


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("📖 Все рецепты"),
        types.KeyboardButton("🔍 Выбрать блюдо"),
    )
    return markup


@bot.message_handler(commands=["start"])
async def welcome_message(message):
    try:
        await bot.send_message(
            message.chat.id,
            "Привет! Я бот, который поможет тебе найти вкусные рецепты. Выбери один из вариантов ниже, чтобы начать.",
            reply_markup=main_menu(),
        )
    except Exception as e:
        print(f"Error in welcome_message: {e}")   


@bot.message_handler(func=lambda m: m.text == "Назад")
async def go_back(message):
    await bot.send_message(
        message.chat.id,
        "Вы вернулись в главное меню.",
        reply_markup=main_menu(),
    )


@bot.message_handler(func=lambda m: m.text == "🔍 Выбрать блюдо")
async def choose_dish(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("🍲 Супы"),
        types.KeyboardButton("🥗 Салаты"),
        types.KeyboardButton("🍚 Гарниры"),
        types.KeyboardButton("🍽 Основные блюда"),
    )
    for dish in RECIPES:
        markup.add(types.KeyboardButton(dish))
    markup.add(types.KeyboardButton("Назад"))
    await bot.send_message(
        message.chat.id,
        "Выберите категорию или конкретное блюдо:",
        reply_markup=markup,
    )


@bot.message_handler(
    func=lambda m: m.text in {"🍲 Супы", "🥗 Салаты", "🍚 Гарниры", "🍽 Основные блюда"}
)
async def choose_category(message):
    category = message.text.split(" ", 1)[1]
    dishes = [
        name
        for name, recipe in RECIPES.items()
        if recipe.get("Категория") == category
    ]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for dish in dishes:
        markup.add(types.KeyboardButton(dish))
    markup.add(
        types.KeyboardButton("🔍 Выбрать блюдо"),
        types.KeyboardButton("Назад"),
    )

    text = (
        f"Блюда в категории «{category}»:"
        if dishes
        else f"В категории «{category}» пока нет блюд."
    )
    await bot.send_message(message.chat.id, text, reply_markup=markup)
    

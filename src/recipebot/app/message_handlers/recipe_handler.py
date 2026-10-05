from recipebot.app.bot.bot import bot
from recipebot.app.message_handlers.start_handler import RECIPES, main_menu

@bot.message_handler(func=lambda m: m.text == "📖 Все рецепты")
async def show_all_recipes(message):
    try:
        if not RECIPES:
            await bot.send_message(message.chat.id, "Пока что нет доступных рецептов.")
            return

        text_parts = ["📖 <b>Все рецепты:</b>\n"]
        for name, data in RECIPES.items():
            text_parts.append(
                f"\n🍲 <b>{name.title()}</b>\n"
                f"<b>Ингредиенты:</b> {', '.join(data['Ингредиенты'])}\n"
                f"<b>Приготовление:</b>\n{data['Рецепт']}\n"
                f"{'—' * 20}"
            )

        full_text = "\n".join(text_parts)

        if len(full_text) <= 4096:
            await bot.send_message(message.chat.id, full_text, parse_mode="HTML")
        else:
            chunk = ""
            for part in text_parts:
                if len(chunk) + len(part) > 4000:
                    await bot.send_message(message.chat.id, chunk, parse_mode="HTML")
                    chunk = ""
                chunk += part
            if chunk:
                await bot.send_message(message.chat.id, chunk, parse_mode="HTML")

    except Exception as e:
        print(f"Error in show_all_recipes: {e}")


@bot.message_handler(func=lambda m: m.text in RECIPES)
async def show_selected_recipe(message):
    recipe = RECIPES[message.text]
    text = (
        f"🍲 <b>{message.text}</b>\n"
        f"<b>Категория:</b> {recipe['Категория']}\n"
        f"<b>Ингредиенты:</b> {', '.join(recipe['Ингредиенты'])}\n"
        f"<b>Приготовление:</b>\n{recipe['Рецепт']}"
    )
    await bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_markup=main_menu(),
    )
import asyncio

from recipebot.app.bot.bot import bot
from recipebot.app.message_handlers.start_handler import welcome_message
from recipebot.app.message_handlers.recipe_handler import show_all_recipes


async def main():
    try:
        print("Starting bot...")
        await bot.infinity_polling()
    except Exception as e:
        print(f"Error occurred: {e}")



if __name__ == "__main__":
    asyncio.run(main())
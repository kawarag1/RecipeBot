from os import getenv

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

load_dotenv()

bot = AsyncTeleBot(getenv("TOKEN"))
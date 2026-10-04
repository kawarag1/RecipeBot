from telebot.async_telebot import AsyncTeleBot
from os import getenv

bot = AsyncTeleBot(getenv("token"))
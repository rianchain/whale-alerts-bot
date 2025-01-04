import requests
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

SELECT THE CHAIN => SELECT THE WALLET THEY WANT TO TRACK => SELECT THE TIME INTERVAL THEY WANT TO BE NOTIFIED

CHAIN, WALLET, INTERVAL = range(3)

user_data = {}

# Create the function to get the information from insight api

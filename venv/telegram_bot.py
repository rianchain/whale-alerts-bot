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
def fetch_transactions(
        chain_id,
        client_id,
        wallet_address,
        limit=1,
        sort_by="block_number",
        sort_order="desc",
):
    try: 
        transactions_url = (f"https://{chain_id}.insight.thirdweb.com/v1/transactions")
        params = {
            "limit": limit,
            "clientId": client_id,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "filter_from_address": wallet_address,
        }

        response = requests.get(transactions_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:

        return {"error": str(e)}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Welcome to the WHALERTS Whale Tracker Bot! 🚀\n\n"
        "With this bot, you can:\n"
        "- Monitor blockchain activity. \n"
        "- Track specific wallet addresses. \n\n"
        "Use /setup to configure your bot preferences.\n"
    )
    await update.message.reply_text(welcome_text)

async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Which blockchain network do you want to work with? (e.g., Ethereum, Solana, etc.)",
        reply_markup=ReplyKeyboardMarkup(
            [["Ethereum", "Solana"]], one_time_keyboard=True
        ),
    )
    return CHAIN

async def set_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = update.message.text
    user_data[update.effective_user.id] = {"chain": chain}
    await update.message.reply_text(
        "Please enter the wallet address you want to track!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return WALLET

async def set_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet = update.message.text
    user_data[update.effective_user.id]["wallet"] = wallet

    await update.message.reply_text(
        "How often do you want to receive updates?\n\n" "Choose in interval",
        reply_markup=ReplyKeyboardMarkup(
            [["1 minute", "1 hour", "4 hour", "12 hours"]],
            one_time_keyboard=True,
        ),
    )
    return INTERVAL


async def set_interval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    interval_text = update.message.text
    user_id = update.effective_user.id

    interval_mapping = {
        "1 Minute": 60,
        "1 hour": 3600,
        "4 hours": 14400,
        "12 hours": 43200,
    }
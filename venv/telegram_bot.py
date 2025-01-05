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
    except requests.exceptions.RequestException as e:

        return {"error": str(e)}